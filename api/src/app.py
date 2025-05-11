from os import getenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# Azure Key Vault
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

# Own Modules
from database import db
from routes import api

def get_secret_from_key_vault(vault_url: str, secret_name: str) -> str:
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=vault_url, credential=credential)
    return client.get_secret(secret_name).value

def create_app():
    """
    Create the API with Flask for Chatbot Database
    """
    app = Flask(__name__)

    cors = CORS(app)
    app.config['CORS_HEADERS'] = 'Content-Type'

    vault_url = getenv('AZURE_KEY_VAULT_URL')

    secret_key = get_secret_from_key_vault(vault_url, 'SECRET-KEY')
    db_url = get_secret_from_key_vault(vault_url, 'DATABASE-URL')

    app.config['SECRET_KEY'] = secret_key
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    app.register_blueprint(api, url_prefix='/api')
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)