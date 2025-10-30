from flask import jsonify, request
from app.models.notification import Notification
from app.models.utilisateur import Utilisateur
from mongoengine.errors import DoesNotExist, ValidationError
import uuid
from flask_jwt_extended import jwt_required


# 🔹 Créer une notification


def creer_notification():
    try:
        data = request.get_json()
        user = Utilisateur.objects(id_user=data.get("id_user")).first()
        if not user:
            return jsonify({"message": "Utilisateur non trouvé"}), 404

        notification = Notification(
            id_notification=str(uuid.uuid4()),
            utilisateur=user,
            titre=data.get("titre"),
            message=data.get("message"),
            type=data.get("type"),
            statut=data.get("statut", "Non lu"),
        )
        notification.save()
        return (
            jsonify(
                {
                    "message": "Notification créée avec succès",
                    "data": notification.to_json(),
                }
            ),
            201,
        )

    except ValidationError as e:
        return jsonify({"message": f"Erreur de validation : {e}"}), 400
    except Exception as e:
        return jsonify({"message": f"Erreur interne : {e}"}), 500


# 🔹 Lister toutes les notifications
@jwt_required()
def liste_notifications():
    notifications = Notification.objects()
    return jsonify([n.to_json() for n in notifications]), 200


# 🔹 Récupérer une notification par ID
def notification__par_id(id_notification):
    try:
        notification = Notification.objects.get(id_notification=id_notification)
        return jsonify(notification.to_json()), 200
    except DoesNotExist:
        return jsonify({"message": "Notification non trouvée"}), 404
    except Exception as e:
        return jsonify({"message": f"Erreur : {e}"}), 500


# 🔹 Mettre à jour une notification
def modifier_notification(id_notification):
    try:
        data = request.get_json()
        notification = Notification.objects.get(id_notification=id_notification)

        notification.update(
            titre=data.get("titre", notification.titre),
            message=data.get("message", notification.message),
            type=data.get("type", notification.type),
            statut=data.get("statut", notification.statut),
        )
        notification.reload()
        return (
            jsonify(
                {
                    "message": "Notification mise à jour",
                    "data": Notification.objects.get(
                        id_notification=id_notification
                    ).to_json(),
                }
            ),
            200,
        )
    except DoesNotExist:
        return jsonify({"message": "Notification non trouvée"}), 404

    except Exception as e:
        return jsonify({"message": f"Erreur : {e}"}), 500


# 🔹 Supprimer une notification
def supprimer_notification(id_notification):
    try:
        notification = Notification.objects.get(id_notification=id_notification)
        notification.delete()
        return jsonify({"message": "Notification supprimée avec succès"}), 200
    except DoesNotExist:
        return jsonify({"message": "Notification non trouvée"}), 404
    except Exception as e:
        return jsonify({"message": f"Erreur : {e}"}), 500
