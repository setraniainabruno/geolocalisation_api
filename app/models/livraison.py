from mongoengine import Document, ReferenceField, StringField, DateTimeField, CASCADE
from datetime import datetime
from app.models.livreur import Livreur
from app.models.commande import Commande
import uuid


class Livraison(Document):
    id_livraison = StringField(primary_key=True, default=str(uuid.uuid4()))
    date_debut = DateTimeField(default=datetime.utcnow)
    date_fin = DateTimeField(default=datetime.utcnow)
    statut = StringField(
        required=True,
        choices=["En cours", "En attente", "En retard", "Livrée", "Echouée"],
    )
    position_actuelle = StringField()
    commande = ReferenceField(Commande, reverse_delete_rule=CASCADE, required=True)
    livreur = ReferenceField(Livreur, reverse_delete_rule=CASCADE, required=True)
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)

    meta = {"collection": "livraisons"}

    def to_json(self):
        return {
            "id_livraison": str(self.id_livraison),
            "date_debut": self.date_debut,
            "date_fin": self.date_fin,
            "statut": self.statut,
            "position_actuelle": self.position_actuelle,
            "commande": self.commande.to_json(),
            "livreur": self.livreur.get_util(),
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    def reload(self, *fields, **kwargs):
        self.updated_at = datetime.utcnow
        return super().reload(*fields, **kwargs)
