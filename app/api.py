from flask import Flask, jsonify, request
import requests
import os

app = Flask(__name__)

KEYCLOAK_URL = os.getenv("KEYCLOAK_URL", "http://localhost:8080")
KEYCLOAK_REALM = os.getenv("KEYCLOAK_REALM", "demo")

def validate_token(token):
    response = requests.get(
        f"{KEYCLOAK_URL}/realms/{KEYCLOAK_REALM}/protocol/openid-connect/userinfo",
        headers={"Authorization": f"Bearer {token}"}
    )
    return response.json() if response.status_code == 200 else None

@app.route("/api/profile")
def profile():
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"error": "Token mancante"}), 401

    token = auth_header.split(" ")[1]
    userinfo = validate_token(token)

    if not userinfo:
        return jsonify({"error": "Token non valido"}), 401

    return jsonify({
        "message": "Risorsa protetta!",
        "user": userinfo.get("preferred_username"),
        "email": userinfo.get("email")
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)