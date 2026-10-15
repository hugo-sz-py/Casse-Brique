# Header

"""
Type de fichier : Fichier graphique
Date : 08/10/2026
Auteur : Constantin QUESSARD
Reste à faire : TOUT
"""

import tkinter as tk
import math
import random


class CasseBriques:
    """Gère la fenêtre principale et les fenêtres de jeu."""

    def __init__(self) -> None:
        """Initialise la fenêtre principale et construit le menu."""
        # Bonne pratique : garder la fenêtre principale dans `self` permet
        # aux autres méthodes de la classe d'y accéder.
        self.fenetre = tk.Tk()
        self.fenetre.title("Casse-briques")
        self.fenetre.geometry("800x540")
        self.creer_menu()

    def creer_menu(self) -> None:
        """Crée les boutons et le texte de bienvenue du menu principal."""
        # Bonne pratique : séparer la création du menu de son initialisation
        # rend chaque méthode plus facile à lire et à maintenir.
        tk.Button(self.fenetre, text="JOUER", command=self.jouer).pack()
        tk.Label(self.fenetre, text="Bienvenue dans le casse-brique d'Hugo et Constantin !", font=("Arial", 16)).pack(pady=20)
        tk.Button(self.fenetre, text="QUITTER", command=self.fenetre.destroy).pack()

    def jouer(self) -> None:
        """Ouvre la fenêtre de jeu et affiche son interface."""
        # Bonne pratique : utiliser une Toplevel permet d'ajouter une fenêtre
        # secondaire sans créer une seconde fenêtre racine Tk.
        jeu = tk.Toplevel(self.fenetre, bg="black")
        jeu.title("Jeu casse-brique")
        jeu.geometry("800x540")

        # Bonne pratique : appeler `.place()` séparément de la création du
        # widget évite de confondre son résultat (None) avec le widget lui-même.
        tk.Label(jeu, text="Score : 0", bg="black", fg="white", font=("Arial", 16)).place(x=10, y=10)
        tk.Label(jeu, text="Casse-brique", bg="black", fg="white", font=("Arial", 16)).place(relx=0.5, y=10, anchor="n")
        tk.Label(jeu, text="Vies : 3", bg="black", fg="white", font=("Arial", 16)).place(relx=1.0, x=-10, y=10, anchor="ne")

        Partie(jeu, self)

    def lancer(self) -> None:
        """Démarre la boucle d'événements de l'application."""
        self.fenetre.mainloop()


class Partie:
    """Gère le terrain et l'animation de la balle d'une partie."""

    LARGEUR = 700
    HAUTEUR = 460
    RAYON = 15
    DELAI_ANIMATION = 8*2

    def __init__(self, fenetre: tk.Toplevel, application: CasseBriques) -> None:
        """Crée le terrain et la balle dans la fenêtre de jeu existante."""
        self.fenetre = fenetre
        self.application = application
        self.terminee = False
        self.animation_id: str | None = None

        self.terrain = tk.Canvas(fenetre, width=self.LARGEUR, height=self.HAUTEUR, bg="black", highlightthickness=0,)
        self.terrain.place(relx=0.5, y=65, anchor="n")
        self.terrain.create_rectangle( 2,     2,     self.LARGEUR - 2,     self.HAUTEUR - 2,     outline="green",     width=3,)

        positions_x = [0.16, 0.33, 0.5, 0.67, 0.84]
        positions_y = [80, 160, 240]

        self.briques_canvas = []

        for y in positions_y:
            for x in positions_x:
                c = tk.Canvas(fenetre, width=100, height=50, bg="red", highlightthickness=0)
                c.place(relx=x, y=y, anchor="n")
                c.create_rectangle(2, 2, 98, 48, outline="yellow", width=3)
                self.briques_canvas.append(c)
    
        self.x = self.LARGEUR / 2
        self.y = self.HAUTEUR / 2
        vitesse = 12
        angle = random.uniform(0, 2 * math.pi)
        self.dx = vitesse * math.cos(angle)
        self.dy = vitesse * math.sin(angle)

        self.balle = self.terrain.create_oval(
            self.x - self.RAYON,
            self.y - self.RAYON,
            self.x + self.RAYON,
            self.y + self.RAYON,
            outline="green",
            fill="white",
        )
        self.fenetre.protocol("WM_DELETE_WINDOW", self.fermer)
        self.deplacement()

    def deplacement(self) -> None:
        """Déplace la balle et la fait rebondir sur les bords du terrain."""
        self.animation_id = None
        if self.terminee:
            return

        x1, y1, x2, y2 = self.terrain.coords(self.balle)

        if x1 + self.dx <= 3 or x2 + self.dx >= self.LARGEUR - 3:
            self.dx = -self.dx
        if self.dy > 0 and y2 + self.dy >= self.HAUTEUR - 3:
            self.afficher_defaite()
            return
        if self.dy < 0 and y1 + self.dy <= 3:
            self.dy = -self.dy

        self.terrain.move(self.balle, self.dx, self.dy)
        self.animation_id = self.terrain.after(self.DELAI_ANIMATION, self.deplacement,)

    def afficher_defaite(self) -> None:
        """Affiche les choix proposés après la perte de la partie."""
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
        """Ferme la partie terminée et en démarre une nouvelle."""
        fenetre_fin.destroy()
        self.fermer()
        self.application.jouer()

    def quitter(self, fenetre_fin: tk.Toplevel) -> None:
        """Ferme la partie et revient au menu principal."""
        fenetre_fin.destroy()
        self.fermer()

    def fermer(self) -> None:
        """Arrête l'animation et ferme la fenêtre de jeu."""
        self.terminee = True
        if self.animation_id is not None and self.terrain.winfo_exists():
            self.terrain.after_cancel(self.animation_id)
            self.animation_id = None
        if self.fenetre.winfo_exists():
            self.fenetre.destroy()


if __name__ == "__main__":
    application = CasseBriques()
    application.lancer()