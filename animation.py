"""
Boucle d'animation et collisions de la balle

08/10/2026

SAEZ Hugo, QUESSARD Constantin

To do :

"""


import tkinter as tk
from collections.abc import Callable
import math

from Balle import Balle


class AnimationBalle:
    """
    Gere l'animation de la balle et ses interactions avec le terrain

    Attributs d'instance :
        terrain: canvas où la balle et les briques sont dessinees
        balle: objet Balle anime
        briques: identifiants des briques encore presentes sur le canvas
        largeur: largeur du terrain, en pixels
        hauteur: hauteur du terrain, en pixels
        perdre_vie: fonction appelee quand la balle tpuche le bas de l'ecran
        ajouter_point: fonction appelee lorsqu'une brique est detruite
        delai: delai entre deux deplacements, en millisecondes
        animation_id: identifiant du prochain deplacement programme, ou None
        arretee: indique si l'animation est arretee
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
        delai: int = 16
    ) -> None:
        """
        Prepare l'animation de la balle sans la demarrer

        Args:
            terrain: canvas Tkinter de la partie
            balle: balle a deplacer
            briques: liste modifiable des identifiants des briques
            raquette_id: identifiant de la raquette sur le canvas
            largeur: largeur du terrain, en pixels
            hauteur: hauteur du terrain, en pixels
            perdre_vie: fonction retirant une vie et relançant ou terminant
                la partie
            delai: temps entre deux deplacements, en millisecondes

        Returns:
            None
        """
        self.terrain = terrain
        self.balle = balle
        self.briques = briques
        self.raquette_id = raquette_id
        self.largeur = largeur
        self.hauteur = hauteur
        self.perdre_vie = perdre_vie
        self.delai = delai
        # self.animation_id est soit un str soit None
        self.animation_id: str | None = None
        self.arretee = True
        self.ajouter_point = ajouter_point

    def demarrer(self) -> None:
        """
        Demarre l'animation en effectuant le premier deplacement

        Returns:
            None
        """
        self.arretee = False
        self.deplacement()

    def deplacement(self) -> None:
        """
        Effectue un pas d'animation et programme le suivant

        Fait rebondir la balle sur les murs, supprime les briques touchees et
        la fait rebondir sur la raquette. Declenche la defaite si la balle
        atteint le bas du terrain.

        Returns:
            None
        """
        self.animation_id = None
        if self.arretee:
            return

        # Coordonnees des quatre bords de la balle avant son prochain deplacement
        x1, y1, x2, y2 = self.balle.coordonnees()

        # Inverse le deplacement horizontal si la balle va toucher un mur lateral
        if x1 + self.balle.dx <= 3 or x2 + self.balle.dx >= self.largeur - 3:
            self.balle.dx = -self.balle.dx
        # Si elle atteint le bas, arrete l'animation et signale une vie perdue
        if self.balle.dy > 0 and y2 + self.balle.dy >= self.hauteur - 3:
            self.arreter()
            self.perdre_vie()
            return
        # La balle rebondit sur le bord superieur du terrain
        if self.balle.dy < 0 and y1 + self.balle.dy <= 3:
            self.balle.dy = -self.balle.dy

        # find_overlapping(x1, y1, x2, y2) renvoie les objets du canvas qui
        # touchent la boîte englobante de la balle. L'asterisque "depaquette"
        # la liste [x1, y1, x2, y2] en quatre arguments
        objets_touches = self.terrain.find_overlapping(*self.balle.coordonnees())
        for objet in objets_touches:
            if objet in self.briques:
                # La brique touchee est supprimee et le rebond vertical est applique
                self.balle.dy = -self.balle.dy
                self.terrain.delete(objet)
                self.briques.remove(objet)
                self.ajouter_point()
                break

        # La destruction de la derniere brique peut avoir termine la partie
        if self.arretee:
            return

        # Recupere les bords horizontaux et le haut de la raquette
        raquette_x1, raquette_y1, raquette_x2, _ = self.terrain.coords(
            self.raquette_id
        )
        balle_x1, balle_y1, balle_x2, balle_y2 = self.balle.coordonnees()
        # Verifie que la balle descend et que sa prochaine position croise
        # la raquette horizontalement et verticalement
        if (self.balle.dy > 0
            and balle_y2 <= raquette_y1
            and balle_y2 + self.balle.dy >= raquette_y1
            and balle_x2 + self.balle.dx >= raquette_x1
            and balle_x1 + self.balle.dx <= raquette_x2):

            centre_raquette = (raquette_x1 + raquette_x2) / 2
            impact_x = (balle_x1 + balle_x2) / 2 + self.balle.dx

            # Decalage du contact par rapport au centre de la raquette :
            # -1 a gauche, 0 au centre, 1 a droite
            decalage = (impact_x - centre_raquette) / (
                (raquette_x2 - raquette_x1) / 2
            )
            decalage = max(-1, min(1, decalage))

            # hypot(dx, dy) calcule sqrt(dx**2 + dy**2), la vitesse totale
            # La conserver permet de changer l'angle sans accelerer la balle
            vitesse = math.hypot(self.balle.dx, self.balle.dy)
            angle_max = math.radians(60)
            angle = decalage * angle_max

            # Convertit l'angle de rebond en composantes horizontale et verticale
            self.balle.dx = vitesse * math.sin(angle)
            self.balle.dy = -vitesse * math.cos(angle)

        # Applique le deplacement calcule puis programme le prochain pas d'animation
        self.balle.deplacer()
        self.animation_id = self.terrain.after(self.delai, self.deplacement)

    def arreter(self) -> None:
        """
        Arrete l'animation et annule les deplacement encore programmes

        Returns:
            None
        """
        # Empêche les prochains pas d'animation de continuer
        self.arretee = True
        # Un callback peut encore attendre dans la file d'événements Tkinter
        if self.animation_id is not None and self.terrain.winfo_exists():
            # Annule ce callback pour éviter qu'il ne déplace la balle après l'arrêt
            self.terrain.after_cancel(self.animation_id)
            # Indique qu'aucun callback d'animation n'est désormais programmé
            self.animation_id = None