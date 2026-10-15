# Header

"""
Type de fichier : Fichier classe partie
Date : 08/10/2026
Auteur : Constantin QUESSARD
Reste à faire : TOUT
"""

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

    def __init__(
        self,
        fenetre: tk.Toplevel,
        application,
        score_label: tk.Label,
        vies_label: tk.Label,
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
        self.terminee = False
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
        self.terrain.focus_set()

        self.briques = []
        self.objets_briques = []
        largeur_brique = 100
        hauteur_brique = 30
        nb_colonnes = 5
        nb_lignes = 3
        marge_x = 50
        marge_y = 50
        ecart = 20
        self.score = 0
        self.score_label = score_label
        self.vies = 3
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
            self.ajouter_point,
        )
        self.fenetre.protocol("WM_DELETE_WINDOW", self.fermer)
        self.animation.demarrer()

    def deplacer_raquette(self, distance: float) -> None:
        """Déplace horizontalement la raquette sans la faire sortir du terrain.

        Args:
            distance: déplacement demandé en pixels (négatif vers la gauche,
                positif vers la droite).

        Returns:
            None.
        """
        x1, _, x2, _ = self.terrain.coords(self.raquette_id)
        nouveau_x1 = max(3, min(x1 + distance, self.LARGEUR - 3 - self.raquette.largeur))
        self.terrain.move(self.raquette_id, nouveau_x1 - x1, 0)
        self.raquette.x = nouveau_x1

    def deplacer_raquette_gauche(self, event: tk.Event) -> None:
        """Déplace la raquette vers la gauche à la pression de la flèche gauche.

        Args:
            event: événement clavier Tkinter associé à la pression de la touche.

        Returns:
            None.
        """
        self.deplacer_raquette(-25)

    def deplacer_raquette_droite(self, event: tk.Event) -> None:
        """Déplace la raquette vers la droite à la pression de la flèche droite.

        Args:
            event: événement clavier Tkinter associé à la pression de la touche.

        Returns:
            None.
        """
        self.deplacer_raquette(25)

    def ajouter_point(self) -> None:
        self.score += 1
        self.score_label.config(text=f"Score : {self.score}")
        if not self.briques:
            self.animation.arreter()
            self.afficher_victoire()

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
        self.animation.arreter()
        if self.fenetre.winfo_exists():
            self.fenetre.destroy()
