"""Définition de la balle et de sa géométrie sur un canvas Tkinter."""

import math
import random
import tkinter as tk


class Balle:
    """Représente la balle, sa géométrie et son déplacement sur le canvas.

    Attributs de classe :
        RAYON: rayon de la balle, en pixels.
        VITESSE: vitesse initiale de la balle, en pixels par déplacement.

    Attributs d'instance :
        terrain: canvas Tkinter sur lequel la balle est dessinée.
        x: position horizontale initiale du centre de la balle.
        y: position verticale initiale du centre de la balle.
        rayon: rayon de cette balle.
        dx: déplacement horizontal à chaque pas d'animation.
        dy: déplacement vertical à chaque pas d'animation.
        identifiant: identifiant de l'ovale créé sur le canvas.

    Convention:
        Les coordonnées du canvas augmentent vers la droite et vers le bas.
        Une valeur positive de ``dy`` déplace donc la balle vers le bas.
    """

    RAYON = 15
    VITESSE = 5

    def __init__(self, terrain: tk.Canvas, x: float, y: float) -> None:
        """Crée et dessine une balle à la position indiquée.

        La balle reçoit une vitesse initiale aléatoire orientée vers le haut.

        Args:
            terrain: canvas Tkinter sur lequel dessiner la balle.
            x: coordonnée horizontale du centre de la balle.
            y: coordonnée verticale du centre de la balle.

        Returns:
            None.
        """
        self.terrain = terrain
        self.x = x
        self.y = y
        self.rayon = self.RAYON

        angle = random.uniform(math.pi, 2 * math.pi)
        self.dx = self.VITESSE * math.cos(angle)
        self.dy = self.VITESSE * math.sin(angle)

        self.identifiant = self.terrain.create_oval(
            self.x - self.rayon,
            self.y - self.rayon,
            self.x + self.rayon,
            self.y + self.rayon,
            outline="#42E6C2",
            fill="white",
        )

    def coordonnees(self) -> list[float]:
        """Récupère les limites actuelles de la balle sur le canvas.

        Returns:
            Liste contenant les coordonnées [x1, y1, x2, y2] de l'ovale.
        """
        return self.terrain.coords(self.identifiant)

    def deplacer(self) -> None:
        """Déplace la balle d'un pas selon ses vitesses dx et dy.

        Returns:
            None.
        """
        self.terrain.move(self.identifiant, self.dx, self.dy)