from django.core.management.base import BaseCommand
from planning.models import Cours

class Command(BaseCommand):
    help = 'Duplique les cours de la semaine 1 vers les semaines 2 à 6'

    def handle(self, *args, **kwargs):
        self.stdout.write("Début de la duplication des cours...")
        
        # Récupérer tous les cours de la semaine 1
        cours_semaine_1 = Cours.objects.filter(semaine=1, est_valide=True)
        
        # Pour chaque semaine de 2 à 6
        for semaine in range(2, 7):
            self.stdout.write(f"Duplication vers la semaine {semaine}...")
            
            # Pour chaque cours de la semaine 1
            for cours in cours_semaine_1:
                # Créer une copie du cours pour la nouvelle semaine
                Cours.objects.create(
                    matiere=cours.matiere,
                    professeur=cours.professeur,
                    groupe=cours.groupe,
                    salle=cours.salle,
                    periode=cours.periode,
                    semaine=semaine,
                    est_valide=True
                )
        
        self.stdout.write(self.style.SUCCESS("Duplication terminée avec succès !")) 