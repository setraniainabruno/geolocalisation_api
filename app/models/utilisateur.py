from mongoengine import Document, StringField, DateTimeField, BooleanField
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


class Utilisateur(Document):
    id_user = StringField(primary_key=True)
    nom = StringField(required=True)
    prenom = StringField(required=True)
    email = StringField(required=True, unique=True)
    _mot_de_passe = StringField(required=True)
    role = StringField(required=True, choices=["Admin", "Livreur", "Client"])
    telephone = StringField()
    photo_profil = StringField()
    statut = BooleanField(default=True)
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)

    meta = {"collection": "utilisateurs"}

    @property
    def mot_de_passe(self):
        raise AttributeError("Le mot de passe ne peut pas être lu directement.")

    @mot_de_passe.setter
    def password(self, mot_de_passe):
        self._mot_de_passe = generate_password_hash(mot_de_passe)

    def check_password(self, mot_de_passe):
        return check_password_hash(self._mot_de_passe, mot_de_passe)

    def to_json(self, include_child=True):
        data = {
            "id_user": self.id_user,
            "nom": self.nom,
            "prenom": self.prenom,
            "email": self.email,
            "role": self.role,
            "telephone": self.telephone,
            "photo_profil": self.photo_profil,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

        if include_child:
            if self.role == "Admin":
                from app.models.admin import Admin

                admin = Admin.objects(utilisateur=self).first()
                if admin:
                    data["admin"] = admin.to_json()
            elif self.role == "Livreur":
                from app.models.livreur import Livreur

                livreur = Livreur.objects(utilisateur=self).first()
                if livreur:
                    data["livreur"] = livreur.to_json()
            elif self.role == "Client":
                from app.models.client import Client

                client = Client.objects(utilisateur=self).first()
                if client:
                    data["client"] = client.to_json()

        return data

    def save(self, *args, **kwargs):
        self.updated_at = datetime.utcnow()
        return super(Utilisateur, self).save(*args, **kwargs)
