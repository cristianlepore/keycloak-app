# MyApp - Identity and Access Management
A Flask web application with federated authentication via **Keycloak** and user dashboard.

## 📋 Features
- **Keycloak Authentication**: Login via OpenID Connect
- **User Dashboard**: Profile view after authentication
- **Responsive Design**: Modern and mobile-friendly UI
- **Docker Compose**: Simplified deployment

## 🚀 Quick Start

### Prerequisites
- Docker
- Docker Compose
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
python -m pip install -r requirements.txt
```

### Access
- **App**: http://localhost:5000
- **Keycloak**: http://localhost:8080
  - Username: `admin`
  - Password: `admin`

## 🔄 How to Start the App (Every Time)

Flask runs locally (outside Docker), Keycloak runs inside Docker.

### 1. Start Keycloak
```bash
# From the project root folder
docker-compose up -d

# Verify Keycloak is running
docker-compose ps
```

### 2. Start Flask
```bash
# Activate the virtual environment
source .venv/bin/activate

# Start the app
python app.py
```

### 3. Stop everything
```bash
# Stop Keycloak
docker-compose down

# Deactivate the virtual environment
deactivate
```

## 📁 Project Structure
```
myapp/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── docker-compose.yml     # Keycloak orchestration
├── .venv/                 # Local Python environment (not committed)
├── static/
│   └── style.css         # CSS styles
├── templates/
│   ├── index.html        # Login page
│   └── dashboard.html    # User dashboard
└── README.md             # This file
```

## 🔧 Configuration

### Environment variables
Set these before running Flask if you need custom values:
```bash
export KEYCLOAK_URL=http://localhost:8080
export KEYCLOAK_REALM=demo
export KEYCLOAK_CLIENT_ID=flask-app
export KEYCLOAK_CLIENT_SECRET=my-secret
export FLASK_SECRET_KEY=supersecret
```

### Keycloak Credentials
- **Client ID**: `flask-app`
- **Client Secret**: `my-secret`
- **Realm**: `demo`

## 📝 Authentication Flow
1. User visits http://localhost:5000
2. Clicks "Login with Keycloak"
3. Redirected to Keycloak for authentication
4. Keycloak returns callback with token
5. Session created and dashboard displayed

## 🛠️ Development

### Recreate the virtual environment
```bash
rm -rf .venv
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

### Update dependencies
```bash
source .venv/bin/activate
python -m pip install <package>
pip freeze > requirements.txt
```

## 📦 Dependencies
- `flask` - Web framework
- `authlib` - OpenID Connect authentication
- `requests` - HTTP client

## 📄 License
MIT