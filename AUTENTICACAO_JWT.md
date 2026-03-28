# 🔐 Autenticação JWT — Guia de Uso

## Visão Geral

O Painel DC-e agora utiliza **JWT (JSON Web Tokens)** para autenticação segura, substituindo o sistema anterior baseado em sessões em memória.

### Benefícios

- ✅ **Tokens com validade definida**: Access tokens (1h) + Refresh tokens (7d)
- ✅ **Refresh automático**: Renovação transparente quando token expira
- ✅ **Segurança melhorada**: Credenciais não são mais armazenadas em memória
- ✅ **Escalabilidade**: Pronto para múltiplos servidores (stateless)
- ✅ **Logout limpo**: Revogação imediata de sessões

---

## Instalação e Configuração

### 1. Instalar Dependências

```bash
pip install -r requirements.txt
```

Dependências necessárias:
- `PyJWT==2.12.1` — Para gerar e validar JWT tokens
- `cryptography==41.0.7` — Para assinatura de tokens
- `python-dotenv==1.0.0` — Para carregar variáveis de ambiente

### 2. Configurar Variáveis de Ambiente

Edite o arquivo `.env` na raiz do projeto:

```env
# ServiceNow
SN_USER=seu_usuario
SN_PASS=sua_senha
SERVICENOW_BASE=https://ibmlocaliza.service-now.com

# SharePoint
SHAREPOINT_SITE_BASE=https://localiza.sharepoint.com/sites/DCE

# JWT (IMPORTANTE: gere uma chave segura em produção!)
JWT_SECRET=your-super-secret-key-change-this-in-production
JWT_ACCESS_EXPIRY=3600   # 1 hora
JWT_REFRESH_EXPIRY=604800 # 7 dias
```

**⚠️ Importante**: Em produção, gere uma chave segura para `JWT_SECRET`:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### 3. Iniciar o Servidor

```bash
python server.py
```

Você verá:

```
╔══════════════════════════════════════════════════════════╗
║  Painel DC-e — Servidor Local (JWT Auth v2)            ║
╠══════════════════════════════════════════════════════════╣
║  URL:   http://localhost:8080/painel-triagem-dce.html   ║
║  ...
```

---

## Endpoints de Autenticação

### POST `/auth/login`

**Descrição**: Faz login com usuário e senha, retorna JWT tokens.

**Request**:
```json
{
  "username": "seu_usuario",
  "password": "sua_senha"
}
```

**Response (200 OK)**:
```json
{
  "ok": true,
  "user": "seu_usuario",
  "access_token": "eyJhbGc...",
  "refresh_token": "eyJhbGc...",
  "expires_in": 3600
}
```

**Response (401 Unauthorized)**:
```json
{
  "ok": false,
  "error": "Credenciais inválidas. Verifique usuário e senha."
}
```

---

### POST `/auth/refresh`

**Descrição**: Renova o access token usando o refresh token.

**Request**:
```json
{
  "refresh_token": "eyJhbGc..."
}
```

**Response (200 OK)**:
```json
{
  "ok": true,
  "access_token": "eyJhbGc...",
  "expires_in": 3600
}
```

**Response (401 Unauthorized)**:
```json
{
  "ok": false,
  "error": "Refresh token inválido ou expirado"
}
```

---

### GET `/auth/status`

**Descrição**: Verifica se há uma sessão ativa (requer JWT no header).

**Request Header**:
```
Authorization: Bearer eyJhbGc...
```

**Response (200 OK - Autenticado)**:
```json
{
  "authenticated": true,
  "user": "seu_usuario",
  "timestamp": 1711650000
}
```

**Response (200 OK - Não Autenticado)**:
```json
{
  "authenticated": false
}
```

---

### POST `/auth/logout`

**Descrição**: Faz logout (limpa token no servidor).

**Request Header**:
```
Authorization: Bearer eyJhbGc...
```

**Response (200 OK)**:
```json
{
  "ok": true
}
```

---

## Como Usar no Frontend

### 1. Fazer Login

```javascript
fetch('/auth/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ 
    username: 'seu_usuario',
    password: 'sua_senha'
  })
})
.then(res => res.json())
.then(data => {
  if (data.ok) {
    authAccessToken = data.access_token;
    authRefreshToken = data.refresh_token;
    authTokenExpiry = Date.now() + (data.expires_in * 1000);
    console.log('Login bem-sucedido!');
  } else {
    console.error(data.error);
  }
});
```

### 2. Fazer Requisições Autenticadas

Adicione o header `Authorization: Bearer <token>` em todas as requisições:

```javascript
fetch('/proxy/api/now/table/incident?...', {
  method: 'GET',
  headers: {
    'Authorization': 'Bearer ' + authAccessToken,
    'Accept': 'application/json'
  }
})
.then(res => {
  if (res.status === 401) {
    // Token expirou — renovar
    return refreshAccessToken().then(() => {
      // Retenta com novo token
      return fetch(...);
    });
  }
  return res.json();
});
```

### 3. Renovar Token Automaticamente

```javascript
function refreshAccessToken() {
  return fetch('/auth/refresh', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ refresh_token: authRefreshToken })
  })
  .then(res => res.json())
  .then(data => {
    if (data.ok) {
      authAccessToken = data.access_token;
      authTokenExpiry = Date.now() + (data.expires_in * 1000);
      return true;
    }
    return false;
  });
}
```

### 4. Fazer Logout

```javascript
fetch('/auth/logout', {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer ' + authAccessToken
  }
})
.then(() => {
  authAccessToken = null;
  authRefreshToken = null;
  console.log('Desconectado com sucesso!');
});
```

---

## Estrutura de JWT

Um JWT típico tem 3 partes separadas por `.`:

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.
eyJzdWIiOiJ1c3VhcmlvIiwiaWF0IjoxNzExNjUwMDAwLCJleHAiOjE3MTE2NTM2MDAsInR5cGUiOiJhY2Nlc3MifQ.
abcdef123456...
```

**Header** (decodificado):
```json
{
  "alg": "HS256",
  "typ": "JWT"
}
```

**Payload** (decodificado):
```json
{
  "sub": "usuario",      // Subject (username)
  "iat": 1711650000,     // Issued at
  "exp": 1711653600,     // Expiration
  "type": "access"       // "access" ou "refresh"
}
```

---

## Tratamento de Erros Comuns

| Erro | Causa | Solução |
|------|-------|--------|
| `401 Unauthorized` | Token expirado ou inválido | Use `refreshAccessToken()` ou faça login novamente |
| `403 Forbidden` | Token válido mas sem permissão | Verifique permissões do usuário no ServiceNow |
| `502 Bad Gateway` | Erro ao proxiar para ServiceNow | Verifique conexão com `SERVICENOW_BASE` |
| `CORS error` | Origin não permitido | Configure `ALLOWED_ORIGINS` em `server.py` |

---

## Segurança

### Boas Práticas

1. **Nunca exponha `JWT_SECRET`** — Mantenha em `.env` (não commit no git)
2. **Use HTTPS em produção** — Tokens devem ser transmitidos por TLS
3. **Regenere tokens periodicamente** — Implemente token rotation
4. **Valide sempre no servidor** — Nunca confie apenas em tokens do cliente
5. **Use refresh tokens** — Access tokens curtos (1h) + refresh tokens longos (7d)

### Como Gerar JWT_SECRET Seguro

```bash
# Python 3.6+
python -c "import secrets; print(secrets.token_hex(32))"

# Linux/Mac
openssl rand -hex 32
```

---

## Próximas Funcionalidades (Roadmap)

- [ ] Suporte a OAuth2 / Azure AD (SSO)
- [ ] Persistência de sessões (banco SQLite ou Redis)
- [ ] Token rotation automático
- [ ] Rate limiting por usuário
- [ ] Auditoria de login/logout
- [ ] 2FA (Two-Factor Authentication)

---

## Troubleshooting

### "JWT_SECRET é a chave padrão de desenvolvimento"

**Solução**: Edite `.env` com uma chave segura:
```bash
JWT_SECRET=sua_chave_segura_aqui
```

### "Sessão expirada. Faça login novamente."

**Solução**: O refresh token expirou (> 7 dias). Faça login novamente.

### Tokens não estão sendo passados corretamente

**Debug**: Verifique o header `Authorization` nas requisições:
```javascript
console.log('Header:', 'Bearer ' + authAccessToken);
```

---

## Suporte

Para dúvidas ou problemas, verifique:
- [Documentação PyJWT](https://pyjwt.readthedocs.io/)
- [RFC 7519 — JWT](https://tools.ietf.org/html/rfc7519)
- Issues do projeto no GitHub
