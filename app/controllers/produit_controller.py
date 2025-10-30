import os
from flask import request, jsonify
from app.models.produit import Produit
from flask_jwt_extended import jwt_required, get_jwt_identity
from mongoengine.errors import DoesNotExist
import uuid

UPLOAD_FOLDER = "uploads/images_produits"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@jwt_required()
def creer_produit():
    try:
        nom_produit = request.form.get("nom_produit")
        description = request.form.get("description", "")
        prix = request.form.get("prix")
        poids = request.form.get("poids", "")
        fichier = request.files.get("fichier_produit")

        if not all([nom_produit, prix, poids, fichier]):
            return jsonify({"error": "Champs requis manquants"}), 400

        filename = f"{uuid.uuid4()}_{fichier.filename}"
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        fichier.save(filepath)
        print(filepath)
        produit = Produit(
            id_produit=str(uuid.uuid4()),
            nom_produit=nom_produit,
            fichier_produit=filepath,
            description=description,
            prix=prix,
            poids=poids,
        )
        produit.save()
        return (
            jsonify(
                {"message": "Produit créé avec succès", "produit": produit.to_json()}
            ),
            201,
        )

    except Exception as e:
        return jsonify({"message": f"Erreur : {e}"}), 500


@jwt_required()
def liste_produits():
    try:
        produits = Produit.objects()
        return jsonify([p.to_json() for p in produits]), 200
    except Exception as e:
        return jsonify({"message": f"Erreur : {e}"}), 500


@jwt_required()
def produit_par_id(id_produit):
    try:
        produit = Produit.objects.get(id_produit=id_produit)
        return jsonify(produit.to_json()), 200
    except DoesNotExist:
        return jsonify({"error": "Produit introuvable"}), 404
    except Exception as e:
        return jsonify({"message": f"Erreur : {e}"}), 500


@jwt_required()
def modifier_produit(id_produit):
    try:
        data = request.form
        produit = Produit.objects.get(id_produit=id_produit)

        fichier = request.files.get("fichier_produit")
        if fichier:
            if os.path.exists(produit.fichier_produit):
                os.remove(produit.fichier_produit)
            filename = f"{uuid.uuid4()}_{fichier.filename}"
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            fichier.save(filepath)

        produit.update(
            nom_produit=data.get("nom_produit", produit.nom_produit),
            fichier_produit=filepath if fichier else produit.fichier_produit,
            description=data.get("description", produit.description),
            prix=data.get("prix", produit.prix),
            poids=data.get("poids", produit.poids),
        )
        produit.reload()
        return (
            jsonify(
                {
                    "message": "Produit mis à jour",
                    "produit": Produit.objects.get(id_produit=id_produit).to_json(),
                }
            ),
            200,
        )
    except DoesNotExist:
        return jsonify({"error": "Produit introuvable"}), 404
    except Exception as e:
        return jsonify({"message": f"Erreur : {e}"}), 500


@jwt_required()
def supprimer_produit(id_produit):
    try:
        produit = Produit.objects.get(id_produit=id_produit)
        produit.delete()
        return jsonify({"message": "Produit supprimé avec succès"}), 200
    except DoesNotExist:
        return jsonify({"error": "Produit introuvable"}), 404
    except Exception as e:
        return jsonify({"message": f"Erreur : {e}"}), 500
