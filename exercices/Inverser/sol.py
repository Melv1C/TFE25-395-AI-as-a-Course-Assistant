def inverser_mots(phrase: str) -> str:
    # Découper la phrase en une liste de mots
    mots = phrase.split()

    # Inverser l'ordre des mots
    mots_inverses = mots[::-1]

    # Recomposer la phrase
    return ' '.join(mots_inverses)