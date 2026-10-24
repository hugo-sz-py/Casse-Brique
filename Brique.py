"""
Definition de la brique dessinee sur le canvas du jeu

08/10/2026

SAEZ Hugo, QUESSARD Constantin

To do :

"""

class Brique:
    """
    Decrit une brique et ses caracteristiques graphiques

    Attributs:
        canvas: zone Tkinter sur laquelle dessiner la brique
        x: coordonnee horizontale du coin superieur gauche
        y: coordonnee verticale du coin superieur gauche
        largeur: largeur de la brique en pixels
        hauteur: hauteur de la brique en pixels
        couleur: couleur de remplissage Tkinter
        nb_vie_brique: nombre de coups requis pour detruire la brique
    """

    def __init__(self, canvas, x, y, largeur, hauteur, couleur, nb_vie_brique):
        """
        Initialise une brique sans la dessiner

        Args:
            canvas: canvas Tkinter qui recevra le rectangle
            x: position horizontale du coin superieur gauche
            y: position verticale du coin superieur gauche
            largeur: largeur du rectangle en pixels
            hauteur: hauteur du rectangle en pixels
            couleur: couleur de remplissage
            nb_vie_brique: nombre de coups requis pour detruire la brique
        """
        self._canvas = canvas
        self.x = x
        self.y = y
        self.largeur = largeur
        self.hauteur = hauteur
        self.couleur = couleur
        self.nb_vie_brique = nb_vie_brique

    def dessin(self):
        """
        Dessine la brique comme un rectangle sur son canvas

        Returns:
            None
        """
        self._canvas.create_rectangle(self.x, self.y, self.x + self.largeur, self.y + self.hauteur, fill=self.couleur,
                                      outline="#0B1020", width=2)

    def canvas(self):
        """
        Retourne le canvas associe a la brique

        Returns:
            Canvas Tkinter utilise pour le dessin
        """
        return self._canvas

    def pos_xy(self):
        """
        Retourne la position du coin superieur gauche de la brique

        Returns:
            Tuple (x, y) des coordonnees de la brique
        """
        return self.x, self.y

    def stats_brq(self):
        """
        Retourne les dimensions et la couleur de la brique

        Returns:
            Tuple (largeur, hauteur, couleur)
        """
        return self.largeur, self.hauteur, self.couleur

    def vie_brq(self):
        """
        Retourne le nombre de coups restants avant destruction

        Returns:
            Nombre de vies actuellement stocke pour la brique
        """
        return self.nb_vie_brique
