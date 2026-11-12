# Casse-briques

Jeu de casse-briques réalisé en Python avec Tkinter.

## Lancer le jeu

Exécuter `main.py` avec Python :


## Règles du jeu

- Déplacez la raquette avec les flèches gauche et droite pour renvoyer la balle.
- La balle rebondit sur les murs, le haut du terrain, la raquette et les briques.
- Chaque brique détruite rapporte un point.
- La partie commence avec 15 briques disposées en 3 rangées de 5.
- Vous perdez une vie si la balle atteint le bas du terrain. La partie se termine
  quand il ne reste plus de vie.
- En mode **normal**, détruire toutes les briques fait gagner la partie.
- En mode **infini**, les briques réapparaissent lorsqu'elles sont toutes
  détruites ; la partie continue jusqu'à la défaite.
- La touche Échap ou le bouton pause ouvre le menu de pause.

## Spécificités de l'implémentation

- Le menu permet de choisir la durée (**normal** ou **infini**) et la difficulté
  (**facile**, **difficile** ou **hardcore**).
- Le mode facile commence avec 3 vies. Le mode hardcore commence avec 1 vie.
- En difficile et en hardcore, détruire une brique augmente la vitesse de la
  raquette et de la balle.
- Les meilleurs scores sont enregistrés séparément pour chaque difficulté en
  mode infini, dans `meilleur_score_facile.txt`,
  `meilleur_score_difficile.txt` et `meilleur_score_hardcore.txt`.
- L'angle de rebond de la balle sur la raquette dépend de l'endroit où elle la
  touche.

## Organisation des fichiers

- `main.py` : point d'entrée de l'application.
- `classcassebrique.py` : fenêtre principale, menu, choix des modes et gestion
  des meilleurs scores.
- `classpartie.py` : configuration et déroulement d'une partie, vies, score,
  pause et écrans de fin.
- `Balle.py`, `Brique.py` et `Raquette.py` : objets du jeu.
- `animation.py` : déplacements de la balle, rebonds et collisions.
- `Implementation_Files.py` : implémentation de la structure de données **File**
  (enfiler, défiler, consulter le premier élément, tester si elle est vide et
  obtenir sa taille).
- `Implementation_Piles.py` : implémentation de la structure de données **Pile**
  (empiler, dépiler, consulter le sommet, tester si elle est vide et obtenir sa
  taille).

## Dépôt Git

Adresse GIT : `https://github.com/hugo-sz-py/Casse-Brique/tree/main`
