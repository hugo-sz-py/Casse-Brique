"""
Definition de la balle et de sa geometrie sur le canvas du jeu

08/10/2026

SAEZ Hugo, QUESSARD Constantin

To do :

"""


import math
import random
import tkinter as tk


class Balle:
    """
    Decrit la balle, sa geometrie et son deplacement sur le canvas

    Attributs :
        RAYON: rayon de la balle, en pixels
        VITESSE: vitesse initiale de la balle, en pixels par deplacement
        terrain: canvas Tkinter sur lequel la balle est dessinee
        x: position horizontale initiale du centre de la balle
        y: position verticale initiale du centre de la balle
        rayon: rayon de la balle
        dx: deplacement horizontal a chaque pas d'animation
        dy: deplacement vertical a chaque pas d'animation
        identifiant: identifiant de l'ovale cree sur le canvas

    Convention:
        Les coordonnees du canvas augmentent vers la droite et vers le bas
        Une valeur positive de dy deplace donc la balle vers le bas
    """

    RAYON = 15
    VITESSE = 5

    def __init__(self, terrain: tk.Canvas, x: float, y: float) -> None:
        """
        Initialise et dessine une balle a la position indiquee
        La balle reçoit une vitesse initiale aleatoire orientee vers le haut

        Args:
            terrain: canvas Tkinter sur lequel dessiner la balle
            x: coordonnee horizontale du centre de la balle
            y: coordonnee verticale du centre de la balle
        """
        self.terrain = terrain
        self.x = x
        self.y = y
        self.rayon = self.RAYON

        angle = random.uniform(math.pi, 2 * math.pi)
        self.dx = self.VITESSE * math.cos(angle)
        self.dy = self.VITESSE * math.sin(angle)

        self.identifiant = self.terrain.create_oval(self.x - self.rayon, self.y - self.rayon,
                                                    self.x + self.rayon, self.y + self.rayon,
                                                    outline="#42E6C2", fill="white")

    def coordonnees(self) -> list[float]:
        """
        Recupere les limites actuelles de la balle sur le canvas

        Returns:
            Liste contenant les coordonnees [x1, y1, x2, y2] de l'ovale
        """
        return self.terrain.coords(self.identifiant)

    def deplacer(self) -> None:
        """
        Deplace la balle d'un pas selon ses vitesses dx et dy

        Returns:
            None
        """
        self.terrain.move(self.identifiant, self.dx, self.dy)