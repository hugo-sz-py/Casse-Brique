"""
Implementation des files en POO

08/10/2026

SAEZ Hugo

To do :

"""

class File :
    """
    Classe représentant une file

    Attribut :
        - file : liste, contenant les éléments de la file

    Méthodes :
        - enfiler(element) : ajoute un élément à la fin de la file
        - defiler() : retire et retourne l'élément en tête de la file
        - premier() : retourne l'élément en tête de la file sans le retirer
        - est_vide() : retourne True si la file est vide, sinon False
        - taille() : retourne le nombre d'éléments dans la file
    """


    def __init__(self):
        """
        Initialise une file vide.
        
        :return: None
        """
        self.file = []


    def enfiler(self, liste):
        """
        Ajoute un élément ou une liste d'éléments à la fin de la file.
        
        :param element: élément ou liste d'éléments à ajouter à la file
        :return: None
        """

        for element in liste :
           self.file.append(element)


    def defiler(self):
        """
        Retire et retourne l'élément en tête de la file. Donne une erreur de type IndexError 
        si la file est vide.

        :return: élément en tête de la file
        """
        if self.est_vide():
            raise IndexError("La file est vide")
        return self.file.pop(0)


    def premier(self): 
        """
        Retourne l'élément en tête de la file sans le retirer. Donne une erreur de type IndexError
        si la file est vide.

        :return: élément en tête de la file
        """

        if self.est_vide() :
            raise IndexError("La file est vide")
        return self.file[0]

    
    def est_vide(self):
        """
        Retourne True si la file est vide, sinon False.
        
        :return: bool, True si la file est vide, sinon False"""
        return len(self.file) == 0


    def taille(self):
        """
        Retourne le nombre d'éléments dans la file.
        
        :return: int, nombre d'élements dans la file
        """
        return len(self.file)