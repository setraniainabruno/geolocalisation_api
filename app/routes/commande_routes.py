from flask import Blueprint
from app.controllers.commande_controller import (
    creer_commande,
    liste_commandes,
    commande_par_id,
    modifier_commande,
    supprimer_commande,
)


commande_bp = Blueprint("commande_bp", __name__)


commande_bp.route("/", methods=["POST"])(creer_commande)
commande_bp.route("/", methods=["GET"])(liste_commandes)
commande_bp.route("/<id_commande>", methods=["GET"])(commande_par_id)
commande_bp.route("/<id_commande>", methods=["PUT"])(modifier_commande)
commande_bp.route("/<id_commande>", methods=["DELETE"])(supprimer_commande)
