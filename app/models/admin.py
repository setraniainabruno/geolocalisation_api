from mongoengine import Document, StringField, ReferenceField, IntField, CASCADE



class Admin(Document):
    id_admin = StringField(primary_key=True)
    utilisateur = ReferenceField(
        'Utilisateur', reverse_delete_rule=CASCADE, required=True
    )
    poste = StringField(default="Manager")  # ou "Superviseur"
    niveau_acces = IntField(default=10)

    meta = {"collection": "admins"}

    def to_json(self):
        return {
            "id_admin": self.id_admin,
            "poste": self.poste,
            "niveau_acces": self.niveau_acces,
        }
