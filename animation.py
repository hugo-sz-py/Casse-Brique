"""Boucle d'animation et collisions de la balle."""

import tkinter as tk
from collections.abc import Callable
import math

from Balle import Balle


class AnimationBalle:
    """Gère l'animation de la balle et ses interactions avec le terrain.

    Attributs d'instance :
        terrain: canvas où la balle et les briques sont dessinées.
        balle: objet Balle animé.
        briques: identifiants des briques encore présentes sur le canvas.
        largeur: largeur du terrain, en pixels.
        hauteur: hauteur du terrain, en pixels.
        perdre_vie: fonction appelée quand la balle est perdue.
        ajouter_point: fonction appelée lorsqu'une brique est détruite.
        delai: délai entre deux déplacements, en millisecondes.
        animation_id: identifiant du prochain déplacement programmé, ou None.
        arretee: indique si l'animation est arrêtée.
    """

    def __init__(
        self,
        terrain: tk.Canvas,
        balle: Balle,
        briques: list[int],
        raquette_id: int,
        largeur: int,
        hauteur: int,
        perdre_vie: Callable[[], None],
        ajouter_point: Callable[[], None],
        delai: int = 16,
    ) -> None:
        """Prépare l'animation de la balle sans la démarrer.

        Args:
            terrain: canvas Tkinter de la partie.
            balle: balle à déplacer.
            briques: liste modifiable des identifiants des briques.
            raquette_id: identifiant de la raquette sur le canvas.
            largeur: largeur du terrain, en pixels.
            hauteur: hauteur du terrain, en pixels.
            perdre_vie: fonction retirant une vie et relançant ou terminant
                la partie.
            delai: temps entre deux déplacements, en millisecondes.

        Returns:
            None.
        """
        self.terrain = terrain
        self.balle = balle
        self.briques = briques
        self.raquette_id = raquette_id
        self.largeur = largeur
        self.hauteur = hauteur
        self.perdre_vie = perdre_vie
        self.delai = delai
        self.animation_id: str | None = None
        self.arretee = True
        self.ajouter_point = ajouter_point

    def demarrer(self) -> None:
        """Démarre l'animation en effectuant le premier déplacement.

        Returns:
            None.
        """
        self.arretee = False
        self.deplacement()

    def deplacement(self) -> None:
        """Effectue un pas d'animation et programme le suivant.

        Fait rebondir la balle sur les murs, supprime les briques touchées et
        la fait rebondir sur la raquette. Déclenche la défaite si la balle
        atteint le bas du terrain.

        Returns:
            None.
        """
        self.animation_id = None
        if self.arretee:
            return

        x1, y1, x2, y2 = self.balle.coordonnees()

        if x1 + self.balle.dx <= 3 or x2 + self.balle.dx >= self.largeur - 3:
            self.balle.dx = -self.balle.dx
        if self.balle.dy > 0 and y2 + self.balle.dy >= self.hauteur - 3:
            self.arreter()
            self.perdre_vie()
            return
        if self.balle.dy < 0 and y1 + self.balle.dy <= 3:
            self.balle.dy = -self.balle.dy

        objets_touches = self.terrain.find_overlapping(*self.balle.coordonnees())
        for objet in objets_touches:
            if objet in self.briques:
                self.balle.dy = -self.balle.dy
                self.terrain.delete(objet)
                self.briques.remove(objet)
                self.ajouter_point()
                break

        if self.arretee:
            return

        raquette_x1, raquette_y1, raquette_x2, _ = self.terrain.coords(
            self.raquette_id
        )
        balle_x1, balle_y1, balle_x2, balle_y2 = self.balle.coordonnees()
        if (
            self.balle.dy > 0
            and balle_y2 <= raquette_y1
            and balle_y2 + self.balle.dy >= raquette_y1
            and balle_x2 + self.balle.dx >= raquette_x1
            and balle_x1 + self.balle.dx <= raquette_x2
        ):
            centre_raquette = (raquette_x1 + raquette_x2) / 2
            impact_x = (balle_x1 + balle_x2) / 2 + self.balle.dx

            # Position du contact entre -1 (bord gauche) et 1 (bord droit).
            decalage = (impact_x - centre_raquette) / (
                (raquette_x2 - raquette_x1) / 2
            )
            decalage = max(-1, min(1, decalage))

            vitesse = math.hypot(self.balle.dx, self.balle.dy)
            angle_max = math.radians(60)
            angle = decalage * angle_max

            self.balle.dx = vitesse * math.sin(angle)
            self.balle.dy = -vitesse * math.cos(angle)

        self.balle.deplacer()
        self.animation_id = self.terrain.after(self.delai, self.deplacement)

    def arreter(self) -> None:
        """Arrête l'animation et annule le déplacement encore programmé.

        Returns:
            None.
        """
        self.arretee = True
        if self.animation_id is not None and self.terrain.winfo_exists():
            self.terrain.after_cancel(self.animation_id)
            self.animation_id = None