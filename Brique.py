"""
Cree une classe Brique pour tkinter.

Hugo SAEZ

08/10/2026

To do :
- outline couleur méthode + appel dans classe partie

"""

class Brique :

    def __init__ (self, canvas, x, y, largeur, hauteur, couleur, nb_vie_brique) :
        """
        Initialise la Brique avec les parametres donnes.
        
        :param: canvas, canvas sur lequel la Brique sera dessinee
        :param: x, position x de la Brique
        :param: y, position y de la Brique
        :param: largeur, largeur de la Brique
        :param: hauteur, hauteur de la Brique
        :param: couleur, couleur de la Brique
        :param: nb_vie_brique, nombre de vies restantes de la Brique
        """

        self.canvas = canvas
        self.x = x
        self.y = y
        self.largeur = largeur
        self.hauteur = hauteur
        self.couleur = couleur
        self.nb_vie_brique = nb_vie_brique

    def dessin(self):
        """
        Cree le rectangle qui represente la Brique sur le canvas
        
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


    def stats_brq (self) :
            """
            Retourne les statistiques visuelles de la raquette
    
            :return: largeur, hauteur, couleur
            """
    
            return self.largeur, self.hauteur, self.couleur

    def vie_brq (self) :
          """
          Retourne le nombre de vies restantes de la brique
          
          :return: nb_vie_brique
          """

          return self.nb_vie_brique