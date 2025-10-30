from mongoengine import Document, StringField, ReferenceField, DateTimeField
from datetime import datetime
from app.models.livreur import Livreur
from mongoengine import CASCADE


class DocumentLivreur(Document):
    id_document = StringField(primary_key=True)
    type_document = StringField(required=True)
    fichier_document = StringField(required=True)
    date_expiration = DateTimeField(required=True)
    livreur = ReferenceField(Livreur, reverse_delete_rule=CASCADE, required=True)
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)

    meta = {"collection": "documents_livreurs"}

    def to_json(self):
        return {
            "id_document": self.id_document,
            "type_document": self.type_document,
            "fichier_document": self.fichier_document,
            "date_expiration": self.date_expiration.strftime("%Y-%m-%d"),
            "livreur": self.livreur.get_util(),
        }

    def save(self, *args, **kwargs):
        self.updated_at = datetime.utcnow()
        return super(DocumentLivreur, self).save(*args, **kwargs)
