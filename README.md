# MyApp - Identity and Access Management

A hands-on learning project to understand **OAuth2**, **OpenID Connect (OIDC)**, and **Identity Management** using Flask, Keycloak, and Authlib.

---

## 📋 What This Project Does

This project demonstrates the full OAuth2 + OIDC authentication flow with a real Identity Provider (Keycloak). It includes:

- **Flask Client App** (`app.py`) — the OAuth2 client that authenticates users via Keycloak
- **Flask Resource Server** (`api.py`) — a protected API that validates tokens before serving data
- **Keycloak** — the Authorization Server and Identity Manager, running in Docker

### Features

- Login via OpenID Connect (Authorization Code Flow)
- JWT token inspection (access token, id token, refresh token)
- Self-registration (users can register themselves via Keycloak)
- Protected API endpoint that validates Bearer tokens
- Logout that terminates both the Flask session and the Keycloak session

---

## 🏗️ Architecture

```
Browser
   │
   ▼
app.py (Flask — OAuth2 Client)        ◄──── port 5000
   │                  │
   │ serves HTML      │ exchanges authorization code for token (server-to-server)
   │                  │
   ▼                  ▼
api.py (Resource Server)    Keycloak (Authorization Server)
port 5001                   port 8080
   │                              │
   └── validates token ──────────►│
```

### OAuth2 Roles

| Role | Who | What it does |
|---|---|---|
| Resource Owner | The user | Wants to access the app |
| Client | `app.py` (Flask) | Requests authentication, holds the token |
| Authorization Server | Keycloak | Verifies identity, issues JWT tokens |
| Resource Server | `api.py` (Flask) | Serves protected data, validates tokens |

---

## 🔐 Authentication Flow (Authorization Code Flow)

```
1. Browser  → GET /login                    → Flask
2. Flask    → redirect to Keycloak          →
3.          ← Keycloak login page           ←
4. User enters credentials on Keycloak
5.          → POST credentials              → Keycloak
6.          ← redirect /callback?code=xxx   ←
7. Browser  → GET /callback?code=xxx        → Flask
8. Flask    → POST /token (code + secret)   → Keycloak  (server-to-server, invisible to browser)
9.          ←  access_token + id_token      ←
10. Flask saves tokens in session (encrypted cookie)
11. Browser ← dashboard                     ←
```

The **token never passes through the browser** — it is exchanged directly between Flask and Keycloak. The browser only receives an encrypted session cookie.

---

## 🗂️ Project Structure

```
myapp/
├── app/
│   ├── app.py              # Flask OAuth2 client — login, callback, dashboard, logout
│   ├── api.py              # Flask Resource Server — protected API, validates tokens
│   ├── requirements.txt    # Python dependencies
│   ├── static/
│   │   └── style.css       # CSS styles
│   └── templates/
│       ├── index.html      # Login page
│       └── dashboard.html  # User dashboard
├── docker-compose.yml      # Keycloak (runs in Docker)
├── .venv/                  # Local Python environment (not committed)
└── README.md               # This file
```

---

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose
- Python 3.x

### Installation

```bash
# Clone the repository
git clone <repo-url>
cd myapp

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
python -m pip install -r app/requirements.txt
```

### Keycloak Setup (first time only)

1. Start Keycloak: `docker-compose up -d`
2. Open http://localhost:8080 → Administration Console
3. Login with `admin` / `admin`
4. Create a Realm named `demo`
5. Create a Client:
   - Client ID: `flask-app`
   - Client authentication: ON
   - Valid redirect URIs: `http://localhost:5000/*`
   - Web origins: `http://localhost:5000`
6. Copy the **Client Secret** from the Credentials tab
7. Create a User (Users → Create new user), set a password in the Credentials tab with Temporary: OFF
8. Optionally enable self-registration: Realm Settings → Login → User registration: ON

---

## 🔄 How to Start the App

Flask runs **outside Docker**. Keycloak runs **inside Docker**.

### 1. Start Keycloak

```bash
docker-compose up -d
docker-compose ps   # verify it's running
```

### 2. Set environment variables

```bash
export KEYCLOAK_URL=http://localhost:8080
export KEYCLOAK_REALM=demo
export KEYCLOAK_CLIENT_ID=flask-app
export KEYCLOAK_CLIENT_SECRET=<your-secret-from-keycloak>
export FLASK_SECRET_KEY=supersecret
```

> Tip: put these in a `.env` file and use `python-dotenv` to load them automatically.

### 3. Start the Flask client (app.py)

```bash
source .venv/bin/activate
cd app
python app.py
```

### 4. Start the Resource Server (api.py)

Open a second terminal:

```bash
source .venv/bin/activate
cd app
python api.py
```

### 5. Stop everything

```bash
docker-compose down   # stop Keycloak
deactivate            # deactivate virtualenv
```

---

## 🌐 Access

| Service | URL |
|---|---|
| Flask app | http://localhost:5000 |
| Resource Server API | http://localhost:5001/api/profile |
| Keycloak admin | http://localhost:8080 |

Keycloak credentials: `admin` / `admin`

---

## 🔍 Debug Routes

These routes are useful for learning and debugging:

| Route | What it shows |
|---|---|
| `/token` | Decoded userinfo from the session |
| `/accesstoken` | Raw access token (JWT string) |
| `/tokens` | All three tokens: access, refresh, id |
| `/protected` | Calls the Resource Server with the token |

---

## 🧪 Token Structure

After login, Flask holds three tokens in the session:

| Token | Purpose | Default lifetime |
|---|---|---|
| `access_token` | Proves identity to Resource Servers | 5 minutes |
| `refresh_token` | Gets a new access token without re-login | 30 minutes |
| `id_token` | Contains user claims (name, email, sub) | 5 minutes |

Paste any token at https://jwt.io to inspect its claims (`sub`, `iat`, `exp`, `iss`, etc.).

---

## 🔧 Development

### Recreate the virtual environment

```bash
rm -rf .venv
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r app/requirements.txt
```

### Update dependencies

```bash
source .venv/bin/activate
python -m pip install <package>
pip freeze > app/requirements.txt
```

---

## 📦 Dependencies

- `flask` — Web framework
- `authlib` — OAuth2 and OpenID Connect client implementation
- `requests` — HTTP client (used by the Resource Server to validate tokens)
- `python-dotenv` — Load environment variables from `.env` file

---

## 📄 License

MIT