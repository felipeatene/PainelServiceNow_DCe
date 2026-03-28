"""
Servidor local para Painel DC-e com proxy reverso para ServiceNow/SharePoint.
Resolve CORS ao servir HTML via HTTP e proxiar requests para APIs.

Implementado nesta versão:
- JWT access + refresh
- Persistência de refresh tokens e auditoria em SQLite
- Rate limiting em endpoints de autenticação
- CORS por variáveis de ambiente
- Início de SSO Microsoft (Azure AD): /auth/microsoft/start e /auth/microsoft/callback
"""

import base64
import hashlib
import http.server
import json
import os
import secrets
import sqlite3
import sys
import threading
import time
import urllib.error
import urllib.parse
import urllib.request

try:
    import jwt
except ImportError:
    print("\n❌ PyJWT não está instalado.")
    print("   Execute: py -m pip install -r requirements.txt")
    sys.exit(1)

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass


PORT = int(os.environ.get("PORT", 8080))
HOST = os.environ.get("HOST", "0.0.0.0")

SERVICENOW_BASE = os.environ.get("SERVICENOW_BASE", "https://ibmlocaliza.service-now.com")
SHAREPOINT_SITE_BASE = os.environ.get("SHAREPOINT_SITE_BASE", "https://localiza.sharepoint.com/sites/DCE")

JWT_SECRET = os.environ.get("JWT_SECRET", "dev-secret-key-change-in-production")
JWT_ACCESS_EXPIRY = int(os.environ.get("JWT_ACCESS_EXPIRY", 3600))
JWT_REFRESH_EXPIRY = int(os.environ.get("JWT_REFRESH_EXPIRY", 604800))

DB_PATH = os.environ.get("DB_PATH", os.path.join(os.path.dirname(__file__), "auth.db"))

RATE_LIMIT_ATTEMPTS = int(os.environ.get("RATE_LIMIT_ATTEMPTS", 8))
RATE_LIMIT_WINDOW_SECONDS = int(os.environ.get("RATE_LIMIT_WINDOW_SECONDS", 60))

raw_origins = os.environ.get("ALLOWED_ORIGINS", "").strip()
if raw_origins:
    ALLOWED_ORIGINS = [origin.strip() for origin in raw_origins.split(",") if origin.strip()]
else:
    ALLOWED_ORIGINS = [
        f"http://localhost:{PORT}",
        f"http://127.0.0.1:{PORT}",
    ]

AZURE_TENANT_ID = os.environ.get("AZURE_TENANT_ID", "")
AZURE_CLIENT_ID = os.environ.get("AZURE_CLIENT_ID", "")
AZURE_CLIENT_SECRET = os.environ.get("AZURE_CLIENT_SECRET", "")
AZURE_REDIRECT_URI = os.environ.get(
    "AZURE_REDIRECT_URI", f"http://localhost:{PORT}/auth/microsoft/callback"
)
AZURE_SCOPE = os.environ.get("AZURE_SCOPE", "openid profile email User.Read")


_db_lock = threading.Lock()
_rate_limit_store = {}
_auth_cache = {}  # {username: {"basic": "...", "last_used": ts}}
_ms_state_store = {}  # {state: {created_at, ip}}


def _now_ts():
    return int(time.time())


def _token_hash(token):
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def _client_ip(handler):
    forwarded = handler.headers.get("X-Forwarded-For", "")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return handler.client_address[0] if handler.client_address else "unknown"


def _audit(event_type, status, user="-", ip="-", details=""):
    now = _now_ts()
    log = {
        "ts": now,
        "event": event_type,
        "status": status,
        "user": user,
        "ip": ip,
        "details": details,
    }
    sys.stderr.write(f"\033[34m[AUDIT]\033[0m {json.dumps(log, ensure_ascii=False)}\n")
    try:
        with _db_lock:
            conn = sqlite3.connect(DB_PATH)
            conn.execute(
                """
                INSERT INTO audit_events(ts, event_type, status, username, ip, details)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (now, event_type, status, user, ip, details[:1000]),
            )
            conn.commit()
            conn.close()
    except Exception as e:
        sys.stderr.write(f"\033[31m[DB]\033[0m Falha ao gravar auditoria: {e}\n")


def _init_db():
    with _db_lock:
        conn = sqlite3.connect(DB_PATH)
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS refresh_tokens (
                token_hash TEXT PRIMARY KEY,
                username TEXT NOT NULL,
                jti TEXT NOT NULL,
                issued_at INTEGER NOT NULL,
                expires_at INTEGER NOT NULL,
                revoked INTEGER NOT NULL DEFAULT 0,
                ip TEXT,
                user_agent TEXT
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS audit_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ts INTEGER NOT NULL,
                event_type TEXT NOT NULL,
                status TEXT NOT NULL,
                username TEXT,
                ip TEXT,
                details TEXT
            )
            """
        )
        conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_refresh_username ON refresh_tokens(username)"
        )
        conn.execute("CREATE INDEX IF NOT EXISTS idx_refresh_exp ON refresh_tokens(expires_at)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_audit_ts ON audit_events(ts)")
        conn.commit()
        conn.close()


def _cleanup_expired_tokens():
    try:
        with _db_lock:
            conn = sqlite3.connect(DB_PATH)
            conn.execute("DELETE FROM refresh_tokens WHERE expires_at < ?", (_now_ts(),))
            conn.commit()
            conn.close()
    except Exception as e:
        sys.stderr.write(f"\033[31m[DB]\033[0m Falha no cleanup de refresh tokens: {e}\n")


def _store_refresh_token(refresh_token, username, jti, expires_at, ip, user_agent):
    token_h = _token_hash(refresh_token)
    with _db_lock:
        conn = sqlite3.connect(DB_PATH)
        conn.execute(
            """
            INSERT OR REPLACE INTO refresh_tokens
            (token_hash, username, jti, issued_at, expires_at, revoked, ip, user_agent)
            VALUES (?, ?, ?, ?, ?, 0, ?, ?)
            """,
            (token_h, username, jti, _now_ts(), expires_at, ip, user_agent),
        )
        conn.commit()
        conn.close()


def _refresh_token_valid(refresh_token, expected_username, expected_jti):
    token_h = _token_hash(refresh_token)
    with _db_lock:
        conn = sqlite3.connect(DB_PATH)
        row = conn.execute(
            """
            SELECT username, jti, expires_at, revoked
            FROM refresh_tokens
            WHERE token_hash = ?
            """,
            (token_h,),
        ).fetchone()
        conn.close()

    if not row:
        return False

    username, jti, expires_at, revoked = row
    if revoked:
        return False
    if username != expected_username or jti != expected_jti:
        return False
    if int(expires_at) < _now_ts():
        return False
    return True


def _revoke_refresh_token(refresh_token):
    token_h = _token_hash(refresh_token)
    with _db_lock:
        conn = sqlite3.connect(DB_PATH)
        conn.execute("UPDATE refresh_tokens SET revoked = 1 WHERE token_hash = ?", (token_h,))
        conn.commit()
        conn.close()


def _revoke_all_user_tokens(username):
    with _db_lock:
        conn = sqlite3.connect(DB_PATH)
        conn.execute("UPDATE refresh_tokens SET revoked = 1 WHERE username = ?", (username,))
        conn.commit()
        conn.close()


def _make_basic(user, password):
    raw = f"{user}:{password}".encode("utf-8")
    return base64.b64encode(raw).decode("ascii")


def _validate_credentials(basic_header):
    url = SERVICENOW_BASE + "/api/now/table/sys_user?sysparm_limit=1&sysparm_fields=user_name"
    req = urllib.request.Request(url)
    req.add_header("Accept", "application/json")
    req.add_header("Authorization", f"Basic {basic_header}")
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            if resp.status == 200:
                data = json.loads(resp.read())
                results = data.get("result", [])
                return results[0].get("user_name", "unknown") if results else "unknown"
    except Exception:
        pass
    return None


def _encode_jwt(username, token_type="access", auth_method="password", jti=None):
    now = _now_ts()
    expiry = JWT_REFRESH_EXPIRY if token_type == "refresh" else JWT_ACCESS_EXPIRY
    payload = {
        "sub": username,
        "iat": now,
        "exp": now + expiry,
        "type": token_type,
        "auth_method": auth_method,
    }
    if jti:
        payload["jti"] = jti
    return jwt.encode(payload, JWT_SECRET, algorithm="HS256")


def _decode_jwt(token):
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None


def _decode_jwt_unverified(token):
    try:
        return jwt.decode(token, options={"verify_signature": False, "verify_exp": False})
    except Exception:
        return {}


def _get_basic_auth(username):
    return _auth_cache.get(username, {}).get("basic")


def _rate_limit_check(route_key, client_ip):
    now = time.time()
    key = f"{client_ip}:{route_key}"
    bucket = _rate_limit_store.setdefault(key, [])
    threshold = now - RATE_LIMIT_WINDOW_SECONDS
    bucket[:] = [ts for ts in bucket if ts >= threshold]
    if len(bucket) >= RATE_LIMIT_ATTEMPTS:
        return False, int(RATE_LIMIT_WINDOW_SECONDS)
    bucket.append(now)
    return True, 0


def _ms_configured():
    return bool(AZURE_TENANT_ID and AZURE_CLIENT_ID and AZURE_CLIENT_SECRET and AZURE_REDIRECT_URI)


def _ms_build_authorize_url(state):
    base = f"https://login.microsoftonline.com/{AZURE_TENANT_ID}/oauth2/v2.0/authorize"
    query = urllib.parse.urlencode(
        {
            "client_id": AZURE_CLIENT_ID,
            "response_type": "code",
            "redirect_uri": AZURE_REDIRECT_URI,
            "response_mode": "query",
            "scope": AZURE_SCOPE,
            "state": state,
            "prompt": "select_account",
        }
    )
    return f"{base}?{query}"


def _ms_exchange_code_for_token(code):
    token_endpoint = f"https://login.microsoftonline.com/{AZURE_TENANT_ID}/oauth2/v2.0/token"
    body = urllib.parse.urlencode(
        {
            "client_id": AZURE_CLIENT_ID,
            "client_secret": AZURE_CLIENT_SECRET,
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": AZURE_REDIRECT_URI,
            "scope": AZURE_SCOPE,
        }
    ).encode("utf-8")

    req = urllib.request.Request(token_endpoint, data=body, method="POST")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")
    req.add_header("Accept", "application/json")
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.loads(resp.read().decode("utf-8"))


class ProxyHandler(http.server.SimpleHTTPRequestHandler):
    def _send_cors_headers(self, origin=None):
        if not origin:
            return
        if origin in ALLOWED_ORIGINS:
            self.send_header("Access-Control-Allow-Origin", origin)
            self.send_header("Access-Control-Allow-Credentials", "true")
            self.send_header("Access-Control-Allow-Headers", "Accept, Content-Type, Authorization")
            self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")

    def _send_json(self, status, obj):
        body = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        origin = self.headers.get("Origin", "")
        self._send_cors_headers(origin)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_html(self, status, html):
        body = html.encode("utf-8")
        self.send_response(status)
        origin = self.headers.get("Origin", "")
        self._send_cors_headers(origin)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _get_jwt_from_header(self):
        header = self.headers.get("Authorization", "")
        if header.startswith("Bearer "):
            return header[7:].strip()
        return None

    def _get_auth_payload(self):
        token = self._get_jwt_from_header()
        if not token:
            return None
        return _decode_jwt(token)

    def _get_auth_username(self):
        payload = self._get_auth_payload()
        return payload.get("sub") if payload else None

    def _read_json_body(self):
        try:
            length = int(self.headers.get("Content-Length", 0))
            raw = self.rfile.read(length) if length > 0 else b"{}"
            return json.loads(raw)
        except Exception:
            return None

    def do_OPTIONS(self):
        self.send_response(204)
        origin = self.headers.get("Origin", "")
        self._send_cors_headers(origin)
        self.send_header("Content-Length", "0")
        self.end_headers()

    def do_GET(self):
        if self.path == "/auth/status":
            self._auth_status()
            return
        if self.path.startswith("/auth/microsoft/start"):
            self._auth_microsoft_start()
            return
        if self.path.startswith("/auth/microsoft/callback"):
            self._auth_microsoft_callback()
            return
        if self.path.startswith("/proxy/"):
            self._handle_proxy("GET")
            return
        if self.path.startswith("/proxy-sp/"):
            self._handle_sharepoint_proxy("GET")
            return
        super().do_GET()

    def do_POST(self):
        if self.path == "/auth/login":
            self._auth_login()
            return
        if self.path == "/auth/refresh":
            self._auth_refresh()
            return
        if self.path == "/auth/logout":
            self._auth_logout()
            return
        if self.path.startswith("/proxy/"):
            self._handle_proxy("POST")
            return
        self._send_json(404, {"error": "Not found"})

    def _auth_login(self):
        ip = _client_ip(self)
        allowed, retry_after = _rate_limit_check("auth_login", ip)
        if not allowed:
            _audit("auth.login", "rate_limited", ip=ip, details=f"retry_after={retry_after}")
            self._send_json(429, {"ok": False, "error": "Muitas tentativas. Aguarde e tente novamente."})
            return

        data = self._read_json_body()
        if not isinstance(data, dict):
            self._send_json(400, {"ok": False, "error": "JSON inválido"})
            return

        username = str(data.get("username", "")).strip()
        password = str(data.get("password", ""))
        if not username or not password:
            self._send_json(400, {"ok": False, "error": "Usuário e senha são obrigatórios"})
            return

        basic = _make_basic(username, password)
        validated_user = _validate_credentials(basic)
        if not validated_user:
            _audit("auth.login", "failed", user=username, ip=ip, details="invalid_credentials")
            self._send_json(401, {"ok": False, "error": "Credenciais inválidas"})
            return

        _auth_cache[validated_user] = {"basic": basic, "last_used": _now_ts()}

        refresh_jti = secrets.token_urlsafe(24)
        access_token = _encode_jwt(validated_user, token_type="access", auth_method="password")
        refresh_token = _encode_jwt(
            validated_user,
            token_type="refresh",
            auth_method="password",
            jti=refresh_jti,
        )
        refresh_exp = _now_ts() + JWT_REFRESH_EXPIRY
        _store_refresh_token(
            refresh_token,
            validated_user,
            refresh_jti,
            refresh_exp,
            ip,
            self.headers.get("User-Agent", ""),
        )

        _audit("auth.login", "ok", user=validated_user, ip=ip)
        self._send_json(
            200,
            {
                "ok": True,
                "user": validated_user,
                "access_token": access_token,
                "refresh_token": refresh_token,
                "expires_in": JWT_ACCESS_EXPIRY,
            },
        )

    def _auth_refresh(self):
        ip = _client_ip(self)
        allowed, retry_after = _rate_limit_check("auth_refresh", ip)
        if not allowed:
            _audit("auth.refresh", "rate_limited", ip=ip, details=f"retry_after={retry_after}")
            self._send_json(429, {"ok": False, "error": "Muitas tentativas. Aguarde."})
            return

        data = self._read_json_body()
        if not isinstance(data, dict):
            self._send_json(400, {"ok": False, "error": "JSON inválido"})
            return

        refresh_token = str(data.get("refresh_token", "")).strip()
        if not refresh_token:
            self._send_json(400, {"ok": False, "error": "refresh_token obrigatório"})
            return

        payload = _decode_jwt(refresh_token)
        if not payload or payload.get("type") != "refresh":
            _audit("auth.refresh", "failed", ip=ip, details="invalid_jwt")
            self._send_json(401, {"ok": False, "error": "Refresh token inválido ou expirado"})
            return

        username = payload.get("sub")
        jti = payload.get("jti")
        if not username or not jti:
            _audit("auth.refresh", "failed", ip=ip, details="missing_sub_or_jti")
            self._send_json(401, {"ok": False, "error": "Refresh token inválido"})
            return

        if not _refresh_token_valid(refresh_token, username, jti):
            _audit("auth.refresh", "failed", user=username, ip=ip, details="token_not_active")
            self._send_json(401, {"ok": False, "error": "Refresh token revogado ou inválido"})
            return

        new_access_token = _encode_jwt(
            username,
            token_type="access",
            auth_method=payload.get("auth_method", "password"),
        )
        _audit("auth.refresh", "ok", user=username, ip=ip)
        self._send_json(
            200,
            {
                "ok": True,
                "access_token": new_access_token,
                "expires_in": JWT_ACCESS_EXPIRY,
            },
        )

    def _auth_logout(self):
        ip = _client_ip(self)
        payload = self._get_auth_payload()
        if not payload:
            self._send_json(200, {"ok": True})
            return

        username = payload.get("sub")
        if username:
            _auth_cache.pop(username, None)
            _revoke_all_user_tokens(username)
            _audit("auth.logout", "ok", user=username, ip=ip)
        self._send_json(200, {"ok": True})

    def _auth_status(self):
        payload = self._get_auth_payload()
        if not payload:
            self._send_json(200, {"authenticated": False})
            return

        self._send_json(
            200,
            {
                "authenticated": True,
                "user": payload.get("sub"),
                "auth_method": payload.get("auth_method", "password"),
                "timestamp": _now_ts(),
            },
        )

    def _auth_microsoft_start(self):
        ip = _client_ip(self)
        parsed = urllib.parse.urlparse(self.path)
        qs = urllib.parse.parse_qs(parsed.query)
        redirect_mode = qs.get("redirect", ["0"])[0] == "1"

        if not _ms_configured():
            if redirect_mode:
                missing = []
                if not AZURE_TENANT_ID:
                    missing.append("AZURE_TENANT_ID")
                if not AZURE_CLIENT_ID:
                    missing.append("AZURE_CLIENT_ID")
                if not AZURE_CLIENT_SECRET:
                    missing.append("AZURE_CLIENT_SECRET")
                if not AZURE_REDIRECT_URI:
                    missing.append("AZURE_REDIRECT_URI")

                missing_list = "".join([f"<li>{name}</li>" for name in missing]) or "<li>Nenhuma</li>"
                self._send_html(
                    503,
                    f"""
                    <html><body style='font-family:Segoe UI;padding:24px'>
                    <h3>SSO Microsoft não configurado</h3>
                    <p>Defina as variáveis abaixo no arquivo .env e reinicie o servidor:</p>
                    <ul>{missing_list}</ul>
                    </body></html>
                    """,
                )
                return

            self._send_json(
                503,
                {
                    "ok": False,
                    "error": "SSO Microsoft não configurado no servidor",
                },
            )
            return

        state = secrets.token_urlsafe(24)
        _ms_state_store[state] = {"created_at": _now_ts(), "ip": ip}
        auth_url = _ms_build_authorize_url(state)
        _audit("auth.microsoft.start", "ok", ip=ip)

        if redirect_mode:
            self.send_response(302)
            origin = self.headers.get("Origin", "")
            self._send_cors_headers(origin)
            self.send_header("Location", auth_url)
            self.send_header("Content-Length", "0")
            self.end_headers()
            return

        self._send_json(200, {"ok": True, "auth_url": auth_url})

    def _auth_microsoft_callback(self):
        ip = _client_ip(self)
        parsed = urllib.parse.urlparse(self.path)
        qs = urllib.parse.parse_qs(parsed.query)

        if "error" in qs:
            error_desc = qs.get("error_description", ["erro desconhecido"])[0]
            _audit("auth.microsoft.callback", "failed", ip=ip, details=error_desc)
            self._send_html(400, f"<h3>Falha no login Microsoft</h3><p>{error_desc}</p>")
            return

        code = qs.get("code", [""])[0]
        state = qs.get("state", [""])[0]
        if not code or not state:
            self._send_html(400, "<h3>Callback inválido</h3><p>Parâmetros ausentes.</p>")
            return

        state_info = _ms_state_store.pop(state, None)
        if not state_info:
            self._send_html(400, "<h3>Estado inválido</h3><p>O login expirou. Tente novamente.</p>")
            return

        if _now_ts() - int(state_info.get("created_at", 0)) > 600:
            self._send_html(400, "<h3>Estado expirado</h3><p>Faça login novamente.</p>")
            return

        try:
            token_data = _ms_exchange_code_for_token(code)
            id_token = token_data.get("id_token", "")
            claims = _decode_jwt_unverified(id_token)
            username = (
                claims.get("preferred_username")
                or claims.get("upn")
                or claims.get("email")
                or claims.get("name")
            )
            if not username:
                raise ValueError("Não foi possível identificar o usuário do token Microsoft")

            refresh_jti = secrets.token_urlsafe(24)
            access_token = _encode_jwt(username, token_type="access", auth_method="aad")
            refresh_token = _encode_jwt(
                username,
                token_type="refresh",
                auth_method="aad",
                jti=refresh_jti,
            )
            refresh_exp = _now_ts() + JWT_REFRESH_EXPIRY
            _store_refresh_token(
                refresh_token,
                username,
                refresh_jti,
                refresh_exp,
                ip,
                self.headers.get("User-Agent", ""),
            )

            _audit("auth.microsoft.callback", "ok", user=username, ip=ip)
            self._send_html(
                200,
                """
                <html><body style='font-family:Segoe UI;padding:24px'>
                <h3>Login Microsoft concluído</h3>
                <p>Você já pode voltar ao painel.</p>
                <script>
                    if (window.opener) {
                        window.opener.postMessage({
                            type: 'dce_auth_success',
                            access_token: '%s',
                            refresh_token: '%s',
                            expires_in: %d,
                            user: '%s'
                        }, '*');
                        window.close();
                    }
                </script>
                </body></html>
                """
                % (access_token, refresh_token, JWT_ACCESS_EXPIRY, str(username).replace("'", "")),
            )
        except Exception as e:
            _audit("auth.microsoft.callback", "failed", ip=ip, details=str(e))
            self._send_html(500, f"<h3>Falha no SSO</h3><p>{str(e)}</p>")

    def _handle_proxy(self, method="GET"):
        username = self._get_auth_username()
        ip = _client_ip(self)
        if not username:
            _audit("proxy.servicenow", "denied", ip=ip, details="missing_auth")
            self._send_json(401, {"error": "Não autenticado. Faça login primeiro."})
            return

        basic = _get_basic_auth(username)
        if not basic:
            _audit("proxy.servicenow", "denied", user=username, ip=ip, details="missing_basic_cache")
            self._send_json(
                403,
                {
                    "error": "Sessão autenticada, mas sem credencial ServiceNow em cache.",
                    "hint": "Faça login por usuário/senha para acessar /proxy do ServiceNow.",
                },
            )
            return

        target_path = self.path[len("/proxy") :]
        target_url = SERVICENOW_BASE + target_path

        req = urllib.request.Request(target_url, method=method)
        req.add_header("Accept", "application/json")
        req.add_header("Authorization", f"Basic {basic}")

        if method == "POST":
            length = int(self.headers.get("Content-Length", 0))
            if length > 0:
                req.data = self.rfile.read(length)
                req.add_header("Content-Type", self.headers.get("Content-Type", "application/json"))

        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                body = resp.read()
                self.send_response(resp.status)
                origin = self.headers.get("Origin", "")
                self._send_cors_headers(origin)
                self.send_header("Content-Type", resp.headers.get("Content-Type", "application/json"))
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
                _audit("proxy.servicenow", "ok", user=username, ip=ip)
        except urllib.error.HTTPError as e:
            body = e.read() if hasattr(e, "read") else b""
            self.send_response(e.code)
            origin = self.headers.get("Origin", "")
            self._send_cors_headers(origin)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            _audit("proxy.servicenow", "http_error", user=username, ip=ip, details=f"status={e.code}")
        except Exception as e:
            msg = json.dumps({"error": str(e)}).encode("utf-8")
            self.send_response(502)
            origin = self.headers.get("Origin", "")
            self._send_cors_headers(origin)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(msg)))
            self.end_headers()
            self.wfile.write(msg)
            _audit("proxy.servicenow", "exception", user=username, ip=ip, details=str(e))

    def _handle_sharepoint_proxy(self, method="GET"):
        if method != "GET":
            self._send_json(405, {"error": "Método não suportado para proxy SharePoint"})
            return

        target_path = self.path[len("/proxy-sp") :]
        if not target_path.startswith("/_api/"):
            self._send_json(400, {"error": "Path inválido. Use /proxy-sp/_api/..."})
            return

        target_url = SHAREPOINT_SITE_BASE + target_path
        req = urllib.request.Request(target_url, method="GET")
        req.add_header("Accept", "application/json;odata=nometadata")
        req.add_header("User-Agent", "Painel-DCE-LocalProxy/2.0")

        auth_header = self.headers.get("Authorization", "")
        if auth_header:
            req.add_header("Authorization", auth_header)

        ip = _client_ip(self)
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                body = resp.read()
                self.send_response(resp.status)
                origin = self.headers.get("Origin", "")
                self._send_cors_headers(origin)
                self.send_header("Content-Type", resp.headers.get("Content-Type", "application/json"))
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
                _audit("proxy.sharepoint", "ok", ip=ip)
        except urllib.error.HTTPError as e:
            body = e.read() if hasattr(e, "read") else b""
            if not body:
                body = json.dumps(
                    {
                        "error": f"HTTP {e.code} no SharePoint",
                        "hint": "Valide permissões da lista e autenticação no tenant.",
                    }
                ).encode("utf-8")
            self.send_response(e.code)
            origin = self.headers.get("Origin", "")
            self._send_cors_headers(origin)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            _audit("proxy.sharepoint", "http_error", ip=ip, details=f"status={e.code}")
        except Exception as e:
            msg = json.dumps({"error": str(e)}).encode("utf-8")
            self.send_response(502)
            origin = self.headers.get("Origin", "")
            self._send_cors_headers(origin)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(msg)))
            self.end_headers()
            self.wfile.write(msg)
            _audit("proxy.sharepoint", "exception", ip=ip, details=str(e))

    def log_message(self, format, *args):
        msg = format % args
        sys.stderr.write(f"[HTTP] {msg}\n")


def _init_env_auth():
    user = os.environ.get("SN_USER", "").strip()
    password = os.environ.get("SN_PASS", "")
    if not user or not password:
        return None

    basic = _make_basic(user, password)
    validated = _validate_credentials(basic)
    if validated:
        _auth_cache[validated] = {"basic": basic, "last_used": _now_ts()}
        _audit("auth.env", "ok", user=validated, ip="local")
        return validated
    return None


def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    if JWT_SECRET == "dev-secret-key-change-in-production":
        sys.stderr.write("\n⚠️  AVISO: JWT_SECRET em valor padrão de desenvolvimento.\n")

    _init_db()
    _cleanup_expired_tokens()

    env_user = _init_env_auth()
    env_line = f"  ✓ Pre-autenticado: {env_user}" if env_user else "  Aguardando login via formulário"

    server = http.server.ThreadingHTTPServer((HOST, PORT), ProxyHandler)
    print(
        f"""
╔══════════════════════════════════════════════════════════════════╗
║  Painel DC-e — Servidor Local (JWT + SQLite + Hardening)        ║
╠══════════════════════════════════════════════════════════════════╣
║  URL:   http://localhost:{PORT}/painel-triagem-dce.html             ║
║  Proxy: /proxy/*      -> ServiceNow (JWT + Basic cache)         ║
║  Proxy: /proxy-sp/*   -> SharePoint API                          ║
║  Auth:  /auth/login | /auth/refresh | /auth/logout | /auth/status║
║  SSO:   /auth/microsoft/start | /auth/microsoft/callback         ║
║  DB:    {DB_PATH[:46]:<46}║
║  {env_line:<62}║
║  Ctrl+C para encerrar                                              ║
╚══════════════════════════════════════════════════════════════════╝
"""
    )
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor encerrado.")
        server.server_close()


if __name__ == "__main__":
    main()
