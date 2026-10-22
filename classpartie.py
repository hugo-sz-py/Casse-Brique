"""Contrôleur d'une partie : terrain, commandes, score et cycle de vie."""

import time
import tkinter as tk

from Balle import Balle
from Brique import Brique
from Implementation_Files import File
from Raquette import Raquette
from animation import AnimationBalle


class Partie:
    """Gère le terrain, les briques, la balle et la fin d'une partie.

    Attributs de classe :
        LARGEUR: largeur du terrain de jeu, en pixels.
        HAUTEUR: hauteur du terrain de jeu, en pixels.
        fenetre: fenêtre Tkinter hébergeant la partie.
        terrain: canvas de jeu.
        balle: balle en mouvement.
        raquette: raquette contrôlée au clavier.
        briques: identifiants des briques encore présentes sur le canvas.
        score: nombre de briques détruites pendant la partie.
        vies: nombre de vies restantes.
        duree: mode de partie (``"normal"``, ``"infini"`` ou ``"niveaux"``).
        difficulte: niveau choisi (``"facile"``, ``"difficile"`` ou
            ``"hardcore"``).
        niveau_actuel: numéro du niveau en cours en mode niveaux.
    """

    LARGEUR = 700
    HAUTEUR = 460
    FOND = "#0B1020"
    PANNEAU = "#151D32"
    PANNEAU_CLAIR = "#202B45"
    TEXTE = "#F4F7FF"
    TURQUOISE = "#42E6C2"
    CORAIL = "#FF6B7A"
    COULEURS_BRIQUES = ("#FF6B7A", "#FFB454", "#A78BFA")
    VITESSE_RAQUETTE = 300
    AUGMENTATION_VITESSE_RAQUETTE = 20
    AUGMENTATION_VITESSE_BALLE = 0.5
    DELAI_RAQUETTE = 16
    PATTERNS_NIVEAUX = (
        ("11111", "11111", "11111"),
        ("10101", "11111", "10101"),
        ("11111", "10001", "11111"),
        ("10101", "01110", "10101"),
    )

    def __init__(
        self,
        fenetre: tk.Frame,
        application,
        score_label: tk.Label,
        vies_label: tk.Label,
        meilleur_score_label: tk.Label | None = None,
        duree: str = "normal",
        difficulte: str = "facile",
        niveau_label: tk.Label | None = None,
    ) -> None:
        """Initialise une partie dans une fenêtre Tkinter existante.

        Crée le terrain et les briques, créé la balle et son animation,
        puis démarre le déplacement.

        Args:
            fenetre: fenêtre Tkinter dans laquelle afficher la partie.
            application: application principale, utilisée pour les records et
                pour relancer une partie.
            score_label: widget affichant le score courant.
            vies_label: widget affichant le nombre de vies restantes.
            meilleur_score_label: widget facultatif affichant le record.
            duree: mode normal (victoire à la dernière brique) ou infini
                (nouvelle grille après chaque série), ou niveaux (série de
                grilles prédéfinies).
            difficulte: niveau qui détermine notamment le nombre de vies et
                l'évolution de la vitesse.
            niveau_label: widget facultatif affichant la progression des
                niveaux.

        Returns:
            None.
        """
        self.fenetre = fenetre
        self.application = application
        self.meilleur_score_label = meilleur_score_label
        self.niveau_label = niveau_label
        self.duree = duree
        self.difficulte = difficulte
        self.niveaux_restants = File()
        self.nombre_niveaux = 0
        self.niveau_actuel = 0
        self.pattern_actuel: tuple[str, ...] | None = None
        if self.duree == "niveaux":
            for pattern in self.PATTERNS_NIVEAUX:
                self.niveaux_restants.enfiler(pattern)
            self.nombre_niveaux = self.niveaux_restants.taille()
            self._charger_niveau_suivant()
        self.vitesse_raquette = self.VITESSE_RAQUETTE
        self.terminee = False
        self.en_pause = False
        self.terrain = tk.Canvas(
            fenetre,
            width=self.LARGEUR,
            height=self.HAUTEUR,
            bg=self.FOND,
            highlightthickness=0,
        )
        self.terrain.place(relx=0.5, y=65, anchor="n")
        self.terrain.create_rectangle(
            2, 2, self.LARGEUR - 2, self.HAUTEUR - 2,
            outline=self.TURQUOISE, width=2,
        )

        largeur_raquette = 150
        self.raquette = Raquette(
            self.terrain,
            (self.LARGEUR - largeur_raquette) / 2,
            self.HAUTEUR - 35,
            largeur_raquette,
            15,
            self.TURQUOISE,
        )
        self.raquette.dessin()
        self.raquette_id = self.terrain.find_all()[-1]
        self._touches_raquette: set[str] = set()
        self._dernier_deplacement_raquette = time.perf_counter()
        self._deplacement_raquette_id: str | None = None
        self.terrain.bind("<KeyPress>", self._touche_raquette_enfoncee)
        self.terrain.bind("<KeyRelease>", self._touche_raquette_relachee)
        self.terrain.bind("<FocusOut>", self._reinitialiser_touches_raquette)
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
        self.vies = 1 if self.difficulte == "hardcore" else 3
        self.vies_label = vies_label
        self.vies_label.config(text=f"Vies : {self.vies}")

        self.largeur_brique = largeur_brique
        self.hauteur_brique = hauteur_brique
        self.nb_colonnes = nb_colonnes
        self.nb_lignes = nb_lignes
        self.marge_x = marge_x
        self.marge_y = marge_y
        self.ecart = ecart
        self.creer_briques()

        self.balle = Balle(self.terrain, self.LARGEUR / 2, self.HAUTEUR / 1.10)
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
        self.animation.demarrer()
        self._demarrer_animation_raquette()

    def creer_briques(self) -> None:
        """Remplace la grille suivie par une nouvelle rangée de briques.

        Met à jour les listes ``briques`` (identifiants du canvas) et
        ``objets_briques`` (instances métier) en même temps que le dessin.
        """
        self.briques.clear()
        self.objets_briques.clear()
        pattern = self.pattern_actuel or tuple(
            "1" * self.nb_colonnes for _ in range(self.nb_lignes)
        )
        for i, ligne in enumerate(pattern):
            for j, presence in enumerate(ligne):
                if presence != "1":
                    continue
                x1 = self.marge_x + j * (self.largeur_brique + self.ecart)
                y1 = self.marge_y + i * (self.hauteur_brique + self.ecart)
                couleur = self.COULEURS_BRIQUES[i % len(self.COULEURS_BRIQUES)]
                brique = Brique(
                    self.terrain,
                    x1,
                    y1,
                    self.largeur_brique,
                    self.hauteur_brique,
                    couleur,
                    1,
                )
                brique.dessin()
                self.objets_briques.append(brique)
                # L'animation utilise les identifiants du canvas pour détecter les collisions.
                self.briques.append(self.terrain.find_all()[-1])

    def _charger_niveau_suivant(self) -> bool:
        """Retire le prochain motif de la file et actualise son indicateur.

        Returns:
            ``True`` si un niveau a été chargé, sinon ``False`` si tous les
            niveaux ont déjà été joués.
        """
        if self.niveaux_restants.est_vide():
            return False

        self.pattern_actuel = self.niveaux_restants.defiler()
        self.niveau_actuel += 1
        if self.niveau_label is not None:
            self.niveau_label.config(
                text=f"Niveau {self.niveau_actuel}/{self.nombre_niveaux}"
            )
        return True

    def ouvrir_menu_pause(self) -> None:
        """Suspend les animations et ouvre les actions de pause.

        Aucun effet si la partie est déjà en pause ou terminée.
        """
        if self.terminee or self.en_pause:
            return

        self.en_pause = True
        self.animation.arreter()
        self._touches_raquette.clear()
        self._arreter_animation_raquette()

        fenetre_pause = tk.Toplevel(self.fenetre)
        fenetre_pause.title("Pause")
        fenetre_pause.geometry("300x170")
        fenetre_pause.configure(bg=self.FOND)
        fenetre_pause.resizable(False, False)

        def reprendre() -> None:
            """Ferme le menu de pause et relance les animations."""
            fenetre_pause.destroy()
            self.en_pause = False
            if not self.terminee:
                self.animation.demarrer()
                self._demarrer_animation_raquette()
                self.terrain.focus_set()

        def quitter() -> None:
            """Ferme le menu de pause puis termine la fenêtre de jeu."""
            fenetre_pause.destroy()
            self.fermer()

        tk.Label(
            fenetre_pause,
            text="PAUSE",
            bg=self.FOND,
            fg=self.TURQUOISE,
            font=("Segoe UI", 18, "bold"),
        ).pack(pady=(20, 14))
        boutons = tk.Frame(fenetre_pause, bg=self.FOND)
        boutons.pack()
        tk.Button(
            boutons,
            text="Reprendre",
            command=reprendre,
            bg=self.TURQUOISE,
            fg=self.FOND,
            activebackground="#78F2D8",
            activeforeground=self.FOND,
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            bd=0,
            padx=15,
            pady=7,
            cursor="hand2",
        ).pack(side="left", padx=6)
        tk.Button(
            boutons,
            text="Quitter",
            command=quitter,
            bg=self.PANNEAU_CLAIR,
            fg=self.TEXTE,
            activebackground="#303D59",
            activeforeground=self.TEXTE,
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            bd=0,
            padx=15,
            pady=7,
            cursor="hand2",
        ).pack(side="left", padx=6)
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
        x1, _, x2, _ = self.terrain.coords(self.raquette_id)
        nouveau_x1 = max(3, min(x1 + distance, self.LARGEUR - 3 - self.raquette.largeur))
        self.terrain.move(self.raquette_id, nouveau_x1 - x1, 0)
        self.raquette.x = nouveau_x1

    def _touche_raquette_enfoncee(self, event: tk.Event) -> None:
        """Mémorise une direction ou ouvre le menu de pause sur Échap.

        Args:
            event: événement Tkinter contenant la touche enfoncée.
        """
        if event.keysym == "Escape":
            self.ouvrir_menu_pause()
            return
        if not self.terminee and event.keysym in ("Left", "Right"):
            self._touches_raquette.add(event.keysym)

    def _touche_raquette_relachee(self, event: tk.Event) -> None:
        """Retire la touche relâchée de l'ensemble des touches actives.

        Args:
            event: événement Tkinter contenant la touche relâchée.
        """
        self._touches_raquette.discard(event.keysym)

    def _reinitialiser_touches_raquette(self, event: tk.Event) -> None:
        """Efface les directions actives lorsque le terrain perd le focus.

        Args:
            event: événement Tkinter déclenché lors de la perte de focus.
        """
        if event.widget == self.terrain:
            self._touches_raquette.clear()

    def _demarrer_animation_raquette(self) -> None:
        """Programme le prochain pas d'animation de la raquette."""
        if self._deplacement_raquette_id is None and not self.terminee:
            self._dernier_deplacement_raquette = time.perf_counter()
            self._deplacement_raquette_id = self.terrain.after(
                self.DELAI_RAQUETTE,
                self._animer_raquette,
            )

    def _arreter_animation_raquette(self) -> None:
        """Annule le pas de déplacement de raquette éventuellement programmé."""
        if (
            self._deplacement_raquette_id is not None
            and self.terrain.winfo_exists()
        ):
            self.terrain.after_cancel(self._deplacement_raquette_id)
            self._deplacement_raquette_id = None

    def _animer_raquette(self) -> None:
        """Déplace la raquette selon les touches et programme le pas suivant.

        Le déplacement tient compte du temps réellement écoulé pour conserver
        une vitesse régulière malgré les variations de cadence de Tkinter.
        """
        self._deplacement_raquette_id = None
        if self.terminee or self.en_pause:
            return

        maintenant = time.perf_counter()
        delta_temps = min(maintenant - self._dernier_deplacement_raquette, 0.05)
        self._dernier_deplacement_raquette = maintenant
        direction = int("Right" in self._touches_raquette) - int("Left" in self._touches_raquette)
        if direction:
            self.deplacer_raquette(
                direction * self.vitesse_raquette * delta_temps
            )

        self._deplacement_raquette_id = self.terrain.after(
            self.DELAI_RAQUETTE,
            self._animer_raquette,
        )

    def ajouter_point(self) -> None:
        """Ajoute un point, actualise les records et traite la fin de grille.

        En difficulté difficile ou hardcore, chaque point augmente aussi la
        vitesse de la raquette et de la balle. En mode infini, la grille est
        recréée ; en mode normal, la partie se termine par une victoire.
        """
        self.score += 1
        self.score_label.config(text=f"Score : {self.score}")
        meilleur_score = self.application.enregistrer_score(
            self.score,
            self.difficulte,
            self.duree,
        )
        if self.meilleur_score_label is not None:
            if self.difficulte in self.application.FICHIERS_MEILLEURS_SCORES:
                valeur = (
                    str(meilleur_score)
                    if meilleur_score is not None
                    else "indisponible"
                )
            else:
                valeur = "non suivi"
            self.meilleur_score_label.config(
                text=f"Meilleur {self.difficulte} : {valeur}"
            )
        if self.difficulte in ("difficile", "hardcore"):
            self.vitesse_raquette += self.AUGMENTATION_VITESSE_RAQUETTE
            self.augmenter_vitesse_balle()
        if not self.briques:
            if self.duree == "infini":
                self.creer_briques()
            elif self.duree == "niveaux" and self._charger_niveau_suivant():
                self.creer_briques()
                centre_x = self.LARGEUR / 2
                centre_y = self.HAUTEUR / 1.10
                self.terrain.coords(
                    self.balle.identifiant,
                    centre_x - self.balle.rayon,
                    centre_y - self.balle.rayon,
                    centre_x + self.balle.rayon,
                    centre_y + self.balle.rayon,
                )
            else:
                self.animation.arreter()
                self.afficher_victoire()

    def augmenter_vitesse_balle(self) -> None:
        """Augmente la norme de la vitesse sans modifier sa direction."""
        vitesse = (self.balle.dx**2 + self.balle.dy**2) ** 0.5
        nouvelle_vitesse = vitesse + self.AUGMENTATION_VITESSE_BALLE
        facteur = nouvelle_vitesse / vitesse
        self.balle.dx *= facteur
        self.balle.dy *= facteur

    def perdre_vie(self) -> None:
        """Retire une vie et replace la balle, ou termine la partie à zéro.

        Returns:
            None.

        Effet de bord:
            Met à jour l'affichage, replace la balle si des vies restent, ou
            ouvre l'écran de défaite à zéro vie.
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
        fenetre_fin.configure(bg=self.FOND)

        tk.Label(
            fenetre_fin,
            text="PARTIE TERMINÉE",
            bg=self.FOND,
            fg=self.CORAIL,
            font=("Segoe UI", 16, "bold"),
        ).pack(pady=(18, 4))
        tk.Label(
            fenetre_fin,
            text=f"Score : {self.score}",
            bg=self.FOND,
            fg=self.TEXTE,
            font=("Segoe UI", 11),
        ).pack(pady=(0, 7))
        tk.Button(
            fenetre_fin,
            text="Rejouer",
            command=lambda: self.rejouer(fenetre_fin),
            bg=self.TURQUOISE,
            fg=self.FOND,
            activebackground="#78F2D8",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            bd=0,
            padx=14,
            pady=5,
            cursor="hand2",
        ).pack(side="left", expand=True)
        tk.Button(
            fenetre_fin,
            text="Quitter",
            command=lambda: self.quitter(fenetre_fin),
            bg=self.PANNEAU_CLAIR,
            fg=self.TEXTE,
            activebackground="#303D59",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            bd=0,
            padx=14,
            pady=5,
            cursor="hand2",
        ).pack(side="right", expand=True)
        fenetre_fin.protocol(
            "WM_DELETE_WINDOW",
            lambda: self.quitter(fenetre_fin),
        )
        fenetre_fin.grab_set()


    def afficher_victoire(self) -> None:
        """Affiche l'écran de victoire après la dernière brique du mode normal.

        La fenêtre propose de démarrer une nouvelle partie ou de quitter.
        """
        self.terminee = True
        fenetre_fin = tk.Toplevel(self.fenetre)
        fenetre_fin.title("Victoire")
        fenetre_fin.geometry("300x140")
        fenetre_fin.transient(self.fenetre)
        fenetre_fin.resizable(False, False)
        fenetre_fin.configure(bg=self.FOND)

        tk.Label(
            fenetre_fin,
            text="BRAVO, VICTOIRE !",
            bg=self.FOND,
            fg=self.TURQUOISE,
            font=("Segoe UI", 16, "bold"),
        ).pack(pady=(18, 4))
        tk.Label(
            fenetre_fin,
            text=f"Score : {self.score}",
            bg=self.FOND,
            fg=self.TEXTE,
            font=("Segoe UI", 11),
        ).pack(pady=(0, 7))
        tk.Button(
            fenetre_fin,
            text="Rejouer",
            command=lambda: self.rejouer(fenetre_fin),
            bg=self.TURQUOISE,
            fg=self.FOND,
            activebackground="#78F2D8",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            bd=0,
            padx=14,
            pady=5,
            cursor="hand2",
        ).pack(side="left", expand=True)
        tk.Button(
            fenetre_fin,
            text="Quitter",
            command=lambda: self.quitter(fenetre_fin),
            bg=self.PANNEAU_CLAIR,
            fg=self.TEXTE,
            activebackground="#303D59",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            bd=0,
            padx=14,
            pady=5,
            cursor="hand2",
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
        self._arreter_animation_raquette()
        self.animation.arreter()
        if self.fenetre.winfo_exists():
            self.application.revenir()
