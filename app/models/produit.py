from mongoengine import Document, StringField, DateTimeField
from datetime import datetime


class Produit(Document):
    id_produit = StringField(primary_key=True)
    nom_produit = StringField(required=True)
    fichier_produit = StringField(required=True)
    description = StringField(default="")
    prix = StringField(required=True)
    poids = StringField(required=True)
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)

    meta = {"collection": "produits"}

    def to_json(self):
        return {
            "id_produit": self.id_produit,
            "nom_produit": self.nom_produit,
            "fichier_produit": self.fichier_produit,
            "description": self.description,
            "prix": self.prix,
            "poids": self.poids,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    def reload(self, *args, **kwargs):
        self.updated_at = datetime.utcnow()
        return super(Produit, self).save(*args, **kwargs)
