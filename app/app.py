from flask import Flask, redirect, url_for, session, render_template
from authlib.integrations.flask_client import OAuth
import os

app = Flask(__name__)
app.secret_key = "supersecret"

oauth = OAuth(app)
keycloak = oauth.register(
    name="keycloak",
    client_id="flask-app",
    client_secret="my-secret",
    server_metadata_url="http://localhost:8080/realms/demo/.well-known/openid-configuration",
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
    return redirect("/")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
