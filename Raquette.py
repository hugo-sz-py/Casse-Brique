"""
Definition de la raquette contrôlee par le joueur

08/10/2026

SAEZ Hugo, QUESSARD Constantin

To do :

"""


class Raquette:
    """
    Decrit la position et l'apparence de la raquette

    Attributs:
        canvas: zone Tkinter ou la raquette sera dessinee
        x: coordonnee horizontale du coin superieur gauche
        y: coordonnee verticale du coin superieur gauche
        largeur: largeur de la raquette en pixels
        hauteur: hauteur de la raquette en pixels
        couleur: couleur de remplissage Tkinter
    """

    def __init__(self, canvas, x, y, largeur, hauteur, couleur):
        """
        Initialise l'objet raquette

        Args:
            canvas: canvas Tkinter qui recevra le rectangle
            x: position horizontale du coin superieur gauche
            y: position verticale du coin superieur gauche
            largeur: largeur du rectangle en pixels
            hauteur: hauteur du rectangle en pixels
            couleur: couleur de remplissage
        """
        self._canvas = canvas
        self.x = x
        self.y = y
        self.largeur = largeur
        self.hauteur = hauteur
        self.couleur = couleur

    def dessin(self):
        """
        Dessine un rectangle pour la raquette sur son canvas

        Returns:
            None
        """
        self._canvas.create_rectangle(self.x, self.y, self.x + self.largeur, self.y + self.hauteur,
                                      fill=self.couleur)

    def canvas(self):
        """
        Retourne le canvas associe a la raquette

        Returns:
            Canvas Tkinter utilise pour le dessin
        """
        return self._canvas

    def pos_xy(self):
        """
        Retourne la position du coin superieur gauche de la raquette

        Returns:
            Tuple (x, y) des coordonnees de la raquette
        """
        return self.x, self.y

    def stats_raq(self):
        """
        Retourne les dimensions et la couleur de la raquette

        Returns:
            Tuple (largeur, hauteur, couleur)
        """
        return self.largeur, self.hauteur, self.couleur
