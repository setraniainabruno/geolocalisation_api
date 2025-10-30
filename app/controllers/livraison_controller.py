from flask import request, jsonify
from flask_jwt_extended import jwt_required
from app.models.livraison import Livraison
from app.models.commande import Commande
from app.models.livreur import Livreur
from mongoengine.errors import DoesNotExist, ValidationError


@jwt_required()
def creer_livraison():
    try:
        data = request.get_json()
        livraison = Livraison(
            date_debut=data.get("date_debut"),
            date_fin=data.get("date_fin"),
            statut=data.get("statut"),
            livreur=data.get("id_livreur"),
            commande=data.get("id_commande"),
        )
        livraison.save()

        return (
            jsonify(
                {"message": "Livraison créée avec succès", "data": livraison.to_json()}
            ),
            201,
        )
    except ValidationError as e:
        return jsonify({"message": f"Erreur de validation : {e}"}), 400
    except Exception as e:
        return jsonify({"message": f"Erreur : {e}"}), 500


@jwt_required()
def liste_livraison():
    try:
        livraisons = Livraison.objects()
        return jsonify([n.to_json() for n in livraisons]), 200
    except Exception as e:
        return jsonify({"message": f"Erreur : {e}"}), 500


@jwt_required()
def livraison_par_id(id_livraison):
    try:
        livraison = Livraison.objects.get(id_livraison=id_livraison)
        return jsonify(livraison.to_json()), 200
    except DoesNotExist:
        return jsonify({"message": "Livraison non trouvée"}), 404
    except Exception as e:
        return jsonify({"message": f"Erreur : {e}"}), 500


@jwt_required()
def modifier_livraison(id_livraison):
    try:
        data = request.get_json()
        livraison = Livraison.objects.get(id_livraison=id_livraison)

        livraison.update(
            date_debut=data.get("date_debut", livraison.date_debut),
            date_fin=data.get("date_fin", livraison.date_fin),
            statut=data.get("statut", livraison.statut),
            livreur=Livreur.objects.get(
                id_livreur=data.get("id_livreur", livraison.livreur.id_livreur)
            ),
            commande=Commande.objects.get(
                id_commande=data.get("id_commande", livraison.commande.id_commande)
            ),
        )

        livraison.reload()

        return (
            jsonify(
                {
                    "message": "Livraison mise a jour",
                    "data": Livraison.objects.get(id_livraison=id_livraison).to_json(),
                }
            ),
            200,
        )
    except DoesNotExist:
        return jsonify({"message": "Livraison non trouvée"}), 404
    except Exception as e:
        return jsonify({"message": f"Erreur : {e}"}), 500


@jwt_required()
def supprimer_livraison(id_livraison):
    try:
        livraison = Livraison.objects.get(id_livraison=id_livraison)
        livraison.delete()
        return jsonify({"message": "Livraison suppromée avec succès"}), 200
    except DoesNotExist:
        return jsonify({"message": "Livraison non trouvée"}), 404
    except Exception as e:
        return jsonify({"message": f"Erreur : {e}"}), 500


def supprimer_toute_livraison():
    livraison = Livraison.objects()
    livraison.delete()
    return jsonify({"message": "Livraison suppromée avec succès"}), 200
