import requests

from flask import Flask, redirect, url_for, session, render_template
from authlib.integrations.flask_client import OAuth
import os
from authlib.jose import jwt as jose_jwt

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "supersecret")

oauth = OAuth(app)

# Configurazione Keycloak da variabili ambiente
KEYCLOAK_URL = os.getenv("KEYCLOAK_URL", "http://localhost:8080")
KEYCLOAK_REALM = os.getenv("KEYCLOAK_REALM", "demo")
KEYCLOAK_CLIENT_ID = os.getenv("KEYCLOAK_CLIENT_ID", "myapp")
KEYCLOAK_CLIENT_SECRET = os.getenv("KEYCLOAK_CLIENT_SECRET", "my-secret")

keycloak = oauth.register(
    name="keycloak",
    client_id=KEYCLOAK_CLIENT_ID,
    client_secret=KEYCLOAK_CLIENT_SECRET,
    server_metadata_url=f"{KEYCLOAK_URL}/realms/{KEYCLOAK_REALM}/.well-known/openid-configuration",
    client_kwargs={"scope": "openid profile email"},
)

@app.route("/")
def index():
    user = session.get("user")
    if user:
        return render_template("dashboard.html", user=user)
    return render_template("index.html")

@app.route("/login")
def login():
    return keycloak.authorize_redirect(redirect_uri=url_for("callback", _external=True))

@app.route("/callback")
def callback():
    token = keycloak.authorize_access_token()
    session["user"] = token["userinfo"]
    session["access_token"] = token.get("access_token")
    session["refresh_token"] = token.get("refresh_token")  # ← aggiungi
    session["id_token"] = token.get("id_token")            # ← aggiungi
    return redirect("/")

@app.route("/logout")
def logout():
    session.clear()
    keycloak_logout_url = (
        f"{KEYCLOAK_URL}/realms/{KEYCLOAK_REALM}/protocol/openid-connect/logout"
        f"?post_logout_redirect_uri=http://localhost:5000"
        f"&client_id={KEYCLOAK_CLIENT_ID}"
    )
    return redirect(keycloak_logout_url)

@app.route("/tokens")
def tokens():
    return {
        "access_token": session.get("access_token"),
        "refresh_token": session.get("refresh_token"),
        "id_token": session.get("id_token"),
    }

@app.route("/protected")
def protected():
    access_token = session.get("access_token")
    if not access_token:
        return redirect("/login")

    response = requests.get(
        "http://localhost:5001/api/profile",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    return response.json()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
