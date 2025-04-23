from django.core.management.base import BaseCommand
from django.utils import timezone
from core.models import Domaine, Specialite, Matiere, Professeur, Salle, Groupe, PeriodeHoraire
from planning.models import Cours
import random
from datetime import time

class Command(BaseCommand):
    help = 'Remplit la base de données avec des données de test'

    def handle(self, *args, **kwargs):
        self.stdout.write("Début du remplissage de la base de données...")
        
        # Nettoyer la base de données
        self.stdout.write("Nettoyage de la base de données...")
        Cours.objects.all().delete()
        PeriodeHoraire.objects.all().delete()
        Matiere.objects.all().delete()
        Specialite.objects.all().delete()
        Domaine.objects.all().delete()
        Professeur.objects.all().delete()
        Salle.objects.all().delete()
        Groupe.objects.all().delete()

        # Créer les domaines
        self.stdout.write("Création des domaines...")
        info = Domaine.objects.create(nom="Informatique")
        sciences = Domaine.objects.create(nom="Sciences")

        # Créer les spécialités
        self.stdout.write("Création des spécialités...")
        dev_web = Specialite.objects.create(nom="Dev Web", domaine=info)
        ia = Specialite.objects.create(nom="IA", domaine=info)
        physique = Specialite.objects.create(nom="Physique", domaine=sciences)
        maths = Specialite.objects.create(nom="Maths", domaine=sciences)

        # Créer les matières
        self.stdout.write("Création des matières...")
        matieres_info = [
            ("HTML/CSS", dev_web),
            ("JavaScript", dev_web),
            ("Python", ia),
            ("Machine Learning", ia),
        ]
        matieres_sciences = [
            ("Mécanique", physique),
            ("Thermodynamique", physique),
            ("Algèbre", maths),
            ("Analyse", maths),
        ]
        matieres = []
        for nom, specialite in matieres_info + matieres_sciences:
            matieres.append(Matiere.objects.create(nom=nom, specialite=specialite))

        # Créer les professeurs
        self.stdout.write("Création des professeurs...")
        professeurs = []
        for i in range(1, 6):
            professeurs.append(Professeur.objects.create(
                nom=f"Professeur {i}",
                email=f"prof{i}@example.com"
            ))

        # Créer les salles
        self.stdout.write("Création des salles...")
        salles = []
        for i in range(1, 7):
            salles.append(Salle.objects.create(
                nom=f"Salle {i}",
                capacite=random.randint(20, 50)
            ))

        # Créer les groupes
        self.stdout.write("Création des groupes...")
        groupes = [
            Groupe.objects.create(nom="L1 Info", specialite=dev_web),
            Groupe.objects.create(nom="L2 Info", specialite=dev_web),
            Groupe.objects.create(nom="L1 Sci", specialite=physique),
            Groupe.objects.create(nom="L2 Sci", specialite=physique),
        ]

        # Créer les périodes horaires
        self.stdout.write("Création des périodes horaires...")
        jours = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi']
        periodes = []
        for jour in jours:
            for i in range(6):
                heure_debut = time(8 + i, 0)
                heure_fin = time(9 + i, 0)
                periodes.append(PeriodeHoraire.objects.create(
                    jour=jour,
                    heure_debut=heure_debut,
                    heure_fin=heure_fin
                ))

        # Créer les cours
        self.stdout.write("Création des cours...")
        semaine = 1
        for groupe in groupes:
            # Sélectionner les matières appropriées selon la spécialité
            if groupe.specialite in [dev_web, ia]:
                matieres_groupe = [m for m in matieres if m.specialite in [dev_web, ia]]
            else:
                matieres_groupe = [m for m in matieres if m.specialite in [physique, maths]]

            # Créer un cours par jour
            for jour in jours:
                # Choisir une période aléatoire pour ce jour
                periodes_jour = [p for p in periodes if p.jour == jour]
                periode = random.choice(periodes_jour)
                
                # Choisir une matière, un professeur et une salle aléatoires
                matiere = random.choice(matieres_groupe)
                professeur = random.choice(professeurs)
                salle = random.choice(salles)

                # Vérifier les conflits
                conflit = False
                for cours_existant in Cours.objects.filter(
                    semaine=semaine,
                    periode=periode,
                    est_valide=True
                ):
                    if cours_existant.professeur == professeur or cours_existant.salle == salle:
                        conflit = True
                        break

                if not conflit:
                    Cours.objects.create(
                        matiere=matiere,
                        professeur=professeur,
                        groupe=groupe,
                        salle=salle,
                        periode=periode,
                        semaine=semaine,
                        est_valide=True
                    )

        self.stdout.write(self.style.SUCCESS("Base de données remplie avec succès !")) 