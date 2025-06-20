#Imports externes
from django.shortcuts import render,\
                            HttpResponseRedirect,\
                            redirect,\
                            get_object_or_404
from django.http import FileResponse
from decimal import Decimal
from datetime import datetime,\
                        date

#Imports internes
from Internet.views import dateTimeParis
from Intranet.views import getLoggedMemberFromRequest
from Intranet.models import Vol,\
                            Aeronef,\
                            Member,\
                            BudgetLigne,\
                            BudgetOperation
from Intranet.MenuComptesPilotes.forms import monVolForm,\
                                                volForm,\
                                                comptePiloteChoiceForm,\
                                                carnetVolChoiceForm
from Intranet.MenuComptesPilotes.CalcComptesPilotes import calcPrixVol,\
                                                            calcTarifInstruction,\
                                                            calcChargeComptePilote
from Intranet.MenuComptesPilotes import config
from Intranet.MenuComptesPilotes.genererPdf import genererBufferComptePilote
                                                            
#************************************************************************************************************
#Gestion compte pilote du loggedMember
    #Comptes pilotes/Gérer mes vols
        #Création d'un vol du loggedMember
def intranetMonVolCreate(request):
    loggedMember = getLoggedMemberFromRequest(request)
    if loggedMember:
        templateName = 'intranetMonVolCreate.html'
        context = {'loggedMember' : loggedMember,
                   'current_date_time' : dateTimeParis(),
                   'actionBtnName' : 'Créer vol',
                   'allAeronef' : Aeronef.objects.all(),
                   }
        #Liste des vols du loggedMember
        volAll = Vol.objects.filter(pilote = loggedMember)
        context['volAll'] = volAll
        if request.method == 'POST':
            form = monVolForm(request.POST)
            if form.is_valid():
                if config.idMonVol == 0:
                    activeVol = Vol()
                    MonVolRegister(request, form, loggedMember, activeVol)
                    volAll = Vol.objects.filter(pilote = loggedMember)
                    loggedMember.chargeComptePilote = calcChargeComptePilote(loggedMember, volAll)
                    loggedMember.save()
                else:
                    activeVol = Vol.objects.get(pk = config.idMonVol)
                    MonVolRegister(request, form, loggedMember, activeVol)
                    volAll = Vol.objects.filter(pilote = loggedMember)
                    loggedMember.chargeComptePilote = calcChargeComptePilote(loggedMember, volAll)
                    loggedMember.save() 
                    config.idMonVol = 0           
                return HttpResponseRedirect(request.path)
        else:
            form = monVolForm()
        context['form'] = form        
        return render(request, templateName, context)
    else:
        return redirect('/internetAccueil')
    
        #Fonction d'enregistrement des items d'un vol du loggedMember
def MonVolRegister(request, form, pilote, activeVol):
    activeVol.date = request.POST.get('date')
    activeVol.aeronef = form.cleaned_data['aeronef']
    activeVol.textVVent = request.POST.get('textVVent')
    activeVol.textAltitude = request.POST.get('textAltitude')
    activeVol.textStress = request.POST.get('textStress')
    activeVol.textDecollage = request.POST.get('textDecollage')
    activeVol.textVol = request.POST.get('textVol')
    activeVol.textVNav = request.POST.get('textVNav')
    activeVol.textRadio = request.POST.get('textRadio')
    activeVol.textAtterrissage = request.POST.get('textAtterrissage')
    activeVol.textTdp = request.POST.get('textTdp')
    activeVol.textBaseULM = request.POST.get('textBaseULM')
    activeVol.textCommentaire = request.POST.get('textCommentaire')
    if activeVol.instructeur == '':
        activeVol.instructeur = None
    else:
        activeVol.instructeur = request.POST.get('instructeur')
    activeVol.horoInit = Decimal(request.POST.get('horoInit'))
    activeVol.horoFin = Decimal(request.POST.get('horoFin'))
    activeVol.pilote = pilote
    activeVol.indemInstructeur = form.cleaned_data['indemInstructeur']
    activeVol.bapteme = form.cleaned_data['bapteme']
    activeVol.maintenance = form.cleaned_data['maintenance']
    activeVol.prixVol = calcPrixVol(activeVol.dureeVol, activeVol.instructeur, activeVol.aeronef)
    activeVol.tarifInstruction = calcTarifInstruction(activeVol.dureeVol, activeVol.instructeur, activeVol.indemInstructeur)
    activeVol.save()

        #Suppression d'un vol du loggedMember    
def intranetMonVolDelete(request, id):
    loggedMember = getLoggedMemberFromRequest(request)
    if loggedMember:
        if request.method == 'POST':
            activeVol = Vol.objects.get(pk=id)
            #On diminue le compte pilote du vol à supprimer et on enregistre
            prixVol = activeVol.prixVol + activeVol.tarifInstruction - activeVol.remise
            loggedMember.chargeComptePilote = loggedMember.chargeComptePilote - prixVol
            loggedMember.save()
            activeVol.delete()
            return HttpResponseRedirect("/intranetMonVolCreate")
    else:
        return redirect('/internetAccueil')
    
        #Modification d'un vol du loggedMember
def intranetMonVolModify(request, id):
    loggedMember = getLoggedMemberFromRequest(request)
    if loggedMember:
        templateName ='intranetMonVolCreate.html'
        context = {
            'loggedMember' : loggedMember,
            'current_date_time' :dateTimeParis(),
            'actionBtnName' : 'Modifier le vol',
            'allAeronef' : Aeronef.objects.all(),
            }
        volAll = Vol.objects.filter(pilote = loggedMember)
        context['volAll'] = volAll
        config.idMonVol = id
        if request.method == 'POST':
            activeVol = Vol.objects.get(pk=config.idMonVol)
            form = monVolForm(initial = {
                'date' : activeVol.date,
                'aeronef' : activeVol.aeronef,
                'textVVent' : activeVol.textVVent,
                'textAltitude' : activeVol.textAltitude,
                'textStress' : activeVol.textStress,
                'textDecollage' : activeVol.textDecollage,
                'textVol' : activeVol.textVol,
                'textNav' : activeVol.textNav,
                'textRadio' : activeVol.textRadio,
                'textAtterrissage' : activeVol.textAtterrissage,
                'textTdp' : activeVol.textTdp,
                'textBaseULM': activeVol.textBaseULM,
                'textCommentaire' : activeVol.textCommentaire,
                'instructeur' : activeVol.instructeur,
                'indemInstructeur' : activeVol.indemInstructeur,
                'bapteme' : activeVol.bapteme,
                'maintenance' : activeVol.maintenance,
                'horoInit' : activeVol.horoInit,
                'horoFin' : activeVol.horoFin})
        context["form"] = form
        return render(request, templateName, context)  
    else:
        return redirect('/internetAccueil')

    #Comptes pilotes/Mon carnet de vol AUV
        #Affichage carnet de vol du loggedMember   
def intranetMonCarnetVol(request):
    loggedMember = getLoggedMemberFromRequest(request)
    if loggedMember:
        templateName = 'intranetMonCarnetVol.html'
        context = {'loggedMember' : loggedMember,
                   'current_date_time' : dateTimeParis(),
                   'current_year' : datetime.now().year,
                   'allAeronef' : Aeronef.objects.all(),
                   }      
        volAllPilote = Vol.objects.filter(pilote = loggedMember,
                                          date__year = datetime.now().year,
                                          instructeur = None)
        dureeVolAllPilote = totalTempsVol(volAllPilote)
        context['volAllPilote'] = volAllPilote
        context['dureeVolAllPilote'] = str(dureeVolAllPilote[0]) + ' heures ' + str(dureeVolAllPilote[1])  + ' minutes'
        volAllEleve = Vol.objects.filter(pilote = loggedMember,
                                         date__year = datetime.now().year).exclude(instructeur = None)
        dureeVolAllEleve = totalTempsVol(volAllEleve)
        context['volAllEleve'] = volAllEleve
        context['dureeVolAllEleve'] = str(dureeVolAllEleve[0]) + ' heures ' + str(dureeVolAllEleve[1])  + ' minutes'   
        return render(request, templateName, context)
    else:
        return redirect('/internetAccueil')  

        #Calcul temps total de vol pour le carnet de vol
def totalTempsVol(listVol): 
    temps = 0
    for vol in listVol :
        temps += vol.dureeVol 
    temps = divmod(temps, 60)  
    return temps

    #Comptes pilotes/Mon Compte pilote
def intranetMonComptePilote(request):            
    loggedMember = getLoggedMemberFromRequest(request)
    if loggedMember:
        templateName = 'intranetMonComptePilote.html'
        context = {
            'loggedMember' : loggedMember,
            'current_date_time' : dateTimeParis(),
            'current_year' : datetime.now().year,
            'allAeronef' : Aeronef.objects.all(),
            }
        #Vols pilotes
        volPiloteList = Vol.objects.filter(pilote = loggedMember)
        context['volPiloteList']= volPiloteList
        #Vols location et instruction
        ligneLocation = BudgetLigne.objects.get(name = 'Vols location')
        ligneInstruction = BudgetLigne.objects.get(name = 'Vols instruction')
        operationMemberAll = BudgetOperation.objects.filter(beneficiaire = loggedMember)
        if loggedMember.reportComptePilote2024 > 0 :
            charge = 0.00
            produit = loggedMember.reportComptePilote2024  
        else:
            charge = loggedMember.reportComptePilote2024
            produit = 0.00
        ligneReport = BudgetOperation(date = date(2025,1,1),
                                      charge = charge,
                                      produit = produit)
        paiementVolList = [ligneReport] 
        for operation in operationMemberAll :
            if operation.ligne == ligneLocation or operation.ligne == ligneInstruction :
                paiementVolList.append(operation)
        paiementVolList = sorted(paiementVolList, key = lambda ligneVol:ligneVol.date, reverse = True)                           
        context['paiementVolList'] = paiementVolList
        return render(request, templateName, context)
    else:
        return redirect('/internetAccueil')

#************************************************************************************************************
#Gestion compte pilote par administrateur
    #Comptes pilotes/Gérer les vols
        #Création d'un vol pilote
def intranetVolCreate(request):
    loggedMember = getLoggedMemberFromRequest(request)
    if loggedMember:
        templateName = 'intranetVolCreate.html'
        context = {'loggedMember' : loggedMember,
                   'current_date_time' : dateTimeParis(),
                   'actionBtnName' : 'Enregistrer vol',
                   'allAeronef' : Aeronef.objects.all(),
                   }
        volAll = Vol.objects.all()
        context['volAll'] = volAll
        if request.method == 'POST':
            form = volForm(request.POST)
            if form.is_valid():
                if config.idVol == 0:
                    activeVol = Vol()
                    activePilote = form.cleaned_data['pilote']
                    volRegister(request, form, activePilote, activeVol)
                    volAllActivePilote = Vol.objects.filter(pilote = activePilote)
                    activePilote.chargeComptePilote = calcChargeComptePilote(activePilote, volAllActivePilote)
                    activePilote.save()
                else:
                    activeVol = Vol.objects.get(pk = config.idVol)
                    activePilote = activeVol.pilote
                    volRegister(request, form, activePilote, activeVol)
                    volAllActivePilote = Vol.objects.filter(pilote=activePilote)
                    activePilote.chargeComptePilote = calcChargeComptePilote(activePilote, volAllActivePilote)
                    activePilote.save()
                    config.idVol = 0
                return HttpResponseRedirect(request.path)
        else:
            form = volForm()
        context['form'] = form        
        return render(request, templateName, context)
    else:
        return redirect('/internetAccueil')

        #Fonction d'enregistrement des items d'un vol pilote
def volRegister(request, form, pilote, activeVol):
    activeVol.date = request.POST.get('date')
    activeVol.aeronef = form.cleaned_data['aeronef']
    activeVol.texte = request.POST.get('text')
    
    if activeVol.instructeur == '':
        activeVol.instructeur = None
    else:
        activeVol.instructeur = request.POST.get('instructeur')
    activeVol.horoInit = Decimal(request.POST.get('horoInit'))
    activeVol.horoFin = Decimal(request.POST.get('horoFin'))
    activeVol.pilote = pilote
    activeVol.textVVent = request.POST.get('textVVent')
    activeVol.textAltitude = request.POST.get('textAltitude')
    activeVol.textStress = request.POST.get('textStress')
    activeVol.textDecollage = request.POST.get('textDecollage')
    activeVol.textVol = request.POST.get('textVol')
    activeVol.textVNav = request.POST.get('textVNav')
    activeVol.textRadio = request.POST.get('textRadio')
    activeVol.textAtterrissage = request.POST.get('textAtterrissage')
    activeVol.textTdp = request.POST.get('textTdp')
    activeVol.textBaseULM = request.POST.get('textBaseULM')
    activeVol.textCommentaire = request.POST.get('textCommentaire')
    if activeVol.instructeur == '':
        activeVol.instructeur = None
    else:
        activeVol.instructeur = request.POST.get('instructeur')
    activeVol.indemInstructeur = form.cleaned_data['indemInstructeur']
    activeVol.bapteme = form.cleaned_data['bapteme']
    activeVol.maintenance = form.cleaned_data['maintenance']
    activeVol.prixVol = calcPrixVol(activeVol.dureeVol, activeVol.instructeur, activeVol.aeronef)
    #Si vol découverte ou vol maintenance, remise automatique du prix du vol
    if (activeVol.bapteme.id == 2) or (activeVol.maintenance.id == 2):
        activeVol.remise = activeVol.prixVol
    else:
        activeVol.remise = Decimal(request.POST.get('remise')) 
    activeVol.tarifInstruction = calcTarifInstruction(activeVol.dureeVol, activeVol.instructeur, activeVol.indemInstructeur)
    activeVol.save()
    
        #Suppression d'un vol pilote    
def intranetVolDelete(request, id):
    loggedMember = getLoggedMemberFromRequest(request)
    if loggedMember:
        if request.method == 'POST':
            activeVol = Vol.objects.get(pk=id)
            pilote = activeVol.pilote
            prixVol = activeVol.prixVol + activeVol.tarifInstruction - activeVol.remise
            pilote.chargeComptePilote = pilote.chargeComptePilote - prixVol
            pilote.save()
            activeVol.delete()
            return HttpResponseRedirect("/intranetVolCreate")
    else:
        return redirect('/internetAccueil')
    
        #Modification d'un vol pilote
def intranetVolModify(request, id):
    loggedMember = getLoggedMemberFromRequest(request)
    if loggedMember:
        templateName ='intranetVolCreate.html'
        context = {
            'loggedMember' : loggedMember,
            'current_date_time' :dateTimeParis(),
            'actionBtnName' : 'Modifier le vol',
            'allAeronef' : Aeronef.objects.all(),
            }
        volAll = Vol.objects.all()
        context['volAll'] = volAll
        config.idVol = id
        if request.method == 'POST':
            activeVol = Vol.objects.get(pk=config.idVol)
            form = volForm(initial = {
                'date' : activeVol.date,
                'aeronef' : activeVol.aeronef,
                'pilote' : activeVol.pilote,
                'textVVent' : activeVol.textVVent,
                'textAltitude' : activeVol.textAltitude,
                'textStress' : activeVol.textStress,
                'textDecollage' : activeVol.textDecollage,
                'textVol' : activeVol.textVol,
                'textNav' : activeVol.textNav,
                'textRadio' : activeVol.textRadio,
                'textAtterrissage' : activeVol.textAtterrissage,
                'textTdp' : activeVol.textTdp,
                'textBaseULM': activeVol.textBaseULM,
                'textCommentaire' : activeVol.textCommentaire,
                'instructeur' : activeVol.instructeur,
                'indemInstructeur' : activeVol.indemInstructeur,
                'bapteme' : activeVol.bapteme,
                'maintenance' : activeVol.maintenance,
                'remise' : activeVol.remise,
                'horoInit' : activeVol.horoInit,
                'horoFin' : activeVol.horoFin})
        context["form"] = form
        return render(request, templateName, context)  
    else:
        return redirect('/internetAccueil')

    #Comptes pilotes/Carnets de vol
        #Choisir un pilote
def intranetCarnetVolChoice(request):
    loggedMember = getLoggedMemberFromRequest(request)
    if loggedMember:
        templateName = 'intranetCarnetVolChoice.html'
        context = {
            'loggedMember' : loggedMember,
            'current_date_time' : dateTimeParis(),
            'current_year' : datetime.now().year,
            'actionBtnName' : 'Choisir Carnet de vol',
            'allAeronef' : Aeronef.objects.all(),
            }
        if request.method == "POST":
            form = comptePiloteChoiceForm(request.POST)
            if form.is_valid():
                activePilote = form.cleaned_data['pilote'] 
                IdPilote = activePilote.id
                return redirect('intranet_Carnet_Vol', id = IdPilote)
        else:
            form = carnetVolChoiceForm()   
            context['form'] = form     
            return render(request, templateName, context)
    else:
        return redirect('/internetAccueil')

    #Afficher Carnet de vol
def intranetCarnetVol(request, id):            
    loggedMember = getLoggedMemberFromRequest(request)
    if loggedMember:
        templateName = 'intranetCarnetVol.html'
        context = {
            'loggedMember' : loggedMember,
            'current_date_time' : dateTimeParis(),
            'current_year' : datetime.now().year,
            'allAeronef' : Aeronef.objects.all(),
            }
        
        activePilote = get_object_or_404(Member, pk=id)
        context['activePilote'] = activePilote
        volAllPilote = Vol.objects.filter(pilote = activePilote,
                                          date__year = datetime.now().year,
                                          instructeur = None)
        dureeVolAllPilote = totalTempsVol(volAllPilote)
        context['volAllPilote'] = volAllPilote
        context['dureeVolAllPilote'] = str(dureeVolAllPilote[0]) + ' heures ' + str(dureeVolAllPilote[1])  + ' minutes'
        volAllEleve = Vol.objects.filter(pilote = activePilote,
                                         date__year = datetime.now().year).exclude(instructeur = None)
        dureeVolAllEleve = totalTempsVol(volAllEleve)
        context['volAllEleve'] = volAllEleve
        context['dureeVolAllEleve'] = str(dureeVolAllEleve[0]) + ' heures ' + str(dureeVolAllEleve[1])  + ' minutes'   
        return render(request, templateName, context)
    else:
        return redirect('/internetAccueil')
    
    #Comptes pilotes/Comptes pilotes
        #Choisir un pilote
def intranetComptePiloteChoice(request):
    loggedMember = getLoggedMemberFromRequest(request)
    if loggedMember:
        templateName = 'intranetComptePiloteChoice.html'
        context = {
            'loggedMember' : loggedMember,
            'current_date_time' : dateTimeParis(),
            'current_year' : datetime.now().year,
            'actionBtnName' : 'Choisir Compte Pilote',
            'allAeronef' : Aeronef.objects.all(),
            }
        if request.method == "POST":
            form = comptePiloteChoiceForm(request.POST)
            if form.is_valid():
                activePilote = form.cleaned_data['pilote'] 
                IdPilote = activePilote.id
                return redirect('intranet_Compte_Pilote', id = IdPilote)
        else:
            form = comptePiloteChoiceForm()   
            context['form'] = form     
            return render(request, templateName, context)
    else:
        return redirect('/internetAccueil')

        #Afficher Compte pilote
def intranetComptePilote(request, id):            
    loggedMember = getLoggedMemberFromRequest(request)
    if loggedMember:
        templateName = 'intranetComptePilote.html'
        context = {
            'loggedMember' : loggedMember,
            'current_date_time' : dateTimeParis(),
            'current_year' : datetime.now().year,
            'allAeronef' : Aeronef.objects.all(),
            }
        activePilote = get_object_or_404(Member, pk=id)
        context['activePilote'] = activePilote
        #Vols pilotes
        volPiloteList = Vol.objects.filter(pilote = activePilote)
        context['volPiloteList']= volPiloteList
        #Vols location et instruction
        ligneLocation = BudgetLigne.objects.get(name = 'Vols location')
        ligneInstruction = BudgetLigne.objects.get(name = 'Vols instruction')
        operationMemberAll = BudgetOperation.objects.filter(beneficiaire = activePilote)
        if activePilote.reportComptePilote2024 > 0 :
            charge = 0.00
            produit = activePilote.reportComptePilote2024  
        else:
            charge = activePilote.reportComptePilote2024
            produit = 0.00
        ligneReport = BudgetOperation(date = date(2025,1,1),
                                      charge = charge,
                                      produit = produit)
        paiementVolList = [ligneReport] 
        for operation in operationMemberAll :
            if operation.ligne == ligneLocation or operation.ligne == ligneInstruction :
                paiementVolList.append(operation)
        paiementVolList = sorted(paiementVolList, key = lambda ligneVol:ligneVol.date, reverse = True)                           
        context['paiementVolList'] = paiementVolList
        return render(request, templateName, context)
    else:
        return redirect('/internetAccueil')
    
        #Générer PDF compte pilote
def pdfComptePilote(request, id): 
    buffer = genererBufferComptePilote(id)
    myPilote = Member.objects.get(pk = id)
    filename = str(myPilote) + '_' + str(date.today()) + ".pdf"
    return FileResponse(buffer, as_attachment=True, filename = filename)
    
    
    #Comptes pilotes/Bilan comptes pilotes
def intranetBilanComptePilote(request):                    
    loggedMember = getLoggedMemberFromRequest(request)
    if loggedMember:
        templateName = 'intranetBilanComptePilote.html'
        context = {
            'loggedMember' : loggedMember,
            'current_date_time' : dateTimeParis(),
            'current_year' : datetime.now().year,
            'allAeronef' : Aeronef.objects.all(),
            }
        allMember = Member.objects.all()
        totalProduit = 0
        totalCharge = 0
        totalBilan = 0
        for member in allMember:
            totalProduit += member.produitComptePilote
            totalCharge += member.chargeComptePilote
            totalBilan += member.bilanComptePilote
        context['totalProduit'] = totalProduit
        context['totalCharge'] = totalCharge
        context['totalBilan'] = totalBilan
        context['allMember'] = allMember
        return render(request, templateName, context)
    else:
        return redirect('/internetAccueil')