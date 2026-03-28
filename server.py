"""
Servidor local para Painel DC-e com proxy reverso para ServiceNow.
Resolve CORS ao servir HTML via HTTP e proxiar requests para a API.
Autenticação via Basic Auth (formulário no painel ou variáveis de ambiente).

Uso: python server.py
      SN_USER=usuario SN_PASS=senha python server.py
Acesse: http://localhost:8080/painel-triagem-dce.html
"""

import base64
import http.server
import json
import os
import sys
import urllib.error
import urllib.request
import uuid

PORT = 8080
SERVICENOW_BASE = "https://ibmlocaliza.service-now.com"
SHAREPOINT_SITE_BASE = "https://localiza.sharepoint.com/sites/DCE"
ALLOWED_ORIGINS = [
    f"http://localhost:{PORT}",
    f"http://127.0.0.1:{PORT}",
]

# Armazena sessions em memória: {token: {"user": "...", "basic": "Base64..."}}
_auth_store = {}


def _make_basic(user, password):
    """Gera header Basic Auth a partir de user:password."""
    raw = f"{user}:{password}".encode("utf-8")
    return base64.b64encode(raw).decode("ascii")


def _validate_credentials(basic_header):
    """Testa credenciais contra ServiceNow. Retorna username ou None."""
    url = SERVICENOW_BASE + "/api/now/table/sys_user?sysparm_limit=1&sysparm_fields=user_name"
    req = urllib.request.Request(url)
    req.add_header("Accept", "application/json")
    req.add_header("Authorization", f"Basic {basic_header}")
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            if resp.status == 200:
                data = json.loads(resp.read())
                results = data.get("result", [])
                return results[0]["user_name"] if results else "unknown"
    except (urllib.error.HTTPError, Exception):
        pass
    return None


class ProxyHandler(http.server.SimpleHTTPRequestHandler):
    """Serve arquivos estáticos, proxy /proxy/* e endpoints /auth/*."""

    def _send_cors_headers(self, origin=None):
        allowed = origin if origin in ALLOWED_ORIGINS else ALLOWED_ORIGINS[0]
        self.send_header("Access-Control-Allow-Origin", allowed)
        self.send_header("Access-Control-Allow-Credentials", "true")
        self.send_header("Access-Control-Allow-Headers", "Accept, Content-Type")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")

    def _get_session(self):
        """Lê cookie sn_session e retorna dados da session ou None."""
        cookie_header = self.headers.get("Cookie", "")
        for part in cookie_header.split(";"):
            part = part.strip()
            if part.startswith("sn_session="):
                token = part[len("sn_session="):]
                return _auth_store.get(token)
        return None

    def _send_json(self, status, obj, set_cookie=None):
        body = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        origin = self.headers.get("Origin", "")
        self._send_cors_headers(origin)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        if set_cookie:
            self.send_header("Set-Cookie", set_cookie)
        self.end_headers()
        self.wfile.write(body)

    # ── HTTP verbs ────────────────────────────────────────

    def do_OPTIONS(self):
        self.send_response(200)
        origin = self.headers.get("Origin", "")
        self._send_cors_headers(origin)
        self.send_header("Content-Length", "0")
        self.end_headers()

    def do_GET(self):
        if self.path == "/auth/status":
            self._auth_status()
        elif self.path.startswith("/proxy/"):
            self._handle_proxy("GET")
        elif self.path.startswith("/proxy-sp/"):
            self._handle_sharepoint_proxy("GET")
        else:
            super().do_GET()

    def do_POST(self):
        if self.path == "/auth/login":
            self._auth_login()
        elif self.path == "/auth/logout":
            self._auth_logout()
        elif self.path.startswith("/proxy/"):
            self._handle_proxy("POST")
        else:
            self._send_json(404, {"error": "Not found"})

    # ── Auth endpoints ────────────────────────────────────

    def _auth_login(self):
        try:
            length = int(self.headers.get("Content-Length", 0))
            raw = self.rfile.read(length)
            data = json.loads(raw)
        except (json.JSONDecodeError, ValueError):
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
            self._send_json(401, {"ok": False, "error": "Credenciais inválidas. Verifique usuário e senha."})
            return

        token = uuid.uuid4().hex
        _auth_store[token] = {"user": validated_user, "basic": basic}
        cookie = f"sn_session={token}; Path=/; HttpOnly; SameSite=Lax"
        self._send_json(200, {"ok": True, "user": validated_user}, set_cookie=cookie)
        sys.stderr.write(f"\033[32m[AUTH]\033[0m Login OK: {validated_user}\n")

    def _auth_status(self):
        session = self._get_session()
        if session:
            self._send_json(200, {"authenticated": True, "user": session["user"]})
        else:
            self._send_json(200, {"authenticated": False})

    def _auth_logout(self):
        cookie_header = self.headers.get("Cookie", "")
        for part in cookie_header.split(";"):
            part = part.strip()
            if part.startswith("sn_session="):
                token = part[len("sn_session="):]
                user = _auth_store.pop(token, {}).get("user", "?")
                sys.stderr.write(f"\033[33m[AUTH]\033[0m Logout: {user}\n")
        cookie = "sn_session=; Path=/; Max-Age=0; HttpOnly; SameSite=Lax"
        self._send_json(200, {"ok": True}, set_cookie=cookie)

    # ── Proxy reverso ─────────────────────────────────────

    def _handle_proxy(self, method="GET"):
        """Proxy: /proxy/api/... -> ServiceNow /api/... com Basic Auth."""
        session = self._get_session()
        if not session:
            self._send_json(401, {"error": "Não autenticado. Faça login primeiro."})
            return

        target_path = self.path[len("/proxy"):]
        target_url = SERVICENOW_BASE + target_path

        req = urllib.request.Request(target_url, method=method)
        req.add_header("Accept", "application/json")
        req.add_header("Authorization", f"Basic {session['basic']}")

        # Repassa body em POST
        body_data = None
        if method == "POST":
            length = int(self.headers.get("Content-Length", 0))
            if length > 0:
                body_data = self.rfile.read(length)
                req.add_header("Content-Type", self.headers.get("Content-Type", "application/json"))
                req.data = body_data

        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                body = resp.read()
                self.send_response(resp.status)
                origin = self.headers.get("Origin", "")
                self._send_cors_headers(origin)
                ct = resp.headers.get("Content-Type", "application/json")
                self.send_header("Content-Type", ct)
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
        except urllib.error.HTTPError as e:
            body = e.read() if hasattr(e, "read") else b""
            self.send_response(e.code)
            origin = self.headers.get("Origin", "")
            self._send_cors_headers(origin)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        except Exception as e:
            msg = json.dumps({"error": str(e)}).encode()
            self.send_response(502)
            origin = self.headers.get("Origin", "")
            self._send_cors_headers(origin)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(msg)))
            self.end_headers()
            self.wfile.write(msg)

    def _handle_sharepoint_proxy(self, method="GET"):
        """Proxy: /proxy-sp/_api/... -> SharePoint /_api/..."""
        if method != "GET":
            self._send_json(405, {"error": "Método não suportado para proxy SharePoint"})
            return

        target_path = self.path[len("/proxy-sp"):]
        if not target_path.startswith("/_api/"):
            self._send_json(400, {"error": "Path inválido. Use /proxy-sp/_api/..."})
            return

        target_url = SHAREPOINT_SITE_BASE + target_path
        req = urllib.request.Request(target_url, method="GET")
        req.add_header("Accept", "application/json;odata=nometadata")
        req.add_header("User-Agent", "Painel-DCE-LocalProxy/1.0")

        # Permite encaminhar bearer token opcional quando disponível no cliente.
        auth_header = self.headers.get("Authorization", "")
        if auth_header:
            req.add_header("Authorization", auth_header)

        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                body = resp.read()
                self.send_response(resp.status)
                origin = self.headers.get("Origin", "")
                self._send_cors_headers(origin)
                ct = resp.headers.get("Content-Type", "application/json")
                self.send_header("Content-Type", ct)
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
        except urllib.error.HTTPError as e:
            body = e.read() if hasattr(e, "read") else b""
            if not body:
                body = json.dumps({
                    "error": f"HTTP {e.code} no SharePoint",
                    "hint": "Valide permissões da lista e autenticação no tenant."
                }).encode("utf-8")
            self.send_response(e.code)
            origin = self.headers.get("Origin", "")
            self._send_cors_headers(origin)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        except Exception as e:
            msg = json.dumps({"error": str(e)}).encode("utf-8")
            self.send_response(502)
            origin = self.headers.get("Origin", "")
            self._send_cors_headers(origin)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(msg)))
            self.end_headers()
            self.wfile.write(msg)

    def log_message(self, format, *args):
        path = args[0] if args else ""
        msg = format % args
        if "/auth/" in str(path):
            sys.stderr.write(f"\033[35m[AUTH]\033[0m {msg}\n")
        elif "/proxy/" in str(path):
            sys.stderr.write(f"\033[36m[PROXY]\033[0m {msg}\n")
        else:
            sys.stderr.write(f"[STATIC] {msg}\n")


def _init_env_auth():
    """Se SN_USER e SN_PASS estão definidos, cria session pré-autenticada."""
    user = os.environ.get("SN_USER", "").strip()
    password = os.environ.get("SN_PASS", "")
    if not user or not password:
        return None

    basic = _make_basic(user, password)
    validated = _validate_credentials(basic)
    if validated:
        token = "env"
        _auth_store[token] = {"user": validated, "basic": basic}
        return validated
    return None


def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    env_user = _init_env_auth()
    env_line = f"  ✓ Login via env: {env_user}" if env_user else "  Aguardando login via formulário"

    server = http.server.HTTPServer(("0.0.0.0", PORT), ProxyHandler)
    print(f"""
╔══════════════════════════════════════════════════════════╗
║  Painel DC-e — Servidor Local                           ║
╠══════════════════════════════════════════════════════════╣
║                                                          ║
║  URL:   http://localhost:{PORT}/painel-triagem-dce.html     ║
║  Proxy: /proxy/* -> ServiceNow (com Basic Auth)          ║
║  Proxy: /proxy-sp/* -> SharePoint API                    ║
║                                                          ║
║  {env_line:<55}║
║                                                          ║
║  Ctrl+C para encerrar                                    ║
╚══════════════════════════════════════════════════════════╝
""")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor encerrado.")
        server.server_close()


if __name__ == "__main__":
    main()
