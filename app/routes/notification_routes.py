from flask import Blueprint
from app.controllers.notification_controller import (
    creer_notification,
    liste_notifications,
    notification__par_id,
    modifier_notification,
    supprimer_notification,
)

notification_bp = Blueprint("notification_bp", __name__)

# CRUD complet
notification_bp.route("/", methods=["POST"])(creer_notification)
notification_bp.route("/", methods=["GET"])(liste_notifications)
notification_bp.route("/<id_notification>", methods=["GET"])(notification__par_id)
notification_bp.route("/<id_notification>", methods=["PUT"])(modifier_notification)
notification_bp.route("/<id_notification>", methods=["DELETE"])(supprimer_notification)
