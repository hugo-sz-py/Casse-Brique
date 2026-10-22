"""Point d'entrée de l'application Casse-Brique.

Importe la classe de l'application, crée son instance puis lance sa boucle
d'événements Tkinter lorsque ce fichier est exécuté directement.

To do :
- Menu pause
- Utilisation des piles(empilemment des menus)/files(succession de niveaux) !!!!!
- Réduire le temps avant les déplacements de la raquette
(- Mode avec vitesse qui augmente
(- Mode infini
(- Mode forcé de toucher (grâce à la visée) une brique à chaque coup (avant de retoucher la raquette)
"""

from classcassebrique import CasseBriques

if __name__ == "__main__":
    # Ce bloc ne s'exécute que si main.py est lancé directement.
    application = CasseBriques()
    application.lancer()