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

### Installation

```bash
# Clone the repository
git clone <repo-url>
cd myapp

# Start the services
docker-compose up
```

### Access

- **App**: http://localhost:5000
- **Keycloak**: http://localhost:8080
  - Username: `admin`
  - Password: `admin`

## 📁 Project Structure

```
myapp/
├── app/
│   ├── app.py                 # Main Flask application
│   ├── requirements.txt       # Python dependencies
│   ├── static/
│   │   └── style.css         # CSS styles
│   └── templates/
│       ├── index.html        # Login page
│       └── dashboard.html    # User dashboard
├── Dockerfile                # Docker image for app
├── docker-compose.yml        # Services orchestration
└── README.md                 # This file
```

## 🔧 Configuration

### Environment variables (docker-compose.yml)

- `FLASK_ENV`: development
- `KEYCLOAK_ADMIN`: admin
- `KEYCLOAK_ADMIN_PASSWORD`: admin

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

### Install dependencies locally

```bash
pip install -r app/requirements.txt
```

### Run app locally

```bash
cd app
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```

## 📦 Dependencies

- `flask` - Web framework
- `authlib` - OpenID Connect authentication
- `requests` - HTTP client

## 📄 License

MIT
