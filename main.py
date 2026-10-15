"""Point d'entrée de l'application Casse-Brique.

Importe la classe de l'application, crée son instance puis lance sa boucle
d'événements Tkinter lorsque ce fichier est exécuté directement.

To do :
- Menu pause
- Score qui augmente
- Vies qui descendent 
- Balle qui part de plus bas
- Changer le rebond selon la position de la raquette
- Utilisation des piles/files
"""

from classcassebrique import CasseBriques

if __name__ == "__main__":
    # Ce bloc ne s'exécute que si main.py est lancé directement.
    application = CasseBriques()
    application.lancer()