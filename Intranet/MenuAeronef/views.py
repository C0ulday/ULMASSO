#Imports externes
from django.shortcuts import render,\
                            redirect,\
                            HttpResponseRedirect
from datetime import datetime
from math import floor

#Imports internes
from Internet.views import dateTimeParis
from Intranet.views import getLoggedMemberFromRequest
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