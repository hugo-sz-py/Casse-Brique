"""Implémentation d'une file FIFO à l'aide d'une liste Python."""


class File:
    """Structure FIFO (premier entré, premier sorti).

    Les éléments sont stockés dans ``file`` du plus ancien au plus récent.
    Chaque appel à ``enfiler`` ajoute un seul objet, qui peut lui-même être
    une liste ou un autre conteneur.
    """

    def __init__(self):
        """Crée une file vide."""
        self.file = []

    def enfiler(self, element):
        """Ajoute un élément à la fin de la file.

        Args:
            element: objet à placer dans la file.

        Returns:
            None.
        """
        self.file.append(element)

    def defiler(self):
        """Retire et retourne l'élément le plus ancien.

        Returns:
            Élément placé en tête de file.

        Raises:
            IndexError: si la file est vide.
        """
        if self.est_vide():
            raise IndexError("La file est vide")
        return self.file.pop(0)

    def premier(self):
        """Retourne l'élément le plus ancien sans le retirer.

        Returns:
            Élément placé en tête de file.

        Raises:
            IndexError: si la file est vide.
        """
        if self.est_vide():
            raise IndexError("La file est vide")
        return self.file[0]

    def est_vide(self):
        """Indique si la file ne contient aucun élément.

        Returns:
            ``True`` si la file est vide, sinon ``False``.
        """
        return len(self.file) == 0

    def taille(self):
        """Compte les éléments actuellement dans la file.

        Returns:
            Nombre d'éléments de la file.
        """
        return len(self.file)
