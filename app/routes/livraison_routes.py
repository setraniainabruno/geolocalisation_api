from flask import Blueprint
from app.controllers.livraison_controller import (
    creer_livraison,
    liste_livraison,
    livraison_par_id,
    modifier_livraison,
    supprimer_livraison,
    supprimer_toute_livraison,
)

livraison_bp = Blueprint("livraison_bp", __name__)

livraison_bp.route("/", methods=["POST"])(creer_livraison)
livraison_bp.route("/", methods=["GET"])(liste_livraison)
livraison_bp.route("/<id_livraison>", methods=["GET"])(livraison_par_id)
livraison_bp.route("/<id_livraison>", methods=["PUT"])(modifier_livraison)
livraison_bp.route("/<id_livraison>", methods=["DELETE"])(supprimer_livraison)
livraison_bp.route("/", methods=["DELETE"])(supprimer_toute_livraison)
