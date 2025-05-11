from os import getenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# Own Modules
from database import db
from routes import api

def create_app():
    """
    Create the API with Flask for Chatbot Database
    """
    app = Flask(__name__)
    app.config['SECRET_KEY'] = getenv('SECRET_KEY')


    cors = CORS(app)
    app.config['CORS_HEADERS'] = 'Content-Type'

    SQLALCHEMY_DATABASE_URI = getenv('DATABASE_URL')

    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    app.register_blueprint(api, url_prefix='/api')
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)