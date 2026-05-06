# MyApp - Identity and Access Management

A hands-on learning project to understand **OAuth2**, **OpenID Connect (OIDC)**, and **SAML 2.0** authentication using Flask, Keycloak, and modern authentication libraries.

---

## 📋 What This Project Does

This project demonstrates multiple authentication methods with real Identity Providers:

### OIDC Module (`oidc/`)
- **Flask Client App** (`app.py`) — OAuth2/OIDC client that authenticates users via Keycloak
- **Flask Resource Server** (`api.py`) — protected API endpoint that validates JWT Bearer tokens
- Features:
  - Login via OpenID Connect (Authorization Code Flow)
  - JWT token inspection (access token, id token, refresh token)
  - Self-registration support
  - Secure token storage in encrypted session cookies
  - Token refresh mechanism
  - Protected API endpoints

### SAML Module (`saml/`)
- **Flask SAML App** (`app.py`) — SAML 2.0 Service Provider (SP)
- **SAML Configuration** (`saml-config/`) — SP metadata and settings
- Features:
  - SAML 2.0 authentication flow
  - Configurable IdP integration
  - Single Sign-On (SSO) and Single Logout (SLO) support
  - User attribute mapping

### Shared Components
- **Static Files** (`static/`) — CSS and frontend assets
- **Templates** (`templates/`) — HTML pages served by both modules

---

## 🏗️ Architecture

### OIDC Flow
```
Browser
   │
   ▼
oidc/app.py (Flask — OAuth2 Client)        ◄──── port 5000
   │                  │
   │ serves HTML      │ exchanges auth code for JWT (server-to-server)
   │                  │
   ▼                  ▼
oidc/api.py           Keycloak (Authorization Server)
(port 5001)           (port 8080)
   │
   └── validates Bearer token
```

### SAML Flow
```
Browser
   │
   ▼
saml/app.py (Flask — SAML Service Provider)  ◄──── port 5002
   │                  │
   │ serves HTML      │ SAML 2.0 AuthnRequest/Response
   │                  │
   ▼                  ▼
   ├─ static/         IdP (SAML Identity Provider)
   └─ templates/      (e.g., Keycloak, Okta, Azure AD)
```

### Component Overview
| Component | Purpose | Port |
|---|---|---|
| `oidc/app.py` | OIDC client, serves login page | 5000 |
| `oidc/api.py` | Protected API with token validation | 5001 |
| `saml/app.py` | SAML Service Provider | 5002 |
| Keycloak | OAuth2/OIDC/SAML Authorization Server | 8080 |

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
├── oidc/                           # OpenID Connect (OAuth2) module
│   ├── app.py                      # OIDC Client (Flask)
│   └── api.py                      # Resource Server (protected API)
├── saml/                           # SAML 2.0 module
│   ├── app.py                      # SAML Service Provider (Flask)
│   └── saml-config/
│       ├── settings.json           # SAML SP configuration
│       └── advanced_settings.json  # SAML security settings
├── static/                         # Shared static files (CSS, JS, etc.)
│   └── style.css
├── templates/                      # Shared HTML templates
│   ├── index.html                  # Login page
│   └── dashboard.html              # User dashboard
├── requirements.txt                # Unified dependencies
├── docker-compose.yml              # Keycloak container setup
├── .venv/                          # Python virtual environment
└── README.md
```

### Key Points
- **oidc/** and **saml/** are independent modules running on different ports
- **static/** and **templates/** are shared resources used by both modules
- **requirements.txt** contains all dependencies for both modules
- Each module can be run independently

---

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose
- Python 3.8+

### Installation

```bash
# Clone the repository
git clone <repo-url>
cd myapp

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install all dependencies (OIDC + SAML)
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file at the root:

```bash
# Keycloak Configuration
KEYCLOAK_URL=http://localhost:8080
KEYCLOAK_REALM=demo
KEYCLOAK_CLIENT_ID=flask-app
KEYCLOAK_CLIENT_SECRET=<your-client-secret>

# Flask Security
FLASK_SECRET_KEY=your-secret-key-here
```

Alternatively, export them before running the apps:

```bash
export KEYCLOAK_URL=http://localhost:8080
export KEYCLOAK_REALM=demo
export KEYCLOAK_CLIENT_ID=flask-app
export KEYCLOAK_CLIENT_SECRET=<your-client-secret>
export FLASK_SECRET_KEY=supersecret
```

---

## 🔄 How to Start the App

Flask modules run **outside Docker**. Keycloak runs **inside Docker**.

### Step 1: Start Keycloak

```bash
docker-compose up -d
docker-compose ps   # verify it's running
```

### Step 2: Set Environment Variables

```bash
source .venv/bin/activate
export KEYCLOAK_URL=http://localhost:8080
export KEYCLOAK_REALM=demo
export KEYCLOAK_CLIENT_ID=flask-app
export KEYCLOAK_CLIENT_SECRET=<your-secret-from-keycloak>
export FLASK_SECRET_KEY=supersecret
```

> Tip: Add these to `.env` file in the project root and `python-dotenv` will load them automatically.

### Step 3: Configure Keycloak (First Time Only)

1. Open http://localhost:8080 → Administration Console
2. Login with `admin` / `admin`
3. Create a Realm: Click "Master" dropdown → "Create Realm" → Name: `demo`
4. Create OIDC Client:
   - Go to Clients → Create
   - Client ID: `flask-app`
   - Client authentication: **ON**
   - Valid redirect URIs: `http://localhost:5000/callback`
   - Web origins: `http://localhost:5000`
   - Save and copy **Client Secret** from Credentials tab
5. Create a Test User:
   - Users → Create user
   - Username: `testuser`
   - Set password in Credentials tab (Temporary: OFF)
6. Optional - Enable self-registration:
   - Realm Settings → Login → User registration: **ON**

### Step 4: Run OIDC Module (OAuth2/OIDC)

```bash
cd oidc
python app.py           # starts port 5000
```

In another terminal:

```bash
cd oidc
python api.py           # starts port 5001 (resource server)
```

### Step 5: Run SAML Module (Optional, Different Port)

In another terminal:

```bash
cd saml
python app.py           # starts port 5002
```

> Note: SAML module requires additional IdP configuration in Keycloak (SAML realm and client setup)

### Stop Everything

```bash
docker-compose down     # stop Keycloak
deactivate             # deactivate virtualenv
```

---

## 🌐 Access

### OIDC Module
| Service | URL |
|---|---|
| Flask Client App | http://localhost:5000 |
| Resource Server API | http://localhost:5001/api/profile |
| Token endpoint | http://localhost:5001/tokens |

### SAML Module
| Service | URL |
|---|---|
| Flask SAML App | http://localhost:5002 |

### Keycloak Admin
| Service | URL |
|---|---|
| Admin Console | http://localhost:8080 |
| Credentials | `admin` / `admin` |

---

## 🔍 OIDC Module - Debug Routes

These routes are available on the OIDC client (`http://localhost:5000`):

| Route | What it shows |
|---|---|
| `/` | Home page (login status) |
| `/login` | Initiates OAuth2 login flow |
| `/logout` | Clears session and logs out of Keycloak |
| `/tokens` | Returns all three tokens (access, refresh, id) |
| `/protected` | Calls the Resource Server API with the token |

---

## 🧪 OIDC Token Structure

After login, Flask holds three tokens in the session:

| Token | Purpose | Default lifetime |
|---|---|---|
| `access_token` | Proves identity to Resource Servers | 5 minutes |
| `refresh_token` | Gets a new access token without re-login | 30 minutes |
| `id_token` | Contains user claims (name, email, sub) | 5 minutes |

**Inspect tokens** at https://jwt.io to decode claims (`sub`, `iat`, `exp`, `iss`, etc.)

---

## 🔧 Development

### Recreate the virtual environment

```bash
rm -rf .venv
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Update dependencies

```bash
source .venv/bin/activate
pip install <package>
pip freeze > requirements.txt
```

---

## 📦 Dependencies

The `requirements.txt` includes all dependencies for both OIDC and SAML modules:

### OIDC Module Dependencies
- `Flask` — Web framework
- `Authlib` — OAuth2 and OpenID Connect client
- `requests` — HTTP client for API calls
- `python-dotenv` — Environment variable management
- `cryptography` — Token validation and signing
- `python-jose` — JWT and JWS support

### SAML Module Dependencies
- `Flask` — Web framework
- `python-3-saml` — SAML 2.0 implementation
- `lxml` — XML processing
- `python-dotenv` — Environment variable management
- `pytz`, `isodate` — Date/time handling for SAML

### Shared Dependencies
- Core Flask and security libraries
- Database support (SQLAlchemy, Flask-SQLAlchemy)
- Encryption and cryptography libraries

---

## 📄 License

MIT
