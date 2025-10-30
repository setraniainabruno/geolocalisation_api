import os
import uuid
from datetime import datetime
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.document_livreur import DocumentLivreur
from app.models.livreur import Livreur

UPLOAD_FOLDER = "uploads/documents_livreurs"

# Assure que le dossier d’upload existe
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@jwt_required()
def creer_document():
    current_user = get_jwt_identity()

    try:
        type_document = request.form.get("type_document")
        date_expiration = request.form.get("date_expiration")
        id_livreur = request.form.get("id_livreur")
        fichier = request.files.get("fichier_document")

        if not all([type_document, date_expiration, id_livreur, fichier]):
            return jsonify({"error": "Champs manquants"}), 400

        livreur = Livreur.objects(id_livreur=id_livreur).first()
        if not livreur:
            return jsonify({"error": "Livreur introuvable"}), 404

        # Sauvegarde du fichier
        filename = f"{uuid.uuid4()}_{fichier.filename}"
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        fichier.save(filepath)

        doc = DocumentLivreur(
            id_document=str(uuid.uuid4()),
            type_document=type_document,
            fichier_document=filepath,
            date_expiration=datetime.strptime(date_expiration, "%Y-%m-%d"),
            livreur=livreur,
        )
        doc.save()

        return jsonify({"message": "Document ajouté", "document": doc.to_json()}), 201

    except Exception as e:
        return jsonify({"message": f"Erreur : {e}"}), 500


@jwt_required()
def liste_documents():
    docs = DocumentLivreur.objects()
    return jsonify([d.to_json() for d in docs]), 200


@jwt_required()
def document_par_id(id_document):
    doc = DocumentLivreur.objects(id_document=id_document).first()
    if not doc:
        return jsonify({"error": "Document non trouvé"}), 404
    return jsonify(doc.to_json()), 200


@jwt_required()
def modifier_document(id_document):
    try:
        doc = DocumentLivreur.objects(id_document=id_document).first()
        if not doc:
            return jsonify({"error": "Document non trouvé"}), 404

        type_document = request.form.get("type_document", doc.type_document)
        date_expiration = request.form.get("date_expiration")
        fichier = request.files.get("fichier_document")

        # Mettre à jour les champs
        doc.type_document = type_document
        if date_expiration:
            doc.date_expiration = datetime.strptime(date_expiration, "%Y-%m-%d")

        # Si un nouveau fichier est uploadé
        if fichier:
            # Supprimer l’ancien fichier
            if os.path.exists(doc.fichier_document):
                os.remove(doc.fichier_document)

            filename = f"{uuid.uuid4()}_{fichier.filename}"
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            fichier.save(filepath)
            doc.fichier_document = filepath

        doc.save()
        return jsonify(doc.to_json()), 200
    except Exception as e:
        return jsonify({"message": f"Erreur : {e}"}), 500


@jwt_required()
def supprimer_document(id_document):
    doc = DocumentLivreur.objects(id_document=id_document).first()
    if not doc:
        return jsonify({"error": "Document non trouvé"}), 404

    # Supprimer le fichier du disque
    if os.path.exists(doc.fichier_document):
        os.remove(doc.fichier_document)

    doc.delete()
    return jsonify({"message": "Document supprimé avec succès"}), 200
