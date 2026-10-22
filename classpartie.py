# Header

"""
Type de fichier : Fichier classe partie
Date : 08/10/2026
Auteur : Constantin QUESSARD
Reste à faire : TOUT
"""

import time
import tkinter as tk
from Brique import Brique
from Balle import Balle
from Raquette import Raquette
from animation import AnimationBalle

class Partie:
    """Gère le terrain, les briques, la balle et la fin d'une partie.

    Attributs de classe :
        LARGEUR: largeur du terrain de jeu, en pixels.
        HAUTEUR: hauteur du terrain de jeu, en pixels.
    """

    LARGEUR = 700
    HAUTEUR = 460
    VITESSE_RAQUETTE = 300
    DELAI_RAQUETTE = 16

    def __init__(
        self,
        fenetre: tk.Toplevel,
        application,
        score_label: tk.Label,
        vies_label: tk.Label,
        duree: str = "normal",
        difficulte: str = "facile",
    ) -> None:
        """Initialise une partie dans une fenêtre Tkinter existante.

        Crée le terrain et les briques, créé la balle et son animation,
        puis démarre le déplacement.

        Args:
            fenetre: fenêtre Tkinter dans laquelle afficher la partie.
            application: application principale, utilisée pour relancer une partie.

        Returns:
            None.
        """
        self.fenetre = fenetre
        self.application = application
        self.duree = duree
        self.difficulte = difficulte
        self.terminee = False
        self.en_pause = False
        self.terrain = tk.Canvas(fenetre, width=self.LARGEUR, height=self.HAUTEUR, bg="black", highlightthickness=0,)
        self.terrain.place(relx=0.5, y=65, anchor="n")
        self.terrain.create_rectangle( 2,     2,     self.LARGEUR - 2,     self.HAUTEUR - 2,     outline="green",     width=3,)

        largeur_raquette = 150
        self.raquette = Raquette(
            self.terrain,
            (self.LARGEUR - largeur_raquette) / 2,
            self.HAUTEUR - 35,
            largeur_raquette,
            15,
            "white",
        )
        self.raquette.dessin()
        self.raquette_id = self.terrain.find_all()[-1]
        self.terrain.bind("<Left>", self.deplacer_raquette_gauche)
        self.terrain.bind("<Right>", self.deplacer_raquette_droite)
        self.terrain.bind(
            "<Escape>",
            lambda event: self.ouvrir_menu_pause(),
        )
        self.terrain.focus_set()

        self.briques: list[int] = []
        self.objets_briques: list[Brique] = []
        largeur_brique = 100
        hauteur_brique = 30
        nb_colonnes = 5
        nb_lignes = 3
        marge_x = 50
        marge_y = 50
        ecart = 20
        self.score = 0
        self.score_label = score_label
        self.vies = 1 if self.difficulte == "hardcore" else 3
        self.vies_label = vies_label

        for i in range(nb_lignes):
            for j in range(nb_colonnes):
                x1 = marge_x + j * (largeur_brique + ecart)
                y1 = marge_y + i * (hauteur_brique + ecart)
                brique = Brique(
                    self.terrain,
                    x1,
                    y1,
                    largeur_brique,
                    hauteur_brique,
                    "red",
                    1,
                )
                brique.dessin()
                self.objets_briques.append(brique)
                # L'animation utilise les identifiants du canvas pour détecter les collisions.
                self.briques.append(self.terrain.find_all()[-1])
    
        self.balle = Balle(
            self.terrain,
            self.LARGEUR / 2,
            self.HAUTEUR / 1.10,
        )
        self.animation = AnimationBalle(
            self.terrain,
            self.balle,
            self.briques,
            self.raquette_id,
            self.LARGEUR,
            self.HAUTEUR,
            self.perdre_vie,
            self.ajouter_point
        )
        self.fenetre.protocol("WM_DELETE_WINDOW", self.fermer)
        self.animation.demarrer()
        #Attend de "DELAI_RAQUETTE" avant de faire "_animer_raquette"
        self._deplacement_raquette_id = self.terrain.after(self.DELAI_RAQUETTE, self._animer_raquette)

    def creer_briques(self) -> None:
        """Dessine une nouvelle rangée complète de briques."""
        self.briques.clear()
        self.objets_briques.clear()
        for i in range(self.nb_lignes):
            for j in range(self.nb_colonnes):
                x1 = self.marge_x + j * (self.largeur_brique + self.ecart)
                y1 = self.marge_y + i * (self.hauteur_brique + self.ecart)
                brique = Brique(
                    self.terrain,
                    x1,
                    y1,
                    self.largeur_brique,
                    self.hauteur_brique,
                    "red",
                    1,
                )
                brique.dessin()
                self.objets_briques.append(brique)
                # L'animation utilise les identifiants du canvas pour détecter les collisions.
                self.briques.append(self.terrain.find_all()[-1])

    def ouvrir_menu_pause(self) -> None:
        """Met la partie en pause et affiche les options de pause."""
        if self.terminee or self.en_pause:
            return

        self.en_pause = True
        self.animation.arreter()

        fenetre_pause = tk.Toplevel(self.fenetre)
        fenetre_pause.title("Pause")
        fenetre_pause.geometry("260x130")

        def reprendre() -> None:
            fenetre_pause.destroy()
            self.en_pause = False
            if not self.terminee:
                self.animation.demarrer()
                self.terrain.focus_set()

        def quitter() -> None:
            fenetre_pause.destroy()
            self.fermer()

        tk.Label(fenetre_pause, text="Jeu en pause", font=("Arial", 16)).pack(pady=15)
        tk.Button(fenetre_pause, text="Reprendre", command=reprendre).pack(side="left", expand=True)
        tk.Button(fenetre_pause, text="Quitter", command=quitter).pack(side="right", expand=True)
        fenetre_pause.protocol("WM_DELETE_WINDOW", reprendre)
        fenetre_pause.grab_set()

    def deplacer_raquette(self, distance: float) -> None:
        """Déplace horizontalement la raquette sans la faire sortir du terrain.

        Args:
            distance: déplacement demandé en pixels (négatif vers la gauche,
                positif vers la droite).

        Returns:
            None.
        """
        x1, _, _, _ = self.terrain.coords(self.raquette_id)
        nouveau_x1 = max(3, min(x1 + distance, self.LARGEUR - 3 - self.raquette.largeur))
        self.terrain.move(self.raquette_id, nouveau_x1 - x1, 0)
        self.raquette.x = nouveau_x1

    def _touche_raquette_enfoncee(self, event: tk.Event) -> None:
        if not self.terminee and event.keysym in ("Left", "Right"):
            self._touches_raquette.add(event.keysym)

    def _touche_raquette_relachee(self, event: tk.Event) -> None:
        self._touches_raquette.discard(event.keysym)

    def _reinitialiser_touches_raquette(self, event: tk.Event) -> None:
        if event.widget == self.terrain:
            self._touches_raquette.clear()

    def _animer_raquette(self) -> None:
        self._deplacement_raquette_id = None
        if self.terminee:
            return

        maintenant = time.perf_counter()
        delta_temps = min(maintenant - self._dernier_deplacement_raquette, 0.05)
        self._dernier_deplacement_raquette = maintenant
        direction = int("Right" in self._touches_raquette) - int(
            "Left" in self._touches_raquette
        )
        if direction:
            self.deplacer_raquette(
                direction * self.VITESSE_RAQUETTE * delta_temps
            )

        self._deplacement_raquette_id = self.terrain.after(
            self.DELAI_RAQUETTE,
            self._animer_raquette,
        )

    def ajouter_point(self) -> None:
        self.score += 1
        self.score_label.config(text=f"Score : {self.score}")
        if self.difficulte in ("difficile", "hardcore"):
            self.augmenter_vitesse_balle()
        if not self.briques:
            if self.duree == "infini":
                self.creer_briques()
            else:
                self.animation.arreter()
                self.afficher_victoire()

    def augmenter_vitesse_balle(self) -> None:
        """Augmente la vitesse de la balle en conservant sa direction."""
        vitesse = (self.balle.dx**2 + self.balle.dy**2) ** 0.5
        vitesse_max = 12
        nouvelle_vitesse = min(vitesse + 0.5, vitesse_max)
        facteur = nouvelle_vitesse / vitesse
        self.balle.dx *= facteur
        self.balle.dy *= facteur

    def perdre_vie(self) -> None:
        """Retire une vie et replace la balle, ou termine la partie à zéro.

        Returns:
            None.
        """
        self.vies -= 1
        self.vies_label.config(text=f"Vies : {self.vies}")

        if self.vies == 0:
            self.afficher_defaite()
            return


        self.terrain.coords(
            self.balle.identifiant,
            self.LARGEUR / 2 - self.balle.rayon,
            self.HAUTEUR / 2 - self.balle.rayon,
            self.LARGEUR / 2 + self.balle.rayon,
            self.HAUTEUR / 2 + self.balle.rayon,
        )
        self.balle.dy = -abs(self.balle.dy)
        self.animation.demarrer()

    def afficher_defaite(self) -> None:
        """Affiche la fenêtre de fin lorsque la balle est perdue.

        La fenêtre propose de rejouer ou de quitter la partie.

        Args:
            Aucun.

        Returns:
            None.
        """
        self.terminee = True
        fenetre_fin = tk.Toplevel(self.fenetre)
        fenetre_fin.title("Fin de partie")
        fenetre_fin.geometry("300x140")
        fenetre_fin.transient(self.fenetre)
        fenetre_fin.resizable(False, False)

        

        tk.Label(
            fenetre_fin,
            text="Vous avez perdu !",
            font=("Arial", 16),
        ).pack(pady=15)
        tk.Button(
            fenetre_fin,
            text="Rejouer",
            command=lambda: self.rejouer(fenetre_fin),
        ).pack(side="left", expand=True)
        tk.Button(
            fenetre_fin,
            text="Quitter",
            command=lambda: self.quitter(fenetre_fin),
        ).pack(side="right", expand=True)
        fenetre_fin.protocol(
            "WM_DELETE_WINDOW",
            lambda: self.quitter(fenetre_fin),
        )
        fenetre_fin.grab_set()


    def afficher_victoire(self) -> None:
            """Affiche la fenêtre de fin lorsque la balle est perdue.
    
            La fenêtre propose de rejouer ou de quitter la partie.
    
            Args:
                Aucun.
    
            Returns:
                None.
            """
            self.terminee = True
            fenetre_fin = tk.Toplevel(self.fenetre)
            fenetre_fin.title("Victoire")
            fenetre_fin.geometry("300x140")
            fenetre_fin.transient(self.fenetre)
            fenetre_fin.resizable(False, False)
        
            tk.Label(
                fenetre_fin,
                text="Vous avez gagné !",
                font=("Arial", 16),
            ).pack(pady=15)
            tk.Button(
                fenetre_fin,
                text="Rejouer",
                command=lambda: self.rejouer(fenetre_fin),
            ).pack(side="left", expand=True)
            tk.Button(
                fenetre_fin,
                text="Quitter",
                command=lambda: self.quitter(fenetre_fin),
            ).pack(side="right", expand=True)
            fenetre_fin.protocol(
                "WM_DELETE_WINDOW",
                lambda: self.quitter(fenetre_fin),
            )
            fenetre_fin.grab_set()
    

    def rejouer(self, fenetre_fin: tk.Toplevel) -> None:
        """Ferme la fenêtre de fin et démarre une nouvelle partie.

        Args:
            fenetre_fin: fenêtre de fin de partie à fermer.

        Returns:
            None.
        """
        fenetre_fin.destroy()
        self.fermer()
        self.application.jouer()

    def quitter(self, fenetre_fin: tk.Toplevel) -> None:
        """Ferme la fenêtre de fin et la fenêtre de jeu.

        Args:
            fenetre_fin: fenêtre de fin de partie à fermer.

        Returns:
            None.
        """
        fenetre_fin.destroy()
        self.fermer()

    def fermer(self) -> None:
        """Arrête l'animation et ferme la fenêtre de jeu.

        Returns:
            None.
        """
        self.terminee = True
        self._touches_raquette.clear()
        if (
            self._deplacement_raquette_id is not None
            and self.terrain.winfo_exists()
        ):
            self.terrain.after_cancel(self._deplacement_raquette_id)
            self._deplacement_raquette_id = None
        self.animation.arreter()
        if self.fenetre.winfo_exists():
            self.fenetre.destroy()
