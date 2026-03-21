#Imports externes
from django.shortcuts import render,\
                            redirect,\
                            HttpResponseRedirect
from datetime import datetime, date
from math import floor

#Imports internes
from Internet.views import dateTimeParis
from Intranet.views import getLoggedMemberFromRequest, _jours_restants, _statut_maintenance
from Intranet.models import Aeronef,\
                            Vol,\
                            BudgetOperation
from Intranet.MenuAeronef.forms import gererAeronefForm,\
                                        aeronefListForm
from Intranet.MenuAeronef import calcAeronef
                                                            
#************************************************************************************************************
#Aeronefs/Paramètres
    #Créer aéronef
def intranetAeronefCreate(request):
    loggedMember = getLoggedMemberFromRequest(request)
    if loggedMember:
        templateName = 'intranetAeronefCreate.html'
        context = {'loggedMember' : loggedMember,
                   'current_date_time' : dateTimeParis(),
                   'actionBtnName' : 'Créer ULM',
                   'allAeronef' : Aeronef.objects.all(),
                   }
        listAeronef = Aeronef.objects.all()
        context['listAeronef'] = listAeronef
        if request.method == 'POST':
            form = gererAeronefForm(request.POST)
            if form.is_valid():
                if listAeronef:
                    typeULM = request.POST.get('type')
                    activeAeronefList = Aeronef.objects.filter(type = typeULM)
                    #Si l'aéronef existe, on le modifie
                    if activeAeronefList:
                        activeAeronef = activeAeronefList[0]#activeSectionList est un queryset. On récupère le premier
                        activeAeronef.typeULM = request.POST.get('type')
                        activeAeronef.classeULM = form.cleaned_data['classeULM']
                        activeAeronef.immatriculation = request.POST.get('immatriculation')
                        activeAeronef.indicatifRadio = request.POST.get('indicatifRadio')
                        activeAeronef.limiteAptitudeVol = form.cleaned_data['limiteAptitudeVol']
                        activeAeronef.limiteLSA = form.cleaned_data['limiteLSA']
                        activeAeronef.limiteParachute = form.cleaned_data['limiteParachute']
                        activeAeronef.tarifPilote = request.POST.get('tarifPilote')
                        activeAeronef.tarifElevePilote = request.POST.get('tarifElevePilote')
                        activeAeronef.save()
                    #Sinon, on le crée
                    else:
                        form.save()
                #Si aucun n'existe
                else:
                    form.save()
            #Evite de créer le même objet quand on rafraichit la page
            return HttpResponseRedirect(request.path) 
        else:
            form = gererAeronefForm()
        context["form"] = form
        return render(request, templateName, context)     
    else:
        return redirect('/internetAccueil')

    #Supprimer aéronef
def intranetAeronefDelete(request, id):
    loggedMember = getLoggedMemberFromRequest(request)
    if loggedMember:
        if request.method == 'POST':
            activeAeronef = Aeronef.objects.get(pk=id)
            activeAeronef.delete()
            return HttpResponseRedirect("/intranetAeronefCreate")
    else:
        return redirect('/internetAccueil')    
    
    #Modifier aéronef
def intranetAeronefModify(request, id):
    loggedMember = getLoggedMemberFromRequest(request)
    if loggedMember:
        templateName ='intranetAeronefCreate.html'
        context = {
            'loggedMember' : loggedMember,
            'current_date_time' :dateTimeParis(),
            'actionBtnName' : 'Modifier l\'ULM',
            'allAeronef' : Aeronef.objects.all(),
            }
        listAeronef = Aeronef.objects.all()
        context['listAeronef'] = listAeronef
        if request.method == 'POST':
            activeAeronef = Aeronef.objects.get(pk=id)
            form = gererAeronefForm(instance = activeAeronef)
        context["form"] = form
        return render(request, templateName, context)  
    else:
        return redirect('/internetAccueil')
    
def intranetAeronefSuiviMecanique(request):
    loggedMember = getLoggedMemberFromRequest(request)
    if not loggedMember:
        return redirect('/internetAccueil')

    current_year = datetime.now().year
    templateName = 'intranetAeronefSuiviMecanique.html'

    aeronefs_suivi = []
    alertes = []

    for aeronef in Aeronef.objects.all():
        # Dates de maintenance
        j_apt = _jours_restants(aeronef.limiteAptitudeVol)
        j_lsa = _jours_restants(aeronef.limiteLSA)
        j_par = _jours_restants(aeronef.limiteParachute)

        badge_apt, classe_apt = _statut_maintenance(j_apt)
        badge_lsa, classe_lsa = _statut_maintenance(j_lsa)
        badge_par, classe_par = _statut_maintenance(j_par)

        # Alertes sidebar
        for label, jours, badge in [
            ('Aptitude au vol', j_apt, badge_apt),
            ('Limites LSA',     j_lsa, badge_lsa),
            ('Parachute',       j_par, badge_par),
        ]:
            if badge in ('danger', 'warning'):
                if jours is not None and jours < 0:
                    alertes.append({'niveau': 'danger',
                                    'message': f'{aeronef.type} — {label} : expiré depuis {abs(jours)}j'})
                elif jours is not None and jours <= 30:
                    alertes.append({'niveau': 'danger',
                                    'message': f'{aeronef.type} — {label} : expire dans {jours}j'})
                else:
                    alertes.append({'niveau': 'warning',
                                    'message': f'{aeronef.type} — {label} : expire dans {jours}j'})

        # Statistiques vols année en cours
        vols_annee = Vol.objects.filter(aeronef=aeronef, date__year=current_year)
        nb_vols = vols_annee.count()
        total_min = sum(v.dureeVol for v in vols_annee)
        tps_h   = floor(total_min / 60)
        tps_min = total_min % 60

        dernier_vol_obj = vols_annee.order_by('-date').first()
        dernier_vol  = dernier_vol_obj.date if dernier_vol_obj else None
        dernier_horo = dernier_vol_obj.horoFin if dernier_vol_obj else None

        # Âge de l'aéronef
        age_aeronef = None
        if aeronef.date:
            age_aeronef = floor((date.today() - aeronef.date).days / 365.25)

        aeronefs_suivi.append({
            'aeronef':          aeronef,
            'jours_aptitude':   j_apt,
            'jours_lsa':        j_lsa,
            'jours_parachute':  j_par,
            'badge_aptitude':   badge_apt,
            'badge_lsa':        badge_lsa,
            'badge_parachute':  badge_par,
            'classe_aptitude':  classe_apt,
            'classe_lsa':       classe_lsa,
            'classe_parachute': classe_par,
            'nb_vols':          nb_vols,
            'tps_vol_h':        tps_h,
            'tps_vol_min':      tps_min,
            'dernier_vol':      dernier_vol,
            'dernier_horo':     dernier_horo,
            'age_aeronef':      age_aeronef,
        })

    context = {
        'loggedMember':    loggedMember,
        'current_date_time': dateTimeParis(),
        'current_year':    current_year,
        'allAeronef':      Aeronef.objects.all(),
        'aeronefs_suivi':  aeronefs_suivi,
        'alertes':         alertes,
    }
    return render(request, templateName, context)


def intranetAeronefStatistiques(request):
    loggedMember = getLoggedMemberFromRequest(request)
    if loggedMember:
        templateName = 'intranetAeronefStatistiques.html'
        context = {'loggedMember' : loggedMember,
                    'current_date_time' : dateTimeParis(),
                    'current_year' : datetime.now().year,
                    'actionBtnName' : 'Statistiques Aéronef',
                    'allAeronef' : Aeronef.objects.all(),
                   }
        allVolCurrentYear = Vol.objects.filter(date__year = datetime.now().year)
        allBudgetOpCurrentYear = BudgetOperation.objects.filter(date__year = datetime.now().year, ligne__name = 'Carburant')
        if request.method == 'POST':
            form = aeronefListForm(request.POST)
            myAeronef = request.POST.get('aeronefSelect')
            context['aeronef'] = myAeronef
            allVol = allVolCurrentYear.filter(aeronef = myAeronef)
            allOpCarburant = allBudgetOpCurrentYear.filter(aeronef = myAeronef)
            #Calcul du nombre d'heures de vol
            tpsVol = calcAeronef.calcTpsVol(allVol) #[HH, MM]
            context['tpsVol'] = tpsVol
            #Calcul du volume de carburant
            volume = calcAeronef.calcVolEssence(allOpCarburant)
            context['volumeCarburant'] = volume
            #Calcul de la consommation
            context['consommation'] = calcAeronef.calcConsommation(tpsVol, volume)
            #Temps de vol par type
            tpsTypeVolMM = calcAeronef.calcTpsTypeVol(allVol)
            tpsTypeVolPercent = []
            tpsTypeVolHHMM = []
            if tpsTypeVolMM:
                for data in tpsTypeVolMM:
                    if sum(tpsTypeVolMM) > 0 :
                        tpsTypeVolPercent.append(floor(data*100/sum(tpsTypeVolMM)))
                        tpsTypeVolHHMM.append(calcAeronef.calcTpsHHMM(data))
            colors = ['red', 'blue', 'green', 'yellow']
            labels = ['Maintenance','Découverte','Instruction', 'Location']
            context['tpsTypeVolPercent'] = tpsTypeVolPercent
            context['label'] = labels 
            context['colors'] = colors  
            context['tpsTypeVol'] = tpsTypeVolHHMM
        else:
            form = aeronefListForm()
        context["form"] = form
        return render(request, templateName, context)
    else:
        return redirect('/internetAccueil')