import sys

@@code@@
    
def test_1():
    History = ""
    bibliotheque = Bibliotheque()
    bibliotheque.ajouter_livre("Harry Potter", 3)
    History += "Ajout: Harry Potter =>  3 \n"
    bibliotheque.ajouter_livre("Le Seigneur des Anneaux", 2)
    History += "Ajout: Le Seigneur des Anneaux =>  2 \n"

    assert bibliotheque.emprunter_livre("Harry Potter") == True, f"{History} Erreur: Emprunt Harry Potter retourne False"
    History += "Emprunt: Harry Potter \n"
    assert bibliotheque.emprunter_livre("Le Seigneur des Anneaux") == True, f"{History} Erreur: Emprunt Le Seigneur des Anneaux retourne False"
    History += "Emprunt: Le Seigneur des Anneaux \n"
    bibliotheque.retourner_livre("Harry Potter")
    History += "Retour: Harry Potter \n"

    assert bibliotheque.consulter_disponibilite("Harry Potter") == 3, f"{History} Erreur: 3 exemplaires de Harry Potter attendu mais {bibliotheque.consulter_disponibilite('Harry Potter')} retourné"
    assert bibliotheque.consulter_disponibilite("Le Seigneur des Anneaux") == 1, f"{History} Erreur: 1 exemplaire de Le Seigneur des Anneaux attendu mais {bibliotheque.consulter_disponibilite('Le Seigneur des Anneaux')} retourné"

def test_2():
    bibliotheque = Bibliotheque()
    assert bibliotheque.emprunter_livre("Harry Potter") == False, f"Erreur: Emprunt Harry Potter retourne True alors que le livre n'existe pas"
    assert bibliotheque.consulter_disponibilite("Harry Potter") == 0, f"Erreur: 0 exemplaires de Harry Potter attendu mais {bibliotheque.consulter_disponibilite('Harry Potter')} retourné"
    
if __name__ == "__main__":
    test_1()
    test_2()
    sys.exit(0)