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
from animation import AnimationBalle

class Partie:
    """Gère le terrain, les briques, la balle et la fin d'une partie.

    Attributs de classe :
        LARGEUR: largeur du terrain de jeu, en pixels.
        HAUTEUR: hauteur du terrain de jeu, en pixels.
    """

    LARGEUR = 700
    HAUTEUR = 460

    def __init__(self, fenetre: tk.Toplevel, application) -> None:
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

        self.briques = []
        self.objets_briques = []
        largeur_brique = 100
        hauteur_brique = 30
        nb_colonnes = 5
        nb_lignes = 3
        marge_x = 50
        marge_y = 50
        ecart = 20

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
            self.HAUTEUR / 2,
        )
        self.animation = AnimationBalle(
            self.terrain,
            self.balle,
            self.briques,
            self.LARGEUR,
            self.HAUTEUR,
            self.afficher_defaite,
        )
        self.fenetre.protocol("WM_DELETE_WINDOW", self.fermer)
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
