from flask import Blueprint
from app.controllers.document_livreur_controller import (
    creer_document,
    liste_documents,
    document_par_id,
    modifier_document,
    supprimer_document,
)

document_livreur_bp = Blueprint("document_livreur_bp", __name__)

document_livreur_bp.route("/", methods=["POST"])(creer_document)
document_livreur_bp.route("/", methods=["GET"])(liste_documents)
document_livreur_bp.route("/<id_document>", methods=["GET"])(document_par_id)
document_livreur_bp.route("/<id_document>", methods=["PUT"])(modifier_document)
document_livreur_bp.route("/<id_document>", methods=["DELETE"])(supprimer_document)
