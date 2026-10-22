"""Définition de la raquette contrôlée par le joueur."""


class Raquette:
    """Décrit la position et l'apparence de la raquette.

    Attributs:
        _canvas: zone Tkinter sur laquelle dessiner la raquette.
        x: coordonnée horizontale du coin supérieur gauche.
        y: coordonnée verticale du coin supérieur gauche.
        largeur: largeur de la raquette en pixels.
        hauteur: hauteur de la raquette en pixels.
        couleur: couleur de remplissage Tkinter.
    """

    def __init__(self, canvas, x, y, largeur, hauteur, couleur):
        """Initialise la raquette sans la dessiner.

        Args:
            canvas: canvas Tkinter qui recevra le rectangle.
            x: position horizontale du coin supérieur gauche.
            y: position verticale du coin supérieur gauche.
            largeur: largeur du rectangle en pixels.
            hauteur: hauteur du rectangle en pixels.
            couleur: couleur de remplissage.
        """
        self._canvas = canvas
        self.x = x
        self.y = y
        self.largeur = largeur
        self.hauteur = hauteur
        self.couleur = couleur

    def dessin(self):
        """Dessine la raquette comme un rectangle sur son canvas.

        Returns:
            None.
        """
        self._canvas.create_rectangle(
            self.x,
            self.y,
            self.x + self.largeur,
            self.y + self.hauteur,
            fill=self.couleur,
        )

    def canvas(self):
        """Retourne le canvas associé à la raquette.

        Returns:
            Canvas Tkinter utilisé pour le dessin.
        """
        return self._canvas

    def pos_xy(self):
        """Retourne la position du coin supérieur gauche de la raquette.

        Returns:
            Tuple (x, y) des coordonnées de la raquette.
        """
        return self.x, self.y

    def stats_raq(self):
        """Retourne les dimensions et la couleur de la raquette.

        Returns:
            Tuple (largeur, hauteur, couleur).
        """
        return self.largeur, self.hauteur, self.couleur
