import tkinter as tk
from collections.abc import Callable

from Balle import Balle


class AnimationBalle:
    """Gère l'animation de la balle et ses interactions avec le terrain.

    Attributs d'instance :
        terrain: canvas où la balle et les briques sont dessinées.
        balle: objet Balle animé.
        briques: identifiants des briques encore présentes sur le canvas.
        largeur: largeur du terrain, en pixels.
        hauteur: hauteur du terrain, en pixels.
        afficher_defaite: fonction appelée quand la balle est perdue.
        delai: délai entre deux déplacements, en millisecondes.
        animation_id: identifiant du prochain déplacement programmé, ou None.
        arretee: indique si l'animation est arrêtée.
    """

    def __init__(
        self,
        terrain: tk.Canvas,
        balle: Balle,
        briques: list[int],
        largeur: int,
        hauteur: int,
        afficher_defaite: Callable[[], None],
        delai: int = 16,
    ) -> None:
        """Prépare l'animation de la balle sans la démarrer.

        Args:
            terrain: canvas Tkinter de la partie.
            balle: balle à déplacer.
            briques: liste modifiable des identifiants des briques.
            largeur: largeur du terrain, en pixels.
            hauteur: hauteur du terrain, en pixels.
            afficher_defaite: fonction affichant la fenêtre de défaite.
            delai: temps entre deux déplacements, en millisecondes.

        Returns:
            None.
        """
        self.terrain = terrain
        self.balle = balle
        self.briques = briques
        self.largeur = largeur
        self.hauteur = hauteur
        self.afficher_defaite = afficher_defaite
        self.delai = delai
        self.animation_id: str | None = None
        self.arretee = True

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
        déclenche la défaite si la balle atteint le bas du terrain.

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
            self.afficher_defaite()
            return
        if self.balle.dy < 0 and y1 + self.balle.dy <= 3:
            self.balle.dy = -self.balle.dy

        objets_touches = self.terrain.find_overlapping(*self.balle.coordonnees())
        for objet in objets_touches:
            if objet in self.briques:
                self.balle.dy = -self.balle.dy
                self.terrain.delete(objet)
                self.briques.remove(objet)
                break

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