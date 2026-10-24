"""
Implementation de pile, sous forme de classe, à l'aide d'une liste

08/10/2026

SAEZ Hugo, QUESSARD Constantin

To do :

"""

class Pile:
    """
    Classe representant une pile
    
    Attributs :
        pile : liste, contenant les elements de la pile
    
    Methodes :
        empiler(element) : ajoute un element au sommet de la pile
        depiler() : retire et retourne l'element au sommet de la pile
        sommet() : retourne l'element au sommet de la pile sans le retirer
        est_vide() : retourne True si la pile est vide, False sinon 
        taille() : retourne le nombre d'elements dans la pile
    """

    def __init__(self):
        """
        Cree une pile vide
        """
        self.pile = []

    def empiler(self, element):
        """
        Place un element au sommet de la pile

        Args:
            element: objet à placer au sommet

        Returns:
            None
        """
        self.pile.insert(0, element)

    def depiler(self):
        """
        Retire et retourne l'element au sommet de la pile

        Returns:
            element situe au sommet

        Raises:
            IndexError: si la pile est vide
        """
        if self.est_vide():
            raise IndexError("La pile est vide")
        return self.pile.pop(0)

    def sommet(self):
        """
        Retourne l'element au sommet sans le retirer

        Returns:
            element situe au sommet

        Raises:
            IndexError: si la pile est vide
        """
        if self.est_vide():
            raise IndexError("La pile est vide")
        return self.pile[0]

    def est_vide(self):
        """
        Indique si la pile ne contient aucun element

        Returns:
            True si la pile est vide, sinon False
        """
        return len(self.pile) == 0

    def taille(self):
        """
        Compte le nombre d'elements dans la pile

        Returns:
            Nombre d'elements de la pile
        """
        return len(self.pile)
