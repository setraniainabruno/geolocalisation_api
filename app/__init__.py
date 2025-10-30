from flask import Flask, Blueprint
from flask_cors import CORS
from dotenv import load_dotenv
from mongoengine import connect
import os
from flask_jwt_extended import JWTManager
from app.routes.utilisateur_routes import utilisateur_bp
from app.routes.document_livreur_routes import document_livreur_bp
from app.routes.notification_routes import notification_bp
from app.routes.produit_routes import produit_bp
from app.routes.commande_routes import commande_bp
from app.routes.livraison_routes import livraison_bp


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
    app.register_blueprint(document_livreur_bp, url_prefix="/api/documentlivreurs")
    app.register_blueprint(notification_bp, url_prefix="/api/notifications")
    app.register_blueprint(produit_bp, url_prefix="/api/produits")
    app.register_blueprint(commande_bp, url_prefix="/api/commandes")
    app.register_blueprint(livraison_bp, url_prefix="/api/livraisons")

    return app
