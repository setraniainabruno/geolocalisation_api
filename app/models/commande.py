from mongoengine import (
    Document,
    StringField,
    ReferenceField,
    DateTimeField,
    IntField,
    CASCADE,
)
from datetime import datetime


class Commande(Document):
    id_commande = StringField(primary_key=True)
    produit = ReferenceField("Produit", reverse_delete_rule=CASCADE, required=True)
    client = ReferenceField("Client", reverse_delete_rule=CASCADE, required=True)
    statut = StringField()
    adresse_livraison = StringField(default="N/A")
    total_prix = IntField(default=0)
    coordonnees_gps = StringField()
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)

    meta = {"collection": "commandes"}

    def to_json(self):
        return {
            "id_commande": self.id_commande,
            "statut": self.statut,
            "adresse_livraison": self.adresse_livraison,
            "total_prix": self.total_prix,
            "coordonnees_gps": self.coordonnees_gps,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "client": self.client.get_util(),
            "produit": self.produit.to_json(),
        }

    def reload(self, *args, **kwargs):
        self.updated_at = datetime.utcnow()
        return super(Commande, self).save(*args, **kwargs)
