"""Point d'entrée de l'application Casse-Brique.

Importe la classe de l'application, crée son instance puis lance sa boucle
d'événements Tkinter lorsque ce fichier est exécuté directement.
"""

from classcassebrique import CasseBriques


if __name__ == "__main__":
    application = CasseBriques()
    application.lancer()