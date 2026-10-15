"""
Implementation des piles en POO

08/10/2026

SAEZ Hugo

To do :

"""


class Pile :
    """
    Classe représentant une file
    
    Attribut :
        - pile : liste, contenant les éléments de la pile
    
    Méthodes :
        - empiler(element) : ajoute un élément au sommet de la pile
        - depiler() : retire et retourne l'élément au sommet de la pile
        - sommet() : retourne l'élément au sommet de la pile sans le retirer
        - est_vide() : retourne True si la pile est vide, sinon False
        - taille() : retourne le nombre d'éléments dans la pile
    """

    def __init__(self):
        """
        Initialise une pile vide.

        :return: None
        """
        self.pile = []

    def empiler(self, liste):
        """
        Ajoute un élément ou une liste d'éléments au sommet de la pile.

        :param element: élément ou liste d'éléments à ajouter à la pile
        :return: None
        """

        for element in liste:
            self.pile.insert(0, element)

    def depiler(self):
        """
        Retire et retourne l'élément au sommet de la pile. Donne une erreur de type IndexError
        si la pile est vide.

        :return: élément au sommet de la pile
        """
        if self.est_vide():
            raise IndexError("La pile est vide")
        return self.pile.pop(0)

    def sommet(self):
        """
        Retourne l'élément sommet de la pile sans le retirer. Donne une erreur de type IndexError
        si la pile est vide.

        :return: élément en tête de la pile
        """

        if self.estvide():
            raise IndexError("La pile est vide")
        return self.pile[0]

    def est_vide(self):
        """
        Retourne True si la pile est vide, sinon False.

        :return: bool, True si la pile est vide, sinon False
        """
        return len(self.pile) == 0

    def taille(self):
        """
        Retourne le nombre d'éléments dans la pile.

        :return: int, nombre d'élements dans la pile
        """
        return len(self.pile)