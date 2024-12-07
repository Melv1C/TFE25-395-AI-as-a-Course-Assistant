def compter_batiments_visibles(hauteurs):
    max_hauteur = 0
    visibles = 0

    for hauteur in hauteurs:
        if hauteur > max_hauteur:
            visibles += 1
            max_hauteur = hauteur

    return visibles