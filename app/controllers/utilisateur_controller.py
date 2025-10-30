from flask import jsonify, request
from app.models.utilisateur import Utilisateur
from app.models.admin import Admin
from app.models.livreur import Livreur
from app.models.client import Client
import uuid
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity


# Connexion
def connexion():
    data = request.get_json()
    try:
        user = Utilisateur.objects(email=data.get("email")).first()
        if not user or not user.check_password(data.get("mot_de_passe")):
            return jsonify({"error": "Email ou mot de passe incorrect"}), 401

        token = create_access_token(identity=user.id_user)
        return (
            jsonify(
                {
                    "message": "Connexion réussie",
                    "token": token,
                    "role": user.role,
                    "utilisateur": user.to_json(),
                }
            ),
            200,
        )
    except Exception as e:
        return jsonify({"message": f"Erreur : {e}"}), 500


# Création d'un utilisateur
def creer_utilisateur():
    data = request.get_json()

    try:
        champs_requis = ["nom", "prenom", "email", "mot_de_passe", "role"]
        for champ in champs_requis:
            if champ not in data or not data[champ]:
                return jsonify({"error": f"Le champ '{champ}' est requis."}), 400

        role = data["role"]

        if Utilisateur.objects(email=data["email"]).first():
            return jsonify({"error": "Cet email existe déjà."}), 400

        utilisateur = Utilisateur(
            id_user=str(uuid.uuid4()),
            nom=data["nom"],
            prenom=data["prenom"],
            email=data["email"],
            role=role,
            telephone=data.get("telephone"),
        )
        utilisateur.password = data["mot_de_passe"]
        utilisateur.save()

        if role == "Admin":
            Admin(
                id_admin=str(uuid.uuid4()),
                utilisateur=utilisateur,
                poste=data.get("poste", "Manager"),
                niveau_acces=data.get("niveau_acces", 10),
            ).save()

        elif role == "Livreur":
            Livreur(
                id_livreur=str(uuid.uuid4()),
                utilisateur=utilisateur,
                vehicule=data.get("vehicule", "Moto"),
                immatriculation=data.get("immatriculation", "N/A"),
            ).save()

        elif role == "Client":
            Client(
                id_client=str(uuid.uuid4()),
                utilisateur=utilisateur,
                adresse_principale=data.get("adresse_principale", "Non spécifiée"),
                ville=data.get("ville", "Antsirabe"),
                code_postal=data.get("code_postal", "110"),
            ).save()
        else:
            return jsonify({"error": f"Rôle '{role}' invalide."}), 400

        return (
            jsonify(
                {
                    "message": f"{role} créé avec succès.",
                    "utilisateur": utilisateur.to_json(),
                }
            ),
            201,
        )

    except Exception as e:
        return jsonify({"message": f"Erreur : {e}"}), 500


# Recuperation de tous les utilisateurs
@jwt_required()
def liste_utilisateurs():
    # print(get_jwt_identity())
    try:
        utilisateurs = Utilisateur.objects()
        data = [u.to_json(include_child=True) for u in utilisateurs]
        return jsonify({"total": len(data), "data": data}), 200

    except Exception as e:
        return jsonify({"message": f"Erreur : {e}"}), 500


# Recuperation d'un utilisateur par id
@jwt_required()
def utilisateur_par_id(id_user):
    try:
        utilisateur = Utilisateur.objects(id_user=id_user).first()
        if not utilisateur:
            return jsonify({"error": "Utilisateur non trouvé"}), 404

        return jsonify(utilisateur.to_json(include_child=True)), 200
    except Exception as e:
        return jsonify({"message": f"Erreur : {e}"}), 500


# Modification d'un utilisateur
@jwt_required()
def modifier_utilisateur(id_user):
    data = request.get_json()
    try:
        utilisateur = Utilisateur.objects(id_user=id_user).first()
        if not utilisateur:
            return jsonify({"error": "Utilisateur non trouvé"}), 404

        utilisateur.nom = data.get("nom", utilisateur.nom)
        utilisateur.prenom = data.get("prenom", utilisateur.prenom)
        utilisateur.email = data.get("email", utilisateur.email)
        utilisateur.telephone = data.get("telephone", utilisateur.telephone)
        utilisateur.save()

        if utilisateur.role == "Admin":
            admin = Admin.objects(utilisateur=utilisateur).first()
            if not admin:
                admin = Admin(id_admin=str(uuid.uuid4()), utilisateur=utilisateur)
            admin.poste = data.get("poste", admin.poste)
            admin.niveau_acces = data.get("niveau_acces", admin.niveau_acces)
            admin.save()
        elif utilisateur.role == "Livreur":
            livreur = Livreur.objects(utilisateur=utilisateur).first()
            if not livreur:
                livreur = Livreur(id_livreur=str(uuid.uuid4()), utilisateur=utilisateur)
            livreur.vehicule = data.get("vehicule", livreur.vehicule)
            livreur.immatriculation = data.get(
                "immatriculation", livreur.immatriculation
            )
            livreur.disponibilite = data.get("disponibilite", livreur.disponibilite)
            livreur.note_moyenne = data.get("note_moyenne", livreur.note_moyenne)
            livreur.nb_livraisons = data.get("nb_livraisons", livreur.nb_livraisons)
            livreur.save()
        elif utilisateur.role == "Client":
            client = Client.objects(utilisateur=utilisateur).first()
            if not client:
                client = Client(id_client=str(uuid.uuid4()), utilisateur=utilisateur)
            client.adresse_principale = data.get(
                "adresse_principale", client.adresse_principale
            )
            client.ville = data.get("ville", client.ville)
            client.code_postal = data.get("code_postal", client.code_postal)
            client.save()

        return jsonify(utilisateur.to_json(include_child=True)), 200

    except Exception as e:
        return jsonify({"message": f"Erreur : {e}"}), 500


# Modification du mot de passe
@jwt_required()
def modifier_mot_de_passe(id_user):
    data = request.get_json()
    try:
        ancien_mdp = data.get("ancien_mdp")
        nouveau_mdp = data.get("nouveau_mdp")

        if not ancien_mdp or not nouveau_mdp:
            return jsonify({"error": "Ancien et nouveau mot de passe sont requis"}), 400

        utilisateur = Utilisateur.objects(id_user=id_user).first()
        if not utilisateur:
            return jsonify({"error": "Utilisateur non trouvé"}), 404

        if not utilisateur.check_password(ancien_mdp):
            return jsonify({"error": "Ancien mot de passe incorrect"}), 401

        utilisateur.password = nouveau_mdp  # setter hachera le mot de passe
        utilisateur.save()

        return jsonify({"message": "Mot de passe modifié avec succès"}), 200
    except Exception as e:
        return jsonify({"message": f"Erreur : {e}"}), 500


# Suppression d'un utilisateur
@jwt_required()
def supprimer_utilisateur(id_user):
    try:
        utilisateur = Utilisateur.objects(id_user=id_user).first()
        if not utilisateur:
            return jsonify({"error": "Utilisateur non trouvé"}), 404

        utilisateur.delete()

        return jsonify({"message": f"Utilisateur {id_user} supprimé"}), 200
    except Exception as e:
        return jsonify({"message": f"Erreur : {e}"}), 500
