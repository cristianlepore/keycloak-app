from flask import Flask, render_template, session, redirect, url_for
from flask_saml2.sp import ServiceProvider
import os
from dotenv import load_dotenv

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "supersecret")

load_dotenv()

# Configurazione SAML
sp = ServiceProvider(
    config_file=os.path.join(os.path.dirname(__file__), 'saml-config/settings.json')
)
sp.init_app(app)

@app.route("/")
def index():
    user = session.get("user")
    if user:
        return render_template("dashboard.html", user=user)
    return render_template("index.html")

@app.route("/saml/login")
def saml_login():
    return sp.create_login_request(return_to=url_for("saml_acs", _external=True))

@app.route("/saml/acs", methods=["POST"])
def saml_acs():
    auth = sp.get_auth()
    auth.process_response()
    
    if not auth.is_authenticated():
        return redirect("/")
    
    session["user"] = auth.get_attributes()
    return redirect("/")

@app.route("/saml/logout")
def saml_logout():
    session.clear()
    return sp.create_logout_request(return_to=url_for("index", _external=True))

@app.route("/saml/sls")
def saml_sls():
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)
