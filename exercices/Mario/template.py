# template.py

@@code@@


def find_max_coins_solution():
    # Solution correcte (référence)
    personnages_pieces = {}
    max_personnage = ""
    max_pieces = 0

    with open("pieces.txt", "r") as f:
        for line in f:
            line = line.strip()
            if line:
                personnage, pieces = line.split(",")
                pieces = int(pieces)
                personnages_pieces[personnage] = pieces
                if pieces > max_pieces:
                    max_personnage = personnage
                    max_pieces = pieces
                elif pieces == max_pieces and personnage < max_personnage:
                    max_personnage = personnage

    return personnages_pieces, max_personnage, max_pieces


import unittest
class TestFindMaxCoins(unittest.TestCase):

    def test_exemple(self):
        personnages_pieces, max_personnage, max_pieces = find_max_coins()
        personnages_pieces_sol, max_personnage_sol, max_pieces_sol = find_max_coins_solution()
        self.assertEqual(personnages_pieces, personnages_pieces_sol)
        self.assertEqual(max_personnage, max_personnage_sol)
        self.assertEqual(max_pieces, max_pieces_sol)

if __name__ == '__main__':
    unittest.main()
