from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from core.models import Groupe, PeriodeHoraire
from .models import Cours
import random
from datetime import time

def calendrier(request):
    groupes = Groupe.objects.all()
    # Récupérer la semaine depuis l'URL, par défaut 1
    semaine = request.GET.get('semaine', 1)
    try:
        semaine = int(semaine)
    except ValueError:
        semaine = 1
    
    # Récupérer uniquement les périodes du lundi pour éviter la duplication
    periodes = PeriodeHoraire.objects.filter(jour='Lundi').order_by('heure_debut')
    jours_semaine = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi']
    
    return render(request, 'planning/calendrier.html', {
        'groupes': groupes,
        'periodes': periodes,
        'jours_semaine': jours_semaine,
        'semaine_actuelle': semaine,
    })

def get_cours(request, groupe_id, semaine):
    # Récupérer tous les cours du groupe et de la semaine
    cours = Cours.objects.filter(
        groupe_id=groupe_id,
        semaine=semaine,
        est_valide=True
    ).select_related('matiere', 'professeur', 'salle', 'periode')

    # Debug: Afficher les cours récupérés
    print(f"Nombre de cours trouvés pour le groupe {groupe_id}, semaine {semaine}: {cours.count()}")
    for c in cours:
        print(f"Cours: {c.matiere.nom} - {c.periode.jour} - {c.periode.heure_debut}-{c.periode.heure_fin}")

    cours_data = []
    for c in cours:
        cours_data.append({
            'id': c.id,
            'jour': c.periode.jour,
            'periode_id': c.periode.id,
            'matiere': c.matiere.nom,
            'professeur': c.professeur.nom,
            'salle': c.salle.nom,
            'heure_debut': c.periode.heure_debut.strftime('%H:%M'),
            'heure_fin': c.periode.heure_fin.strftime('%H:%M')
        })

    return JsonResponse(cours_data, safe=False)

def trouver_suggestions(cours, periode_id, semaine):
    """Trouve des créneaux disponibles pour un cours donné."""
    suggestions = []
    
    # Récupérer tous les cours de la même semaine
    cours_semaine = Cours.objects.filter(
        semaine=semaine,
        est_valide=True
    ).select_related('periode')
    
    # Récupérer les périodes déjà utilisées par le professeur ou la salle
    periodes_utilisees = set()
    for c in cours_semaine:
        if c.professeur == cours.professeur or c.salle == cours.salle:
            periodes_utilisees.add(c.periode.id)
    
    # Trouver toutes les périodes disponibles
    periodes_disponibles = PeriodeHoraire.objects.exclude(id__in=periodes_utilisees)
    
    # Créer des suggestions
    for periode in periodes_disponibles:
        suggestions.append({
            'jour': periode.jour,
            'periode_id': periode.id
        })
    
    return suggestions

@csrf_exempt
@require_http_methods(["POST"])
def update_cours(request):
    try:
        import json
        data = json.loads(request.body)
        
        cours_id = data.get('cours_id')
        jour = data.get('jour')
        periode_id = data.get('periode_id')
        semaine = data.get('semaine')
        
        if not all([cours_id, jour, periode_id, semaine]):
            return JsonResponse({'error': 'Données manquantes'}, status=400)
        
        try:
            cours = Cours.objects.get(id=cours_id)
            periode = PeriodeHoraire.objects.get(id=periode_id)
            
            # Vérifier les conflits
            conflit_prof = Cours.objects.filter(
                semaine=semaine,
                periode=periode,
                professeur=cours.professeur,
                est_valide=True
            ).exclude(id=cours_id).exists()
            
            conflit_salle = Cours.objects.filter(
                semaine=semaine,
                periode=periode,
                salle=cours.salle,
                est_valide=True
            ).exclude(id=cours_id).exists()
            
            if conflit_prof or conflit_salle:
                message = "Professeur déjà occupé" if conflit_prof else "Salle déjà utilisée"
                if conflit_prof and conflit_salle:
                    message = "Professeur et salle déjà occupés"
                
                suggestions = trouver_suggestions(cours, periode_id, semaine)
                
                return JsonResponse({
                    'success': False,
                    'conflict': True,
                    'message': message,
                    'suggestions': suggestions
                })
            
            # Si pas de conflit, mettre à jour le cours
            cours.periode = periode
            cours.save()
            
            return JsonResponse({'success': True})
            
        except (Cours.DoesNotExist, PeriodeHoraire.DoesNotExist):
            return JsonResponse({'error': 'Cours ou période non trouvé'}, status=404)
            
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Données JSON invalides'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
