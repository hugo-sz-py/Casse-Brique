"""Implémentation d'une pile LIFO à l'aide d'une liste Python."""


class Pile:
<<<<<<< HEAD
    """
    Classe représentant une pile
    
    Attribut :
        - pile : liste, contenant les éléments de la pile
    
    Méthodes :
        - empiler(element) : ajoute un élément au sommet de la pile
        - depiler() : retire et retourne l'élément au sommet de la pile
        - sommet() : retourne l'élément au sommet de la pile sans le retirer
        - est_vide() : retourne True si la pile est vide, sinon False
        - taille() : retourne le nombre d'éléments dans la pile
=======
    """Structure LIFO (dernier entré, premier sorti).

    Le sommet est conservé à l'indice ``0`` de ``pile``. Chaque appel à
    ``empiler`` place un seul objet au sommet.
>>>>>>> b365c16a828ac35f527615d47872276b41a6abe6
    """

    def __init__(self):
        """Crée une pile vide."""
        self.pile = []

    def empiler(self, element):
<<<<<<< HEAD
        """
        Ajoute un élément au sommet de la pile.

        :param element: élément à ajouter à la pile
        :return: None
=======
        """Place un élément au sommet de la pile.

        Args:
            element: objet à placer au sommet.

        Returns:
            None.
>>>>>>> b365c16a828ac35f527615d47872276b41a6abe6
        """
        self.pile.insert(0, element)

    def depiler(self):
        """Retire et retourne l'élément au sommet de la pile.

        Returns:
            Élément situé au sommet.

        Raises:
            IndexError: si la pile est vide.
        """
        if self.est_vide():
            raise IndexError("La pile est vide")
        return self.pile.pop(0)

    def sommet(self):
        """Retourne l'élément au sommet sans le retirer.

        Returns:
            Élément situé au sommet.

        Raises:
            IndexError: si la pile est vide.
        """
        if self.est_vide():
            raise IndexError("La pile est vide")
        return self.pile[0]

    def est_vide(self):
        """Indique si la pile ne contient aucun élément.

        Returns:
            ``True`` si la pile est vide, sinon ``False``.
        """
        return len(self.pile) == 0

    def taille(self):
        """Compte les éléments actuellement dans la pile.

        Returns:
            Nombre d'éléments de la pile.
        """
        return len(self.pile)
