"""
Cree une classe Raquette pour tkinter.

Hugo SAEZ

08/10/2026

To do :
- méthodes permettant de stocker (return) les variables

"""


class Raquette :

    def __init__ (self, canvas, x, y, largeur, hauteur, couleur) :
        """
        Initialise la raquette avec les parametres donnes.
        
        :param: canvas, canvas sur lequel la raquette sera dessinee
        :param: x, position x de la raquette
        :param: y, position y de la raquette
        :param: largeur, largeur de la raquette
        :param: hauteur, hauteur de la raquette
        :param: couleur, couleur de la raquette
        """

        self.canvas = canvas
        self.x = x
        self.y = y
        self.largeur = largeur
        self.hauteur = hauteur
        self.couleur = couleur

    def dessin(self):
        """
        Cree le rectangle qui represente la raquette sur le canvas
        
        :return: None
        """

        self.canvas.create_rectangle(self.x, self.y, self.x + self.largeur, self.y + self.hauteur, fill=self.couleur)


    def canvas (self) :
        """
        Retourne le canvas

        :return: canvas
        """

        return self.canvas

    def pos_xy (self) :
        """
        Retourne les positions x et y de la raquette

        :return: position x, position y
        """

        return self.x, self.y

    def stats_raq (self) :
        """
        Retourne les statistiques visuelles de la raquette

        :return: largeur, hauteur, couleur
        """

        return self.largeur, self.hauteur, self.couleur