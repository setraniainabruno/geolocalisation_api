from mongoengine import (
    Document,
    StringField,
    DateTimeField,
    ReferenceField,
    CASCADE,
)
from datetime import datetime
from app.models.utilisateur import Utilisateur


class Notification(Document):
    id_notification = StringField(primary_key=True)
    utilisateur = ReferenceField(
        Utilisateur, required=True, reverse_delete_rule=CASCADE
    )
    titre = StringField(required=True)
    message = StringField(required=True)
    type = StringField(choices=["Info", "Alerte", "Rappel", "Promotion"], required=True)
    statut = StringField(choices=["Non lu", "Lu"], default="Non lu")
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)

    meta = {"collection": "notifications"}

    def to_json(self):
        user_data = None
        if self.utilisateur:
            user_data = {
                "nom": getattr(self.utilisateur, "nom", None),
                "prenom": getattr(self.utilisateur, "prenom", None),
                "email": getattr(self.utilisateur, "email", None),
                "role": getattr(self.utilisateur, "role", None),
            }

        return {
            "id_notification": str(self.id_notification),
            "titre": self.titre,
            "message": self.message,
            "type": self.type,
            "statut": self.statut,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "utilisateur": user_data,
        }

    def reload(self, *args, **kwargs):
        self.updated_at = datetime.utcnow()
        return super(Notification, self).save(*args, **kwargs)
