from django.urls import path
from . import views

urlpatterns = [
    path('', views.calendrier, name='calendrier'),
    path('cours/<int:groupe_id>/<int:semaine>/', views.get_cours, name='get_cours'),
    path('update-cours/', views.update_cours, name='update_cours'),
] 