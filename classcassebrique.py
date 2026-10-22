# Header

"""
Type de fichier : Fichier classe casse brique
Date : 08/10/2026
Auteur : Constantin QUESSARD
Reste à faire : TOUT
"""

import tkinter as tk
from pathlib import Path
from tkinter import messagebox

from Implementation_Piles import Pile


class CasseBriques:
    """Gère les écrans de l'application et leur historique de navigation."""

    FICHIERS_MEILLEURS_SCORES = {
        "facile": "meilleur_score_facile.txt",
        "difficile": "meilleur_score_difficile.txt",
        "hardcore": "meilleur_score_hardcore.txt",
    }

    def __init__(self) -> None:
        """Initialise la fenêtre principale et construit le menu."""
        # Bonne pratique : garder la fenêtre principale dans `self` permet
        # aux autres méthodes de la classe d'y accéder.
        self.fenetre = tk.Tk()
        self.fenetre.title("Casse-briques")
        self.fenetre.geometry("800x540")
        self.fenetre.protocol("WM_DELETE_WINDOW", self.fenetre.destroy)
        self.ecrans = Pile()
        self.meilleurs_scores = self._charger_meilleurs_scores()
        self.menu = tk.Frame(self.fenetre)
        self.creer_menu()
        self._afficher_ecran(self.menu)

    def creer_menu(self) -> None:
        """Crée les boutons et le texte de bienvenue du menu principal."""
        # Bonne pratique : séparer la création du menu de son initialisation
        # rend chaque méthode plus facile à lire et à maintenir.
        tk.Label(self.menu, text="Bienvenue dans le casse-brique d'Hugo et Constantin !", font=("Arial", 16)).pack(pady=20)

        self.duree_var = tk.StringVar(value="normal")
        tk.Label(self.menu, text="Durée de la partie", font=("Arial", 16)).pack()
        ligne_duree = tk.Frame(self.menu)
        ligne_duree.pack()
        for option in ("normal", "infini"):
            tk.Radiobutton(
                ligne_duree,
                text=option.capitalize(),
                variable=self.duree_var,
                value=option,
                font=("Arial", 16),
            ).pack(side="left", padx=10)

        self.difficulte_var = tk.StringVar(value="facile")
        tk.Label(self.menu, text="Difficulté", font=("Arial", 16)).pack(pady=(10, 0))
        ligne_difficulte = tk.Frame(self.menu)
        ligne_difficulte.pack()
        for option in ("facile", "difficile", "hardcore"):
            tk.Radiobutton(
                ligne_difficulte,
                text=option.capitalize(),
                variable=self.difficulte_var,
                value=option,
                font=("Arial", 16),
            ).pack(side="left", padx=10)

        self.meilleurs_scores_label = tk.Label(
            self.menu,
            text=self._texte_meilleurs_scores(),
            font=("Arial", 12),
            justify="center",
        )
        self.meilleurs_scores_label.pack(pady=15)

        tk.Button(self.menu, text="JOUER", command=self.jouer, font=("Arial", 16)).place(x=360, y=320)
        tk.Button(self.menu, text="QUITTER", command=self.fenetre.destroy, font=("Arial",16)).place(x=350,y=420)

    def _afficher_ecran(self, ecran: tk.Frame) -> None:
        """Empile et affiche un écran en masquant celui qui était actif."""
        if not self.ecrans.est_vide():
            self.ecrans.sommet().pack_forget()
        self.ecrans.empiler(ecran)
        ecran.pack(fill="both", expand=True)

    def revenir(self) -> None:
        """Retire l'écran actif et réaffiche l'écran précédent."""
        if self.ecrans.taille() <= 1:
            return

        ecran_actif = self.ecrans.depiler()
        ecran_actif.destroy()
        self.ecrans.sommet().pack(fill="both", expand=True)

    def _chemin_fichier_score(self, difficulte: str) -> Path:
        return Path(__file__).resolve().parent / self.FICHIERS_MEILLEURS_SCORES[difficulte]

    def _charger_meilleurs_scores(self) -> dict[str, int | None]:
        scores: dict[str, int | None] = {}
        for difficulte in self.FICHIERS_MEILLEURS_SCORES:
            chemin = self._chemin_fichier_score(difficulte)
            try:
                contenu = chemin.read_text(encoding="utf-8").strip()
                scores[difficulte] = int(contenu) if contenu else 0
                if scores[difficulte] is not None and scores[difficulte] < 0:
                    raise ValueError("Le score ne peut pas être négatif.")
            except FileNotFoundError:
                scores[difficulte] = 0
            except (OSError, ValueError) as erreur:
                scores[difficulte] = None
                messagebox.showerror(
                    "Erreur de meilleur score",
                    f"Impossible de lire {chemin.name} : {erreur}",
                    parent=self.fenetre,
                )
        return scores

    def _texte_meilleurs_scores(self) -> str:
        lignes = ["Meilleurs scores en mode infini"]
        for difficulte, score in self.meilleurs_scores.items():
            valeur = str(score) if score is not None else "indisponible"
            lignes.append(f"{difficulte.capitalize()} : {valeur}")
        return "\n".join(lignes)

    def meilleur_score(self, difficulte: str) -> int | None:
        return self.meilleurs_scores.get(difficulte)

    def _texte_meilleur_score(self, difficulte: str) -> str:
        if difficulte not in self.FICHIERS_MEILLEURS_SCORES:
            return "non suivi"
        score = self.meilleur_score(difficulte)
        return str(score) if score is not None else "indisponible"

    def enregistrer_score(
        self,
        score: int,
        difficulte: str,
        duree: str,
    ) -> int | None:
        """Enregistre un nouveau record uniquement pour les modes infinis suivis."""
        meilleur_score = self.meilleur_score(difficulte)
        if (
            duree != "infini"
            or difficulte not in self.FICHIERS_MEILLEURS_SCORES
            or meilleur_score is None
            or score <= meilleur_score
        ):
            return meilleur_score

        chemin = self._chemin_fichier_score(difficulte)
        try:
            chemin.write_text(f"{score}\n", encoding="utf-8")
        except OSError as erreur:
            self.meilleurs_scores[difficulte] = None
            messagebox.showerror(
                "Erreur de meilleur score",
                f"Impossible d'enregistrer le record dans {chemin.name} : {erreur}",
                parent=self.fenetre,
            )
            self.meilleurs_scores_label.config(text=self._texte_meilleurs_scores())
            return None

        self.meilleurs_scores[difficulte] = score
        self.meilleurs_scores_label.config(text=self._texte_meilleurs_scores())
        return score

    def jouer(self) -> None:
        """Empile l'écran de jeu au-dessus du menu principal."""
        import classpartie as Pt
        jeu = tk.Frame(self.fenetre, bg="black")

        # Bonne pratique : appeler `.place()` séparément de la création du
        # widget évite de confondre son résultat (None) avec le widget lui-même.
        score_label = tk.Label(jeu, text="Score : 0", bg="black", fg="white", font=("Arial", 16))
        score_label.place(x=70, y=10)        
        tk.Label(jeu, text="Casse-brique", bg="black", fg="white", font=("Arial", 16)).place(relx=0.5, y=10, anchor="n")
        vies_label = tk.Label(jeu, text="Vies : 3", bg="black", fg="white", font=("Arial", 16))
        vies_label.place(relx=1.0, x=-10, y=10, anchor="ne")
        difficulte = self.difficulte_var.get()
        meilleur_score_label = tk.Label(
            jeu,
            text=f"Meilleur {difficulte} : {self._texte_meilleur_score(difficulte)}",
            bg="black",
            fg="white",
            font=("Arial", 12),
        )
        meilleur_score_label.place(relx=0.5, y=36, anchor="n")

        partie = Pt.Partie(
            jeu,
            self,
            score_label,
            vies_label,
            duree=self.duree_var.get(),
            difficulte=difficulte,
            meilleur_score_label=meilleur_score_label,
        )
        tk.Button(jeu, text="   I I   ", command=partie.ouvrir_menu_pause,font=("Arial", 12)).place(x=10, y=10)
        self._afficher_ecran(jeu)
        partie.terrain.focus_set()

    def lancer(self) -> None:
        """Démarre la boucle d'événements de l'application."""
        self.fenetre.mainloop()