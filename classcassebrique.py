# Header

"""
Type de fichier : Fichier classe casse brique
Date : 08/10/2026
Auteur : Constantin QUESSARD
Reste à faire : TOUT
"""

import tkinter as tk

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
        import classpartie as Pt

        jeu = tk.Toplevel(self.fenetre, bg="black")
        jeu.title("Jeu casse-brique")
        jeu.geometry("800x540")

        # Bonne pratique : appeler `.place()` séparément de la création du
        # widget évite de confondre son résultat (None) avec le widget lui-même.
        tk.Label(jeu, text="Score : 0", bg="black", fg="white", font=("Arial", 16)).place(x=10, y=10)
        tk.Label(jeu, text="Casse-brique", bg="black", fg="white", font=("Arial", 16)).place(relx=0.5, y=10, anchor="n")
        tk.Label(jeu, text="Vies : 3", bg="black", fg="white", font=("Arial", 16)).place(relx=1.0, x=-10, y=10, anchor="ne")

        Pt.Partie(jeu, self)

    def lancer(self) -> None:
        """Démarre la boucle d'événements de l'application."""
        self.fenetre.mainloop()