from flask import request, jsonify
from app.models.commande import Commande
from app.models.client import Client
from app.models.produit import Produit
from flask_jwt_extended import jwt_required, get_current_user
from mongoengine.errors import DoesNotExist, ValidationError
import uuid


@jwt_required()
def creer_commande():
    try:
        data = request.get_json()
        commande = Commande(
            id_commande=str(uuid.uuid4()),
            client=data.get("id_client"),
            produit=data.get("id_produit"),
            statut=data.get("statut"),
            adresse_livraison=data.get("adresse_livraison", "N/A"),
            total_prix=data.get("total_prix"),
            coordonnees_gps=data.get("coordonnees_gps"),
        )
        commande.save()
        return (
            jsonify(
                {"message": "Commande créée avec succès", "data": commande.to_json()}
            ),
            201,
        )

    except ValidationError as e:
        return jsonify({"message": f"Erreur de validation : {e}"}), 400
    except Exception as e:
        return jsonify({"message": f"Erreur : {e}"}), 500


@jwt_required()
def liste_commandes():
    try:
        commandes = Commande.objects()
        return jsonify([n.to_json() for n in commandes]), 200
    except Exception as e:
        return jsonify({"message": f"Erreur : {e}"}), 500


@jwt_required()
def commande_par_id(id_commande):
    try:
        commande = Commande.objects.get(id_commande=id_commande)
        return jsonify(commande.to_json()), 200
    except DoesNotExist as e:
        return jsonify({"message": "Commande non trouvé"}), 404


@jwt_required()
def modifier_commande(id_commande):
    try:
        data = request.get_json()
        commande = Commande.objects.get(id_commande=id_commande)
        commande.update(
            produit=Produit.objects.get(
                id_produit=data.get("id_produit", commande.produit.id_produit)
            ),
            statut=data.get("statut", commande.statut),
            adresse_livraison=data.get("adresse_livraison", commande.adresse_livraison),
            coordonnees_gps=data.get("coordonnees_gps", commande.coordonnees_gps),
            total_prix=data.get("total_prix"),
        )
        commande.reload()
        return (
            jsonify(
                {
                    "message": "Commande mise à jour",
                    "data": Commande.objects.get(id_commande=id_commande).to_json(),
                }
            ),
            200,
        )
    except DoesNotExist:
        return jsonify({"message": "Commande non trouvé"}), 404
    except Exception as e:
        return jsonify({"message": f"Erreur : {e}"}), 500


@jwt_required()
def supprimer_commande(id_commande):
    try:
        commande = Commande.objects.get(id_commande=id_commande)
        commande.delete()
        return jsonify({"message": "Commande supprimé avec succès"}), 200
    except DoesNotExist:
        return jsonify({"message": "Commande non trouvé"}), 404
    except Exception as e:
        return jsonify({"message": f"Erreur : {e}"}), 500
