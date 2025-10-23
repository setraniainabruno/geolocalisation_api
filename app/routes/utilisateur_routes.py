from flask import Blueprint
from flask_jwt_extended import jwt_required
from app.controllers.utilisateur_controller import (
    creer_utilisateur,
    connexion,
    liste_utilisateurs,
    modifier_utilisateur,
    modifier_mot_de_passe,
    supprimer_utilisateur,
    get_utilisateur,
)

utilisateur_bp = Blueprint("utilisateur_bp", __name__)
# ROUTES PUBLIC
# Route pour l'ajout d'un utilisateur
utilisateur_bp.route("/", methods=["POST"])(creer_utilisateur)

# Route pour la connexion
utilisateur_bp.route("/connexion", methods=["POST"])(connexion)


# ROUTES PROTEGE PAR JWT
# Route pour recupere tous l'utilsateur
utilisateur_bp.route("/", methods=["GET"])(jwt_required()(liste_utilisateurs))

# Route pour recuperer un utilisateur par son id
utilisateur_bp.route("/<id_user>", methods=["GET"])(jwt_required()(get_utilisateur))

# Route pour la modification d'un utilisateur
utilisateur_bp.route("/<id_user>", methods=["PUT"])(
    jwt_required()(modifier_utilisateur)
)

# Route pour modifier le mot de passe
utilisateur_bp.route("/<id_user>/password", methods=["PATCH"])(
    jwt_required()(modifier_mot_de_passe)
)

# Route pour supprimer un utilisateur
utilisateur_bp.route("/<id_user>", methods=["DELETE"])(
    jwt_required()(supprimer_utilisateur)
)
