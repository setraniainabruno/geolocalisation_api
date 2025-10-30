from mongoengine import (
    Document,
    StringField,
    ReferenceField,
    BooleanField,
    FloatField,
    IntField,
    CASCADE,
)



class Livreur(Document):
    id_livreur = StringField(primary_key=True)
    utilisateur = ReferenceField(
        "Utilisateur", reverse_delete_rule=CASCADE, required=True
    )
    vehicule = StringField(default="Moto")
    immatriculation = StringField(default="N/A")
    disponibilite = BooleanField(default=True)
    note_moyenne = FloatField(default=0.0)
    nb_livraisons = IntField(default=0)

    meta = {"collection": "livreurs"}

    def to_json(self):
        return {
            "id_livreur": self.id_livreur,
            "vehicule": self.vehicule,
            "immatriculation": self.immatriculation,
            "disponibilite": self.disponibilite,
            "note_moyenne": self.note_moyenne,
            "nb_livraisons": self.nb_livraisons,
        }

    def get_util(self):
        u = self.utilisateur
        return {
            "nom": u.nom,
            "prenom": u.prenom,
            "email": u.email,
            "role": u.role,
            "telephone": u.telephone,
            "vehicule": self.vehicule,
            "immatriculation": self.immatriculation,
            "disponibilite": self.disponibilite,
            "note_moyenne": self.note_moyenne,
            "nb_livraisons": self.nb_livraisons,
        }
