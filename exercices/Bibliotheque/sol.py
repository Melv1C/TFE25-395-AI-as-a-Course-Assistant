class Bibliotheque:
    def __init__(self):
        self.livres = {}

    def ajouter_livre(self, titre: str, auteur: str, exemplaires: int):
        if titre not in self.livres:
            self.livres[titre] = {"auteur": auteur, "exemplaires": exemplaires}
        else:
            self.livres[titre]["exemplaires"] += exemplaires

    def emprunter_livre(self, titre: str):
        if titre in self.livres and self.livres[titre]["exemplaires"] > 0:
            self.livres[titre]["exemplaires"] -= 1
            print(f"Vous avez emprunté {titre}.")
        else:
            print(f"Le livre {titre} n'est pas disponible.")

    def retourner_livre(self, titre: str):
        if titre in self.livres:
            self.livres[titre]["exemplaires"] += 1
            print(f"Vous avez retourné {titre}.")
        else:
            print(f"Le livre {titre} n'existe pas dans la bibliothèque.")

    def consulter_disponibilite(self, titre: str):
        if titre in self.livres:
            return f"{titre} : {self.livres[titre]['exemplaires']} exemplaire{'s' if self.livres[titre]['exemplaires'] > 1 else ''} disponible{'s' if self.livres[titre]['exemplaires'] > 1 else ''}"
        else:
            return f"Le livre {titre} n'existe pas dans la bibliothèque."
            
# Exemple d'utilisation
bibliotheque = Bibliotheque()
bibliotheque.ajouter_livre("Harry Potter", "J.K. Rowling", 3)
bibliotheque.ajouter_livre("Le Seigneur des Anneaux", "J.R.R. Tolkien", 2)

bibliotheque.emprunter_livre("Harry Potter")
bibliotheque.emprunter_livre("Le Seigneur des Anneaux")
bibliotheque.retourner_livre("Harry Potter")

print(bibliotheque.consulter_disponibilite("Harry Potter"))  # Résultat attendu : 2
print(bibliotheque.consulter_disponibilite("Le Seigneur des Anneaux"))  # Résultat attendu : 1
