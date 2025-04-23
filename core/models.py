from django.db import models

# Create your models here.

class Domaine(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom

class Specialite(models.Model):
    nom = models.CharField(max_length=100)
    domaine = models.ForeignKey(Domaine, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nom} ({self.domaine.nom})"

class Professeur(models.Model):
    nom = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return self.nom

class Matiere(models.Model):
    nom = models.CharField(max_length=100)
    specialite = models.ForeignKey(Specialite, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nom} - {self.specialite.nom}"

class Salle(models.Model):
    nom = models.CharField(max_length=100)
    capacite = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.nom

class Groupe(models.Model):
    nom = models.CharField(max_length=100)
    specialite = models.ForeignKey(Specialite, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nom} - {self.specialite.nom}"

class PeriodeHoraire(models.Model):
    JOURS_SEMAINE = [
        ('Lundi', 'Lundi'),
        ('Mardi', 'Mardi'),
        ('Mercredi', 'Mercredi'),
        ('Jeudi', 'Jeudi'),
        ('Vendredi', 'Vendredi'),
        ('Samedi', 'Samedi'),
        ('Dimanche', 'Dimanche'),
    ]
    
    jour = models.CharField(max_length=10, choices=JOURS_SEMAINE)
    heure_debut = models.TimeField()
    heure_fin = models.TimeField()

    def __str__(self):
        return f"{self.jour} - {self.heure_debut} à {self.heure_fin}"
