from django.contrib import admin
from .models import Domaine, Specialite, Professeur, Matiere, Salle, Groupe, PeriodeHoraire

admin.site.register(Domaine)
admin.site.register(Specialite)
admin.site.register(Professeur)
admin.site.register(Matiere)
admin.site.register(Salle)
admin.site.register(Groupe)
admin.site.register(PeriodeHoraire)
