"""Définition de la brique dessinée sur le canvas du jeu."""


class Brique:
    """Décrit une brique et ses caractéristiques graphiques.

    Attributs:
        _canvas: zone Tkinter sur laquelle dessiner la brique.
        x: coordonnée horizontale du coin supérieur gauche.
        y: coordonnée verticale du coin supérieur gauche.
        largeur: largeur de la brique en pixels.
        hauteur: hauteur de la brique en pixels.
        couleur: couleur de remplissage Tkinter.
        nb_vie_brique: nombre de coups requis pour détruire la brique.
    """

    def __init__(
        self,
        canvas,
        x,
        y,
        largeur,
        hauteur,
        couleur,
        nb_vie_brique,
    ):
        """Initialise une brique sans la dessiner.

        Args:
            canvas: canvas Tkinter qui recevra le rectangle.
            x: position horizontale du coin supérieur gauche.
            y: position verticale du coin supérieur gauche.
            largeur: largeur du rectangle en pixels.
            hauteur: hauteur du rectangle en pixels.
            couleur: couleur de remplissage.
            nb_vie_brique: nombre de coups nécessaires à sa destruction.
        """
        self._canvas = canvas
        self.x = x
        self.y = y
        self.largeur = largeur
        self.hauteur = hauteur
        self.couleur = couleur
        self.nb_vie_brique = nb_vie_brique

    def dessin(self):
        """Dessine la brique comme un rectangle sur son canvas.

        Returns:
            None.
        """
        self._canvas.create_rectangle(
            self.x,
            self.y,
            self.x + self.largeur,
            self.y + self.hauteur,
            fill=self.couleur,
            outline="#0B1020",
            width=2,
        )

    def canvas(self):
        """Retourne le canvas associé à la brique.

        Returns:
            Canvas Tkinter utilisé pour le dessin.
        """
        return self._canvas

    def pos_xy(self):
        """Retourne la position du coin supérieur gauche de la brique.

        Returns:
            Tuple (x, y) des coordonnées de la brique.
        """
        return self.x, self.y

    def stats_brq(self):
        """Retourne les dimensions et la couleur de la brique.

        Returns:
            Tuple (largeur, hauteur, couleur).
        """
        return self.largeur, self.hauteur, self.couleur

    def vie_brq(self):
        """Retourne le nombre de coups restants avant destruction.

        Returns:
            Nombre de vies actuellement stocké pour la brique.
        """
        return self.nb_vie_brique
