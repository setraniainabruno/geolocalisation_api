from flask import Blueprint
from app.controllers.produit_controller import (
    creer_produit,
    liste_produits,
    produit_par_id,
    modifier_produit,
    supprimer_produit,
)

produit_bp = Blueprint("produit_bp", __name__)

produit_bp.route("/", methods=["POST"])(creer_produit)
produit_bp.route("/", methods=["GET"])(liste_produits)
produit_bp.route("/<id_produit>", methods=["GET"])(produit_par_id)
produit_bp.route("/<id_produit>", methods=["PUT"])(modifier_produit)
produit_bp.route("/<id_produit>", methods=["DELETE"])(supprimer_produit)
