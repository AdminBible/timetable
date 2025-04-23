from django.db import models
from core.models import Matiere, Professeur, Groupe, Salle, PeriodeHoraire

class Cours(models.Model):
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE)
    professeur = models.ForeignKey(Professeur, on_delete=models.CASCADE)
    groupe = models.ForeignKey(Groupe, on_delete=models.CASCADE)
    salle = models.ForeignKey(Salle, on_delete=models.CASCADE)
    periode = models.ForeignKey(PeriodeHoraire, on_delete=models.CASCADE)
    semaine = models.IntegerField()
    date = models.DateField(null=True, blank=True)
    est_valide = models.BooleanField(default=False)

    def __str__(self):
        date_str = f" le {self.date}" if self.date else f" (semaine {self.semaine})"
        return f"{self.matiere.nom} - {self.professeur.nom} - {self.groupe.nom}{date_str} - {self.periode}"
