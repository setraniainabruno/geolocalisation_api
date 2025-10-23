from flask import Flask, Blueprint
from flask_cors import CORS
from dotenv import load_dotenv
from mongoengine import connect
import os
from flask_jwt_extended import JWTManager
from app.routes.utilisateur_routes import utilisateur_bp


def create_app():
    load_dotenv()
    app = Flask(__name__)
    CORS(app)

    # Configuration
    app.config["DEBUG"] = os.getenv("FLASK_DEBUG")
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

    # Connexion MongoDB via URI
    connect(host=os.getenv("MONGO_URI"))

    # JWT
    jwt = JWTManager(app)

    index = Blueprint("index_bp", __name__)

    @index.route("/")
    def serveur() -> str:
        return "Serveur marche bien"

    # Routes
    app.register_blueprint(index, url_prefix="/")

    app.register_blueprint(utilisateur_bp, url_prefix="/api/utilisateurs")

    return app
