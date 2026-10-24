"""
Fenetre principale, menu de configuration et gestion des records

08/10/2026

SAEZ Hugo, QUESSARD Constantin

To do :

"""

import tkinter as tk
from pathlib import Path
from tkinter import messagebox

from Implementation_Piles import Pile


class CasseBriques:
    """
    Gere le menu principal, les records et l'ouverture des parties

    Attributs:
        fenetre: fenetre racine Tkinter de l'application
        meilleurs_scores: record par difficulte, ou None si illisible
        duree_var: variable Tkinter du mode normal, infini ou niveaux
        difficulte_var: variable Tkinter du niveau de difficulte
        meilleurs_scores_label: widget affichant les records du menu
        ecrans: pile des ecrans utilises pour la navigation
    """

    FOND = "#0B1020"
    PANNEAU = "#151D32"
    PANNEAU_CLAIR = "#202B45" 
    TEXTE = "#F4F7FF"
    TEXTE_DOUX = "#A9B5CC"
    TURQUOISE = "#42E6C2"
    CORAIL = "#FF6B7A"

    FICHIERS_MEILLEURS_SCORES = {
        "facile": "meilleur_score_facile.txt",
        "difficile": "meilleur_score_difficile.txt",
        "hardcore": "meilleur_score_hardcore.txt",
    }

    def __init__(self) -> None:
        """
        Cree la fenetre racine, charge les records et construit le menu
        """
        self.fenetre = tk.Tk()
        self.fenetre.title("Casse-briques")
        self.fenetre.geometry("800x620")
        self.fenetre.minsize(720, 580)
        self.fenetre.configure(bg=self.FOND)
        self.ecrans = Pile()
        self.meilleurs_scores = self.charger_meilleurs_scores()
        self.menu = tk.Frame(self.fenetre, bg=self.FOND)
        self.creer_menu()
        self.afficher_ecran(self.menu)

    def creer_menu(self) -> None:
        """
        Construit les choix de mode, de difficulte et les actions du menu

        Les choix sont conserves dans des variables Tkinter utilisees ensuite
        par jouer() pour configurer une nouvelle partie
        """
        tk.Frame(self.menu, bg=self.TURQUOISE, height=5).pack(fill="x")
        contenu = tk.Frame(self.menu, bg=self.FOND)
        contenu.pack(fill="both", expand=True, padx=32, pady=22)

        tk.Label(
            contenu,
            text="CASSE-BRIQUES",
            bg=self.FOND,
            fg=self.TEXTE,
            font=("Segoe UI", 27, "bold")
        ).pack()

        tk.Label(
            contenu,
            text="Choisis ton mode et prepare-toi a jouer",
            bg=self.FOND,
            fg=self.TEXTE_DOUX,
            font=("Segoe UI", 11)
        ).pack(pady=(2, 18))

        options = tk.Frame(contenu, bg=self.PANNEAU, padx=22, pady=16)
        options.pack(fill="x")
        self.duree_var = tk.StringVar(value="normal")
        tk.Label(
            options, text="MODE DE JEU", bg=self.PANNEAU, fg=self.TURQUOISE,
            font=("Segoe UI", 10, "bold")
        ).pack(anchor="w")

        ligne_duree = tk.Frame(options, bg=self.PANNEAU)
        ligne_duree.pack(anchor="w", pady=(5, 14))

        for option in ("normal", "infini", "niveaux"):
            tk.Radiobutton(
                ligne_duree,
                text=f"  {option.capitalize()}  ",
                variable=self.duree_var,
                value=option,
                indicatoron=False,
                selectcolor=self.PANNEAU_CLAIR,
                bg=self.PANNEAU,
                fg=self.TEXTE,
                activebackground=self.PANNEAU_CLAIR,
                activeforeground=self.TURQUOISE,
                font=("Segoe UI", 10, "bold"),
                padx=7,
                pady=7,
                bd=0,
                relief="flat",
                cursor="hand2"
            ).pack(side="left", padx=(0, 8))

        self.difficulte_var = tk.StringVar(value="facile")
        tk.Label(
            options, text="DIFFICULTe", bg=self.PANNEAU, fg=self.TURQUOISE,
            font=("Segoe UI", 10, "bold")
        ).pack(anchor="w")

        ligne_difficulte = tk.Frame(options, bg=self.PANNEAU)
        ligne_difficulte.pack(anchor="w", pady=(5, 0))
        for option in ("facile", "difficile", "hardcore"):
            tk.Radiobutton(
                ligne_difficulte,
                text=f"  {option.capitalize()}  ",
                variable=self.difficulte_var,
                value=option,
                indicatoron=False,
                selectcolor=self.PANNEAU_CLAIR,
                bg=self.PANNEAU,
                fg=self.TEXTE,
                activebackground=self.PANNEAU_CLAIR,
                activeforeground=self.TURQUOISE,
                font=("Segoe UI", 10, "bold"),
                padx=7,
                pady=7,
                bd=0,
                relief="flat",
                cursor="hand2"
            ).pack(side="left", padx=(0, 8))

        scores = tk.Frame(contenu, bg=self.PANNEAU, padx=18, pady=12)
        scores.pack(fill="x", pady=14)
        self.meilleurs_scores_label = tk.Label(
            scores,
            text=self._texte_meilleurs_scores(),
            bg=self.PANNEAU,
            fg=self.TEXTE,
            font=("Segoe UI", 10),
            justify="center",
            padx=5,
            pady=2
        )
        self.meilleurs_scores_label.pack()

        boutons = tk.Frame(contenu, bg=self.FOND)
        boutons.pack(pady=(2, 0))
        tk.Button(
            boutons,
            text="JOUER",
            command=self.jouer,
            bg=self.TURQUOISE,
            fg=self.FOND,
            activebackground="#78F2D8",
            activeforeground=self.FOND,
            font=("Segoe UI", 12, "bold"),
            relief="flat",
            bd=0,
            padx=36,
            pady=10,
            cursor="hand2"
        ).pack(side="left", padx=8)

        tk.Button(
            boutons,
            text="QUITTER",
            command=self.fenetre.destroy,
            bg=self.PANNEAU_CLAIR,
            fg=self.TEXTE,
            activebackground="#303D59",
            activeforeground=self.TEXTE,
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            bd=0,
            padx=24,
            pady=10,
            cursor="hand2"
        ).pack(side="left", padx=8)


    def afficher_ecran(self, ecran: tk.Frame) -> None:
        """
        Empile puis affiche un ecran en masquant l'ecran actuellement actif

        Args:
            ecran: frame Tkinter a afficher
        """
        if not self.ecrans.est_vide():
            self.ecrans.sommet().pack_forget()
        self.ecrans.empiler(ecran)
        ecran.pack(fill="both", expand=True)

    def revenir(self) -> None:
        """
        Ferme l'ecran actif et affiche l'ecran precedent s'il existe
        """
        if self.ecrans.taille() <= 1:
            return

        ecran_actif = self.ecrans.depiler()
        ecran_actif.destroy()
        self.ecrans.sommet().pack(fill="both", expand=True)

    def chemin_fichier_score(self, difficulte: str) -> Path:
        """
        Construit le chemin du fichier de record d'une difficulte

        Args:
            difficulte: cle de difficulte presente dans FICHIERS_MEILLEURS_SCORES

        Returns:
            Chemin du fichier associe, dans le dossier de ce module
        """
        return Path(__file__).resolve().parent / self.FICHIERS_MEILLEURS_SCORES[difficulte]

    def charger_meilleurs_scores(self) -> dict[str, int | None]:
        """
        Charge les records connus et signale les fichiers invalides

        Un fichier absent represente un score initial de zero. Une erreur de
        lecture ou un contenu invalide est signale et stocke
        sous la forme None

        Returns:
            Dictionnaire associant chaque difficulte a son score ou None
        """
        scores: dict[str, int | None] = {}
        for difficulte in self.FICHIERS_MEILLEURS_SCORES:
            chemin = self.chemin_fichier_score(difficulte)
            try:
                contenu = chemin.read_text(encoding="utf-8").strip()
                scores[difficulte] = int(contenu) if contenu else 0
                if scores[difficulte] is not None and scores[difficulte] < 0:
                    raise ValueError("Le score ne peut pas etre negatif.")
            except FileNotFoundError:
                scores[difficulte] = 0
            except (OSError, ValueError) as erreur:
                scores[difficulte] = None
                messagebox.showerror(
                    "Erreur de meilleur score",
                    f"Impossible de lire {chemin.name} : {erreur}",
                    parent=self.fenetre
                )
        return scores

    def _texte_meilleurs_scores(self) -> str:
        """
        Formate les records pour l'affichage dans le menu

        Returns:
            Texte multiligne contenant le meilleur score de chaque difficulte
        """
        lignes = ["Meilleurs scores en mode infini"]
        for difficulte, score in self.meilleurs_scores.items():
            valeur = str(score) if score is not None else "indisponible"
            lignes.append(f"{difficulte.capitalize()} : {valeur}")
        return "\n".join(lignes)

    def meilleur_score(self, difficulte: str) -> int | None:
        """
        Retourne le record actuellement connu pour une difficulte

        Args:
            difficulte: nom du niveau a consulter

        Returns:
            Score enregistre, ou None si la difficulte est inconnue ou
            si son fichier de score n'est pas lisible
        """
        return self.meilleurs_scores.get(difficulte)

    def texte_meilleur_score(self, difficulte: str) -> str:
        """
        Convertit le record d'une difficulte en texte d'interface

        Args:
            difficulte: difficulte affichee

        Returns:
            Score en texte, "indisponible" ou "non suivi"
        """
        if difficulte not in self.FICHIERS_MEILLEURS_SCORES:
            return "non suivi"
        score = self.meilleur_score(difficulte)
        return str(score) if score is not None else "indisponible"

    def enregistrer_score(self, score: int, difficulte: str, duree: str) -> int | None:
        """
        Enregistre un nouveau record si le score depasse l'ancien

        Seuls les modes infinis et les difficultes repertoriees sont suivis
        En cas d'erreur d'ecriture, une boîte de dialogue est affichee et le
        score de cette difficulte devient indisponible

        Args:
            score: score obtenu par la partie
            difficulte: niveau de difficulte de la partie
            duree: mode de duree selectionne

        Returns:
            Nouveau record, ancien record si aucun remplacement n'est requis,
            ou None en cas d'echec de lecture/ecriture
        """
        meilleur_score = self.meilleur_score(difficulte)
        if (
            duree != "infini"
            or difficulte not in self.FICHIERS_MEILLEURS_SCORES
            or meilleur_score is None
            or score <= meilleur_score
        ):
            return meilleur_score

        chemin = self.chemin_fichier_score(difficulte)
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
        """
        Affiche un ecran de jeu configure selon les choix du menu
        """
        import classpartie as Pt

        jeu = tk.Frame(self.fenetre, bg=self.FOND)

        barre = tk.Frame(jeu, bg=self.PANNEAU, padx=10, pady=7)
        barre.place(relx=0.5, y=9, anchor="n", width=700, height=46)
        score_label = tk.Label(
            barre, text="Score : 0", bg=self.PANNEAU, fg=self.TURQUOISE,
            font=("Segoe UI", 11, "bold"),
        )
        score_label.pack(side="left", padx=(5, 12))

        tk.Label(
            barre, text="CASSE-BRIQUES", bg=self.PANNEAU, fg=self.TEXTE,
            font=("Segoe UI", 11, "bold")
        ).pack(side="left", padx=8)

        difficulte = self.difficulte_var.get()
        meilleur_score_label = tk.Label(
            barre,
            text=f"Meilleur {difficulte} : {self.texte_meilleur_score(difficulte)}",
            bg=self.PANNEAU,
            fg=self.TEXTE_DOUX,
            font=("Segoe UI", 9)
        )
        meilleur_score_label.pack(side="left", padx=8)

        niveau_label = tk.Label(
            barre,
            text="",
            bg=self.PANNEAU,
            fg=self.TEXTE_DOUX,
            font=("Segoe UI", 9, "bold")
        )
        niveau_label.pack(side="left", padx=8)

        vies_label = tk.Label(
            barre, text="Vies : 3", bg=self.PANNEAU, fg=self.CORAIL,
            font=("Segoe UI", 11, "bold")
        )
        vies_label.pack(side="right", padx=(8, 5))

        partie = Pt.Partie(
            jeu,
            self,
            score_label,
            vies_label,
            duree=self.duree_var.get(),
            difficulte=difficulte,
            meilleur_score_label=meilleur_score_label,
            niveau_label=niveau_label,
        )

        tk.Button(
            barre,
            text="PAUSE",
            command=partie.ouvrir_menu_pause,
            bg=self.PANNEAU_CLAIR,
            fg=self.TEXTE,
            activebackground="#303D59",
            activeforeground=self.TURQUOISE,
            font=("Segoe UI", 9, "bold"),
            relief="flat",
            bd=0,
            padx=10,
            pady=4,
            cursor="hand2",
        ).pack(side="right", padx=6)

        self.afficher_ecran(jeu)
        partie.terrain.focus_set()

    def lancer(self) -> None:
        """
        Lance la boucle d'evenements Tkinter de la fenetre principale
        """
        self.fenetre.mainloop()