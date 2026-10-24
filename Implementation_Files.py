"""
Implementation de file, sous forme de classe, a l'aide d'une liste

08/10/2026

SAEZ Hugo, QUESSARD Constantin

To do :

"""

class File:
    """
    Classe representant une pile

    Methodes :
        emfiler(element) : ajoute un element a la fin de la file
        defiler() : retire et retourne l'element en tete de file
        premier() : retourne l'element a la fin de la file sans le retirer
        est_vide() : retourne True si la file est vide, False sinon 
        taille() : retourne le nombre d'elements dans la file    
    """

    def __init__(self):
        """
        Cree une file vide
        """
        self.file = []

    def enfiler(self, element):
        """
        Ajoute un element a la fin de la file

        Args:
            element: objet a placer a la fin de la file

        Returns:
            None
        """
        self.file.append(element)

    def defiler(self):
        """
        Retire et retourne l'element le plus ancien

        Returns:
            element place en tete de file

        Raises:
            IndexError: si la file est vide
        """
        if self.est_vide():
            raise IndexError("La file est vide")
        return self.file.pop(0)

    def premier(self):
        """
        Retourne l'element le plus ancien sans le retirer

        Returns:
            element place en tete de file

        Raises:
            IndexError: si la file est vide
        """
        if self.est_vide():
            raise IndexError("La file est vide")
        return self.file[0]

    def est_vide(self):
        """
        Indique si la file ne contient aucun element

        Returns:
            True si la file est vide, sinon False
        """
        return len(self.file) == 0

    def taille(self):
        """
        Compte le nombre d'elements de la file

        Returns:
            Nombre d'elements de la file
        """
        return len(self.file)
