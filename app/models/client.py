from mongoengine import Document, StringField, ReferenceField, CASCADE


class Client(Document):
    id_client = StringField(primary_key=True)
    utilisateur = ReferenceField(
        "Utilisateur", reverse_delete_rule=CASCADE, required=True
    )
    adresse_principale = StringField(default="Non spécifiée")
    ville = StringField(default="Antsirabe")
    code_postal = StringField(default="110")

    meta = {"collection": "clients"}

    def to_json(self):
        return {
            "id_client": self.id_client,
            "adresse_principale": self.adresse_principale,
            "ville": self.ville,
            "code_postal": self.code_postal,
        }

    def get_util(self):
        u = self.utilisateur
        return {
            "nom": u.nom,
            "prenom": u.prenom,
            "email": u.email,
            "role": u.role,
            "telephone": u.telephone,
            "adresse_principale": self.adresse_principale,
            "ville": self.ville,
            "code_postal": self.code_postal,
        }
