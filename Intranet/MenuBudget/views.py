#Imports externes
from django.shortcuts import render,\
                                HttpResponseRedirect,\
                                redirect,\
                                get_object_or_404
from django.http import FileResponse
from datetime import datetime

#Imports internes
from Intranet.MenuBudget.forms import budgetGererSectionForm,\
                                        budgetGererProjetForm,\
                                        budgetGererLigneForm,\
                                        budgetLigneChoiceForm,\
                                        budgetGererOperationForm,\
                                        budgetGererOperationLocInstForm,\
                                        budgetLigneListForm,\
                                        compteEpargneChoiceForm,\
                                        compteEpargneOperationForm,\
                                        compteEpargneListForm,\
                                        gererCompteEpargneForm,\
                                        budgetGenFactureForm,\
                                        budgetGenFactureClientForm,\
                                        budgetGenFactureOpForm,\
                                        budgetAeronefListForm
from Intranet.models import BudgetSection,\
                            BudgetProjet,\
                            BudgetLigne,\
                            BudgetOperation,\
                            BudgetBudget,\
                            CompteEpargne,\
                            CompteEpargneOperation,\
                            Facture,\
                            OperationFacture,\
                            Aeronef
from ULMASSO.views import dateTimeParis
from Intranet.views import getLoggedMemberFromRequest
from Intranet.MenuBudget.calcBudget import defineCodeOperation,\
                                            CalcAddBudget,\
                                            CalcSubBudget,\
                                            defineCodeCompteEpargneOperation,\
                                            CalcSubCompteEpargne,\
                                            CalcAddCompteEpargne,\
                                            defineCodeFacture
from Intranet.MenuBudget import config
from Intranet.MenuBudget.genererPdf import genererBufferFacture,\
                                            genererBufferBudget

#*********************************************************************************************************
#Budget/Gérer sections
    #Créer Sections
def intranetBudgetSectionAddShow(request):
    loggedMember = getLoggedMemberFromRequest(request)
    if loggedMember:
        templateName ='intranetBudgetGererSection.html'
        context = {
            'loggedMember' : loggedMember,
            'current_date_time' : dateTimeParis(),
            'current_year' : datetime.now().year,
            'actionBtnName' : 'Créer la section',
            'allAeronef' : Aeronef.objects.all(),
            }
        budgetSectionAll = BudgetSection.objects.all().order_by('code')
        context['budgetSectionAll'] = budgetSectionAll
        if request.method == 'POST':
            form = budgetGererSectionForm(request.POST)
            if form.is_valid():
                if config.idBudgetSection == 0:
                    form.save()
                else:
                    activeSection = BudgetSection.objects.get(pk = config.idBudgetSection)
                    activeSection.code=request.POST.get('code')
                    activeSection.name=request.POST.get('name')
                    activeSection.save()
                    config.idBudgetSection = 0
                return HttpResponseRedirect(request.path) #Evite de créer le même objet quand on rafraichit la page
        else:
            form = budgetGererSectionForm()
        context["form"] = form
        return render(request, templateName, context)   
    else:
        return redirect('/internetAccueil')

    #Supprimer Section
def intranetBudgetSectionDelete(request, id):
    loggedMember = getLoggedMemberFromRequest(request)
    if loggedMember:
        if request.method == 'POST':
            activeSection = BudgetSection.objects.get(pk=id)
            activeSection.delete()
            return HttpResponseRedirect("/intranetBudgetGererSection")
    else:
        return redirect('/internetAccueil')
    
    #Modifier Section
def intranetBudgetSectionModify(request, id):
    loggedMember = getLoggedMemberFromRequest(request)
    if loggedMember:
        templateName ='intranetBudgetGererSection.html'
        context = {
            'loggedMember' : loggedMember,
            'current_date_time' :dateTimeParis(),
            'actionBtnName' : 'Modifier la section',
            'allAeronef' : Aeronef.objects.all(),
            }
        budgetSectionAll = BudgetSection.objects.all().order_by('code')
        context['budgetSectionAll'] = budgetSectionAll
        config.idBudgetSection = id
        if request.method == 'POST':
            activeSection = BudgetSection.objects.get(pk=config.idBudgetSection)
            form = budgetGererSectionForm(instance = activeSection)
        context["form"] = form
        return render(request, templateName, context)  
    else:
        return redirect('/internetAccueil')

#*********************************************************************************************************
#Budget/Gérer Projets
    #Créer Projets
def intranetBudgetProjetAddShow(request):
    loggedMember = getLoggedMemberFromRequest(request)
    if loggedMember:
        templateName ='intranetBudgetGererProjet.html'
        context = {
            'loggedMember' : loggedMember,
            'current_date_time' : dateTimeParis(),
            'current_year' : datetime.now().year,
            'actionBtnName' : 'Créer le projet',
            'allAeronef' : Aeronef.objects.all(),
            }
        budgetProjetAll = BudgetProjet.objects.all().order_by('section','code')
        context['budgetProjetAll'] = budgetProjetAll
        if request.method == 'POST':
            form = budgetGererProjetForm(request.POST)
            if form.is_valid():
                if config.idBudgetProjet == 0:
                    form.save()
                else:
                    activeProjet = BudgetProjet.objects.get(pk = config.idBudgetProjet)
                    activeProjet.code = request.POST.get('code')
                    activeProjet.name = request.POST.get('name')
                    activeProjet.section = form.cleaned_data['section']
                    activeProjet.save()
                    config.idBudgetProjet = 0
                return HttpResponseRedirect(request.path) #Evite de créer le même objet quand on rafraichit la page
        else:
            form = budgetGererProjetForm()
        context["form"] = form
        return render(request, templateName, context) 
    else:
        return redirect('/internetAccueil')

    #Supprimer Projet
def intranetBudgetProjetDelete(request, id):
    loggedMember = getLoggedMemberFromRequest(request)
    if loggedMember:
        if request.method == 'POST':
            activeProjet = BudgetProjet.objects.get(pk=id)
            activeProjet.delete()
            return HttpResponseRedirect("/intranetBudgetGererProjet")
    else:
        return redirect('/internetAccueil')

    #Modifier Projet
def intranetBudgetProjetModify(request, id):
    loggedMember = getLoggedMemberFromRequest(request)
    if loggedMember:
        templateName ='intranetBudgetGererProjet.html'
        context = {
            'loggedMember' : loggedMember,
            'current_date_time' : dateTimeParis(),
            'current_year' : datetime.now().year,
            'actionBtnName' : 'Modifier le projet',
            'allAeronef' : Aeronef.objects.all(),
            }
        budgetProjetAll = BudgetProjet.objects.all().order_by('code')
        context['budgetProjetAll'] = budgetProjetAll
        config.idBudgetProjet = id
        if request.method == 'POST':
            activeProjet = BudgetProjet.objects.get(pk=config.idBudgetProjet)
            form = budgetGererProjetForm(instance = activeProjet)
        context["form"] = form
        return render(request, templateName, context)
    else:
        return redirect('/internetAccueil')

#*********************************************************************************************************
#Budget/Gérer Lignes
    #Créer Ligne
def intranetBudgetLigneAddShow(request):
    loggedMember = getLoggedMemberFromRequest(request)
    if loggedMember:
        templateName ='intranetBudgetGererLigne.html'
        context = {
            'loggedMember' : loggedMember,
            'current_date_time' : dateTimeParis(),
            'current_year' : datetime.now().year,
            'actionBtnName' : 'Créer la ligne',
            'allAeronef' : Aeronef.objects.all(),
            }
        budgetLigneAll = BudgetLigne.objects.all().order_by('-code')
        context['budgetLigneAll'] = budgetLigneAll
        if request.method == 'POST':
            form = budgetGererLigneForm(request.POST)             
            if form.is_valid():
                if config.idBudgetLigne == 0:
                    form.save()
                else:
                    activeLigne = BudgetLigne.objects.get(config.idBudgetLigne)
                    activeLigne.code = request.POST.get('code')
                    activeLigne.name = request.POST.get('name')
                    activeLigne.projet = form.cleaned_data['projet']
                    activeLigne.save()
                    config.idBudgetLigne = 0
                return HttpResponseRedirect(request.path) #Evite de créer le même objet quand on rafraichit la page
        else:
            form = budgetGererLigneForm()
        context["form"] = form
        return render(request, templateName, context)
    else:
        return redirect('/internetAccueil') 

    #Supprimer ligne
def intranetBudgetLigneDelete(request, id):
    loggedMember = getLoggedMemberFromRequest(request)
    if loggedMember:
        if request.method == 'POST':
            activeLigne = BudgetLigne.objects.get(pk=id)
            activeLigne.delete()
            return HttpResponseRedirect("/intranetBudgetGererLigne")
    else:
        return redirect('/internetAccueil') 

    #Modifier ligne
def intranetBudgetLigneModify(request, id):
    loggedMember = getLoggedMemberFromRequest(request)
    if loggedMember:
        templateName ='intranetBudgetGererLigne.html'
        context = {
            'loggedMember' : loggedMember,
            'current_date_time' : dateTimeParis(),
            'current_year' : datetime.now().year,
            'actionBtnName' : 'Modifier la ligne',
            'allAeronef' : Aeronef.objects.all(),
            }
        budgetLigneAll = BudgetLigne.objects.all().order_by('code')
        context['budgetLigneAll'] = budgetLigneAll
        config.idBudgetLigne = id
        if request.method == 'POST':
            activeLigne = BudgetLigne.objects.get(pk=config.idBudgetLigne)
            form = budgetGererLigneForm(instance = activeLigne)
        context["form"] = form
        return render(request, templateName, context)
    else:
        return redirect('/internetAccueil')    

#*********************************************************************************************************
#Budget/Gérer Opérations
    #Choisir ligne pour créer opération
def intranetBudgetLigneChoice(request):
    loggedMember = getLoggedMemberFromRequest(request)
    if loggedMember:
        templateName = 'intranetBudgetLigneChoice.html'
        context = {
            'loggedMember' : loggedMember,
            'current_date_time' : dateTimeParis(),
            'current_year' : datetime.now().year,
            'actionBtnName' : 'Choisir la ligne',
            'allAeronef' : Aeronef.objects.all(),
            }
        if request.method == "POST":
            form = budgetLigneChoiceForm(request.POST)
            if form.is_valid():
                activeLigne = form.cleaned_data['ligne'] 
                IdLigne = activeLigne.id
                return redirect('intranet_Budget_Operation_Add_Show', id = IdLigne)
        else:
            form = budgetLigneChoiceForm()   
            context['form'] = form     
            return render(request, templateName, context)
    else:
        return redirect('/internetAccueil')

    #Créer opération
def intranetBudgetOperationAddShow(request,id):
    loggedMember = getLoggedMemberFromRequest(request)
    if loggedMember:
        templateName = 'intranetBudgetGererOperation.html'
        context = {
            'loggedMember' : loggedMember,
            'current_date_time' : dateTimeParis(),
            'current_year' : datetime.now().year,
            'actionBtnName' : 'Créer l\'opération',
            'allAeronef' : Aeronef.objects.all(),
            }
        activeLigne = get_object_or_404(BudgetLigne, pk=id)
        activeProjet = activeLigne.projet
        activeSection = activeProjet.section
        context['activeLigne'] = activeLigne
        context["activeProjet"] = activeProjet
        context["activeSection"] = activeSection
        #extraction des opérations qui correpondent à la ligne sélectionnée
        budgetOpAll = BudgetOperation.objects.filter(ligne = activeLigne)
        context["budgetOpAll"] = budgetOpAll
        if request.method == "POST":
            #On différencie pour insérer nom du pilote pour location et instructiopn
            if activeLigne.name == 'Vols location' or activeLigne.name == 'Vols instruction':
                form = budgetGererOperationLocInstForm(request.POST)   
            else:  
                form = budgetGererOperationForm(request.POST)  
            if form.is_valid():    
                #Recherche par le code de l'opération si elle existe
                #Si oui on modifie l'opération
                #Si non en cré une nouvelle
                code = request.POST.get('code')
                activeOpList = BudgetOperation.objects.filter(code = code)
                #Le code de l'opération existe : modification de l'opération 
                if activeOpList:
                    activeOp = activeOpList[0] 
                    #Soustraction des charges et produits dans les différents niveaux du budget
                    CalcSubBudget(activeOp)
                    #Remplacement des différentes valeurs de champs par les nouvelles suite à la modification
                    activeOp.name = request.POST.get('name')
                    activeOp.date = form.cleaned_data['date']
                    activeOp.aeronef = form.cleaned_data['aeronef']
                    activeOp.charge = request.POST.get('charge')
                    activeOp.produit = request.POST.get('produit')
                    #Cas particuliers des vols location et instruction : nom du bénéficiaire obligatoire
                    if activeLigne.name == 'Vols location' or activeLigne.name == 'Vols instruction':
                        activeOp.beneficiaire = form.cleaned_data['beneficiaire']
                        if activeOp.beneficiaire:
                            activeOp.save()
                            calcProduitComptePilote(activeOp.beneficiaire)
                        else:
                            form = budgetGererOperationLocInstForm()
                            error = 'Définir un membre pour valider l\'opération !'
                            context['error'] = error
                            return render(request, templateName, context)
                    else:
                        activeOp.save()
                #Le code de l'opération n'existe pas : création de l'opération 
                else:   
                    if activeLigne.name == 'Vols location' or activeLigne.name == 'Vols instruction':
                        activeOp = form.save()
                        if activeOp.beneficiaire :
                            activeOp.code = defineCodeOperation(BudgetOperation.objects.filter(ligne = activeLigne),activeLigne)
                            activeOp.ligne = activeLigne
                            activeOp.save()
                            calcProduitComptePilote(activeOp.beneficiaire)
                        else:
                            error = 'Définir un membre pour valider l\'opération !'
                            context['error'] = error
                            activeOp.delete()
                            form = budgetGererOperationLocInstForm()
                            context['form']=form
                            return render(request, templateName, context)
                    else:
                        activeOp = form.save()
                        activeOp.code = defineCodeOperation(BudgetOperation.objects.filter(ligne = activeLigne), activeLigne)
                        activeOp.ligne = activeLigne
                        activeOp.save()
            #Addition des charges et produits dans les différents niveaux du budget
            CalcAddBudget(activeOp)
            return redirect('/intranetBudgetLigneChoice')
        else:
            if activeLigne.name == 'Vols location' or activeLigne.name == 'Vols instruction':
                form = budgetGererOperationLocInstForm()   
            else:   
                form = budgetGererOperationForm()   
            context['form'] = form     
            return render(request, templateName, context)
    else:
        return redirect('/internetAccueil')

def calcProduitComptePilote(activePilote):
    #si ligne "Vols instruction" ou "Vols location", recalculer les produits compte pilote
    ligneLocation = BudgetLigne.objects.get(name = 'Vols location')
    ligneInstruction = BudgetLigne.objects.get(name = 'Vols instruction')
    operationBeneficiaireAll = BudgetOperation.objects.filter(beneficiaire = activePilote)
    produitComptePilote = 0
    for operation in operationBeneficiaireAll:
        if operation.ligne == ligneLocation or operation.ligne == ligneInstruction :
            produitComptePilote += operation.produit
    report = activePilote.reportComptePilote2024
    if report > 0:
        produitComptePilote = produitComptePilote + report
    activePilote.produitComptePilote = produitComptePilote 
    activePilote.save()

    #Supprimer opération
def intranetBudgetOperationDelete(request, id):
    loggedMember = getLoggedMemberFromRequest(request)
    if loggedMember:
        if request.method == 'POST':
            activeOp = BudgetOperation.objects.get(pk=id)
            CalcSubBudget(activeOp) #Recalcul du budget activeLigne, activeProjet, activeSection
            activeLigne = activeOp.ligne
            IdLigne = activeLigne.id
            activeOp.delete()
            return redirect('intranet_Budget_Operation_Add_Show', id = IdLigne)
    else:
        return redirect('/internetAccueil') 

    #Modifier opération
def intranetBudgetOperationModify(request, id):
    loggedMember = getLoggedMemberFromRequest(request)
    if loggedMember:
        templateName = 'intranetBudgetGererOperation.html'
        context = {
            'loggedMember' : loggedMember,
            'current_date_time' : dateTimeParis(),
            'current_year' : datetime.now().year,
            'actionBtnName' : 'Modifier l\'opération',
            'allAeronef' : Aeronef.objects.all(),
            }
        activeOp = BudgetOperation.objects.get(pk=id)
        activeLigne = activeOp.ligne
        activeProjet = activeLigne.projet
        activeSection = activeProjet.section
        context['activeLigne'] = activeLigne
        context["activeProjet"] = activeProjet
        context["activeSection"] = activeSection
        budgetOpAll = BudgetOperation.objects.filter(ligne = activeLigne)
        context["budgetOpAll"] = budgetOpAll
        if request.method == 'POST':
            if activeLigne.name == 'Vols location' or activeLigne.name == 'Vols instruction':
                form = budgetGererOperationLocInstForm(instance = activeOp)   
            else:   
                form = budgetGererOperationForm(instance = activeOp)
            context['form']=form
        return render(request, templateName, context)
    else:
        return redirect('/internetAccueil')
    
#*********************************************************************************************************
#Budget/Budget Année courante
def intranetBudgetCurrentYear(request):
    loggedMember = getLoggedMemberFromRequest(request)
    if loggedMember:
        templateName = 'intranetBudgetCurrentYear.html'
        current_year = datetime.now().year
        activeBudget = BudgetBudget.objects.filter(year = current_year)
        activeBudget = activeBudget[0]
        allOp = BudgetOperation.objects.filter(budget = activeBudget)
        allLigne = BudgetLigne.objects.all()
        allProjet = BudgetProjet.objects.all()
        allSection = BudgetSection.objects.all()
        allCompteEpargne = CompteEpargne.objects.all()
        context = {
            'loggedMember' : loggedMember,
            'current_date_time' : dateTimeParis(),
            'current_year' : current_year,
            'allOp' : allOp,
            'allLigne' : allLigne,
            'allProjet' : allProjet,
            'allSection' : allSection,
            'allCompteEpargne' : allCompteEpargne,
            'activeBudget' : activeBudget,
            }
        return render(request, templateName, context)
    else:
        return redirect('/internetAccueil')
    
def pdfBudget(request): 
    buffer = genererBufferBudget()
    year = str(datetime.now().year)
    month = str(datetime.now().month)
    if len(month) == 1:
        month = "0" + month
    day = str(datetime.now().day)
    if len(day) == 1:
        day = "0" + day
    filename = year + month + day + " - Budget " + year + ".pdf"
    return FileResponse(buffer, as_attachment=True, filename = filename)

#*********************************************************************************************************
#Budget/Budget Année courante par ligne   
def intranetBudgetCurrentYearLigne(request):
    loggedMember = getLoggedMemberFromRequest(request)
    if loggedMember:
        templateName = 'intranetBudgetCurrentYearLigne.html'
        current_year = datetime.now().year
        activeBudget = BudgetBudget.objects.filter(year = current_year)
        activeBudget = activeBudget[0]
        allOp = BudgetOperation.objects.filter(budget = activeBudget)
        allLigne = BudgetLigne.objects.all()
        allProjet = BudgetProjet.objects.all()
        allSection = BudgetSection.objects.all()
        context = {
            'loggedMember' : loggedMember,
            'current_date_time' : dateTimeParis(),
            'allAeronef' : Aeronef.objects.all(),
            'current_year' : current_year,
            'actionBtnName' : 'Visualiser Ligne',
            'allOp' : allOp,
            'allLigne' : allLigne,
            'allProjet' : allProjet,
            'allSection' : allSection,
            'activeBudget' : activeBudget,
            }
        if request.method == 'POST':
            form = budgetLigneListForm(request.POST)   
            myLigne = request.POST.get('ligneSelect')
            context['ligne']= BudgetLigne.objects.get(pk=myLigne)
        else :
            form = budgetLigneListForm()    
        context["form"] = form
        return render(request, templateName, context)
    else:
        return redirect('/internetAccueil')
    
#*********************************************************************************************************
#Budget/Budget Année courante par aeronef   
def intranetBudgetCurrentYearAeronef(request):
    loggedMember = getLoggedMemberFromRequest(request)
    if loggedMember:
        templateName = 'intranetBudgetCurrentYearAeronef.html'
        current_year = datetime.now().year
        activeBudget = BudgetBudget.objects.filter(year = current_year)
        activeBudget = activeBudget[0]
        allOp = BudgetOperation.objects.filter(budget = activeBudget)
        allLigne = BudgetLigne.objects.all()
        allProjet = BudgetProjet.objects.all()
        allSection = BudgetSection.objects.all()
        context = {
            'loggedMember' : loggedMember,
            'current_date_time' : dateTimeParis(),
            'current_year' : current_year,
            'allAeronef' : Aeronef.objects.all(),
            'actionBtnName' : 'Visualiser Aéronef',
            'allOp' : allOp,
            'allLigne' : allLigne,
            'allProjet' : allProjet,
            'allSection' : allSection,
            'activeBudget' : activeBudget,
            }
        if request.method == 'POST':
            form = budgetAeronefListForm(request.POST)   
            myAeronef = request.POST.get('aeronefSelect')
            myOperation = allOp.filter(aeronef = myAeronef)
            myLigneList = []
            for ligne in allLigne:
                myLigne = [0]*4
                for op in myOperation:
                    if op.ligne == ligne:
                        myLigne[0] = ligne.code + ' - ' + ligne.name
                        myLigne[1] = op.charge + myLigne[1]
                        myLigne[2] = op.produit + myLigne[2]
                        myLigne[3] = op.resultat + myLigne[3]        
                myLigneList.append(myLigne)
            
            ligneList = []
            bilan = [0]*3
            for myLigne in myLigneList:
                if myLigne[0]!=0:
                    ligneList.append(myLigne)
                    bilan[0] += myLigne[1]
                    bilan[1] += myLigne[2]
                    bilan[2] += myLigne[3]
                
            context['aeronef']= Aeronef.objects.get(pk=myAeronef)
            context['ligneList'] = ligneList
            context['bilan'] = bilan
        else :
            form = budgetAeronefListForm()    
        context["form"] = form
        return render(request, templateName, context)
    else:
        return redirect('/internetAccueil')
 
 #*********************************************************************************************************
#Budget/Gérer comptes épargnes
    #Créer Ligne
def intranetCompteEpargneAddShow(request):
    loggedMember = getLoggedMemberFromRequest(request)
    if loggedMember:
        templateName ='intranetGererCompteEpargne.html'
        context = {
            'loggedMember' : loggedMember,
            'current_date_time' : dateTimeParis(),
            'actionBtnName' : 'Créer le compte épargne',
            'allAeronef' : Aeronef.objects.all(),
            }
        compteEpargneAll = CompteEpargne.objects.all()
        context['compteEpargneAll'] = compteEpargneAll
        if request.method == 'POST':
            form = gererCompteEpargneForm(request.POST)             
            if form.is_valid():
                if config.idCompteEpargne == 0:
                    form.save()
                else:
                    activeCompteEpargne = CompteEpargne.objects.get(pk=config.idCompteEpargne)
                    activeCompteEpargne.name = request.POST.get('name')
                    activeCompteEpargne.save()
                    config.idCompteEpargne = 0
                return HttpResponseRedirect(request.path) #Evite de créer le même objet quand on rafraichit la page
        else:
            form = gererCompteEpargneForm()
        context["form"] = form
        return render(request, templateName, context)
    else:
        return redirect('/internetAccueil') 

    #Supprimer ligne
def intranetCompteEpargneDelete(request, id):
    loggedMember = getLoggedMemberFromRequest(request)
    if loggedMember:
        if request.method == 'POST':
            activeCompteEpargne = CompteEpargne.objects.get(pk=id)
            activeCompteEpargne.delete()
            return HttpResponseRedirect("/intranetGererCompteEpargne")
    else:
        return redirect('/internetAccueil') 

    #Modifier ligne
def intranetCompteEpargneModify(request, id):
    loggedMember = getLoggedMemberFromRequest(request)
    if loggedMember:
        templateName ='intranetGererCompteEpargne.html'
        context = {
            'loggedMember' : loggedMember,
            'current_date_time' : dateTimeParis(),
            'actionBtnName' : 'Modifier la ligne',
            'allAeronef' : Aeronef.objects.all(),
            }
        compteEpargneAll = CompteEpargne.objects.all()
        context['compteEpargneAll'] = compteEpargneAll
        config.idCompteEpargne = id
        if request.method == 'POST':
            activeCompteEpargne = CompteEpargne.objects.get(pk=config.idCompteEpargne)
            form = gererCompteEpargneForm(instance = activeCompteEpargne)
        context["form"] = form
        return render(request, templateName, context)
    else:
        return redirect('/internetAccueil')    
   
#*********************************************************************************************************
#Budget/Compte Epargne
    #Choisir compte pour créer opération
def intranetCompteEpargneChoice(request):
    loggedMember = getLoggedMemberFromRequest(request)
    if loggedMember:
        templateName = 'intranetCompteEpargneChoice.html'
        context = {
            'loggedMember' : loggedMember,
            'current_date_time' : dateTimeParis(),
            'actionBtnName' : 'Choisir le compte',
            'allAeronef' : Aeronef.objects.all(),
            }
        if request.method == "POST":
            form = compteEpargneChoiceForm(request.POST)
            if form.is_valid():
                activeCompteEpargne = form.cleaned_data['compteEpargne'] 
                IdCompteEpargne = activeCompteEpargne.id
                return redirect('intranet_Compte_Epargne_Operation_Add_Show', id = IdCompteEpargne)
        else:
            form = compteEpargneChoiceForm()   
            context['form'] = form     
            return render(request, templateName, context)
    else:
        return redirect('/internetAccueil')

    #Créer opération
def intranetCompteEpargneOperationAddShow(request,id):
    loggedMember = getLoggedMemberFromRequest(request)
    if loggedMember:
        templateName = 'intranetCompteEpargneGererOperation.html'
        context = {
            'loggedMember' : loggedMember,
            'current_date_time' : dateTimeParis(),
            'actionBtnName' : 'Créer l\'opération',
            'allAeronef' : Aeronef.objects.all(),
            }
        activeCompteEpargne = get_object_or_404(CompteEpargne, pk=id)
        context['activeCompteEpargne'] = activeCompteEpargne
        #extraction des opérations qui correpondent au compte sélectionné
        compteEpargneOpAll = CompteEpargneOperation.objects.filter(compteEpargne = activeCompteEpargne)
        context["compteEpargneOpAll"] = compteEpargneOpAll
        if request.method == "POST":
            form = compteEpargneOperationForm(request.POST)      
            if form.is_valid():
                #Recherche par le code de l'opération si elle existe
                #Si oui on modifie l'opération
                #Si non en cré une nouvelle
                code = request.POST.get('code')
                activeCompteEpargneOpList = CompteEpargneOperation.objects.filter(code = code)
                #Le code de l'opération existe : modification de l'opération 
                if activeCompteEpargneOpList:
                    activeCompteEpargneOp = activeCompteEpargneOpList[0]
                    #Soustraction des charges et produits dans les différents niveaux du budget
                    CalcSubCompteEpargne(activeCompteEpargneOp)
                    #Remplacement des différentes valeurs de champs par les nouvelles suite à la modification
                    activeCompteEpargneOp.name = request.POST.get('name')
                    activeCompteEpargneOp.date = form.cleaned_data['date']
                    activeCompteEpargneOp.charge = request.POST.get('charge')
                    activeCompteEpargneOp.produit = request.POST.get('produit')
                    activeCompteEpargneOp.save()
                #Le code de l'opération n'existe pas : création de l'opération 
                else:   
                    activeCompteEpargneOp = form.save()
                    activeCompteEpargneOp.code = defineCodeCompteEpargneOperation(CompteEpargneOperation.objects.all())
                    activeCompteEpargneOp.compteEpargne = activeCompteEpargne
                    activeCompteEpargneOp.save()
                #Soustraction des charges et produits dans les différents niveaux du budget
                CalcAddCompteEpargne(activeCompteEpargneOp)
            return redirect('/intranetCompteEpargneChoice')
            
        else:
            form = compteEpargneOperationForm()   
            context['form'] = form     
            return render(request, templateName, context)
    else:
        return redirect('/internetAccueil')

    #Supprimer opération
def intranetCompteEpargneOperationDelete(request, id):
    loggedMember = getLoggedMemberFromRequest(request)
    if loggedMember:
        if request.method == 'POST':
            activeOp = CompteEpargneOperation.objects.get(pk=id)
            CalcSubCompteEpargne(activeOp) #Recalcul du budget activeLigne, activeProjet, activeSection
            activeCompteEpargne = activeOp.compteEpargne
            IdCompteEpargne = activeCompteEpargne.id
            activeOp.delete()
            return redirect('intranet_Compte_Epargne_Operation_Add_Show', id = IdCompteEpargne)
    else:
        return redirect('/internetAccueil') 
    
    #Modifier opération
def intranetCompteEpargneOperationModify(request, id):
    loggedMember = getLoggedMemberFromRequest(request)
    if loggedMember:
        templateName = 'intranetCompteEpargneGererOperation.html'
        context = {
            'loggedMember' : loggedMember,
            'current_date_time' : dateTimeParis(),
            'actionBtnName' : 'Modifier l\'opération',
            'allAeronef' : Aeronef.objects.all(),
            }
        activeOp = CompteEpargneOperation.objects.get(pk=id)
        activeCompteEpargne = activeOp.compteEpargne
        context['activeCompteEpargne'] = activeCompteEpargne
        compteEpargneOpAll = CompteEpargneOperation.objects.filter(compteEpargne = activeCompteEpargne)
        context["compteEpargneOpAll"] = compteEpargneOpAll
        if request.method == 'POST':
            form = compteEpargneOperationForm(instance = activeOp)
            context['form']=form
        return render(request, templateName, context)
    else:
        return redirect('/internetAccueil')

#*********************************************************************************************************
#Budget/Bilan comptes Epargne   
def intranetBilanCompteEpargne(request):
    loggedMember = getLoggedMemberFromRequest(request)
    if loggedMember:
        templateName = 'intranetBilanCompteEpargne.html'
        allOp = CompteEpargneOperation.objects.all()
        current_year = datetime.now().year
        bilanBudget = BudgetBudget.objects.filter(year = current_year)
        bilanBudget = bilanBudget[0]
        context = {
            'loggedMember' : loggedMember,
            'current_date_time' : dateTimeParis(),
            'allAeronef' : Aeronef.objects.all(),
            'actionBtnName' : 'Visualiser Compte Épargne',
            'currentYear' : current_year,
            'allOp' : allOp,
            'bilanBudget' : bilanBudget,
            }
        if request.method == 'POST':
            form = compteEpargneListForm(request.POST)   
            myCompteEpargne = request.POST.get('compteEpargneSelect')
            context['compteEpargne']= CompteEpargne.objects.get(pk=myCompteEpargne)
        else :
            form = compteEpargneListForm()    
        context["form"] = form
        return render(request, templateName, context)
    else:
        return redirect('/internetAccueil')
    
#**********************************************************************************************************
#Budget/Générateur de factures
    #Créer facture
def intranetBudgetGenFacture(request):
    loggedMember = getLoggedMemberFromRequest(request)
    if loggedMember:
        templateName = 'intranetBudgetGenFacture.html'
        context = {
            'loggedMember' : loggedMember,
            'current_date_time' : dateTimeParis(),
            'actionBtnName' : 'Créer facture',
            'allAeronef' : Aeronef.objects.all(),
            }
        factureList = Facture.objects.all()
        context['factureList'] = factureList
        if request.method == 'POST':
            form = budgetGenFactureForm(request.POST)
            formClient = budgetGenFactureClientForm(request.POST)
            if form.is_valid() and formClient.is_valid():
                #La facture n'existe pas. Elle va être créée
                if config.idFacture == 0:
                    activeFacture = Facture()
                    activeFacture.code = defineCodeFacture(factureList)
                    activeFacture.date = form.cleaned_data['date']
                    activeFacture.acquite = form.cleaned_data['acquite']
                    activeFacture.clientName = request.POST.get('clientName')
                    activeFacture.clientVorname = request.POST.get('clientVorname')
                    activeFacture.clientAdress = request.POST.get('clientAdress')
                    activeFacture.clientZip = request.POST.get('clientZip')
                    activeFacture.clientCity = request.POST.get('clientCity')
                    activeFacture.clientCountry= request.POST.get('clientCountry')
                    activeFacture.save()
                #La facture existe. Elle va être modifiée
                else:
                    activeFacture = Facture.objects.get(pk=config.idFacture)
                    activeFacture.date = form.cleaned_data['date']
                    activeFacture.acquite = form.cleaned_data['acquite']
                    activeFacture.clientName = request.POST.get('clientName')
                    activeFacture.clientVorname = request.POST.get('clientVorname')
                    activeFacture.clientAdress = request.POST.get('clientAdress')
                    activeFacture.clientZip = request.POST.get('clientZip')
                    activeFacture.clientCity = request.POST.get('clientCity')
                    activeFacture.clientCountry= request.POST.get('clientCountry')
                    activeFacture.save()
            return redirect('intranet_Budget_Gen_Facture_Op', id = activeFacture.id)
        else:
            form = budgetGenFactureForm()
            formClient = budgetGenFactureClientForm()
        context['form']=form 
        context['formClient']=formClient  
        return render(request, templateName, context)
    else:
        return redirect('/internetAccueil')
    
    #Supprimer Facture
def intranetBudgetFactureDelete(request, id):
    loggedMember = getLoggedMemberFromRequest(request)
    if loggedMember:
        if request.method == 'POST':
            activeFacture = Facture.objects.get(pk=id)
            #On supprime la facture
            activeFacture.delete()
            return redirect('/intranetBudgetGenFacture')
    else:
        return redirect('/internetAccueil') 

def intranetBudgetFactureModify(request, id):
    loggedMember = getLoggedMemberFromRequest(request)
    if loggedMember:
        templateName = 'intranetBudgetGenFacture.html'
        context = {
            'loggedMember' : loggedMember,
            'current_date_time' : dateTimeParis(),
            'actionBtnName' : 'Modifier facture',
            'allAeronef' : Aeronef.objects.all(),
            }
        factureList = Facture.objects.all()
        context['factureList'] = factureList
        config.idFacture = id
        if request.method == 'POST':
            activeFacture = Facture.objects.get(pk=id)
            form = budgetGenFactureForm(instance = activeFacture)
            formClient = budgetGenFactureClientForm(instance = activeFacture)
        context['form'] = form
        context['formClient'] = formClient
        return render(request, templateName, context)
    else:
        return redirect('/internetAccueil') 
    
def intranetBudgetGenFactureOp(request,id):
    loggedMember = getLoggedMemberFromRequest(request)
    if loggedMember:
        templateName = 'intranetBudgetGenFactureOp.html'
        context = {
            'loggedMember' : loggedMember,
            'current_date_time' : dateTimeParis(),
            'actionBtnName' : 'Créer l\'opération',
            'allAeronef' : Aeronef.objects.all(),
            }
        activeFacture = get_object_or_404(Facture, pk=id)
        context['activeFacture'] = activeFacture
        factureOpList = OperationFacture.objects.filter(facture = activeFacture)
        context['factureOpList'] = factureOpList
        if request.method == "POST":
            form = budgetGenFactureOpForm(request.POST)
            if form.is_valid():
                print(config.idFactureOp)
                #L'opération n'existe pas. Elle va être créée
                if config.idFactureOp == 0 : 
                    activeFactureOp = form.save()
                    activeFactureOp.code = activeFactureOp.ligne.code
                    activeFactureOp.facture = activeFacture
                    activeFactureOp.save()
                #L'opération existe. Elle va être modifiée
                else :
                    activeFactureOp = OperationFacture.objects.get(pk=config.idFactureOp)
                    activeFactureOp.ligne = form.cleaned_data['ligne']
                    activeFactureOp.code = activeFactureOp.ligne.code
                    activeFactureOp.objet = request.POST.get('objet')
                    activeFactureOp.prixHT = request.POST.get('prixHT')
                    activeFactureOp.nb = request.POST.get('nb')
                    activeFactureOp.facture = activeFacture
                    activeFactureOp.save()   
                    config.idFactureOp = 0                 
            return redirect('intranet_Budget_Gen_Facture_Op', id = id)
        else:
            form = budgetGenFactureOpForm()
        context['form']=form
        return render(request, templateName, context)
    else:
        return redirect('/internetAccueil')
    
def intranetBudgetFactureOpDelete(request,id):
    loggedMember = getLoggedMemberFromRequest(request)
    if loggedMember:
        if request.method == 'POST':
            activeFactureOp = OperationFacture.objects.get(pk=id)
            activeFactureId = activeFactureOp.facture.id
            #On supprime la facture
            activeFactureOp.delete()
            return redirect('intranet_Budget_Gen_Facture_Op', id = activeFactureId)
    else:
        return redirect('\internetAccueil')

def intranetBudgetFactureOpModify(request,id):
    loggedMember = getLoggedMemberFromRequest(request)
    if loggedMember:
        templateName = 'intranetBudgetGenFactureOp.html'
        context = {
            'loggedMember' : loggedMember,
            'current_date_time' : dateTimeParis(),
            'actionBtnName' : 'Modifier l\'opération',
            'allAeronef' : Aeronef.objects.all(),
            }
        config.idFactureOp = id
        if request.method == 'POST':
            activeFactureOp = OperationFacture.objects.get(pk=id)
            activeFacture = activeFactureOp.facture
            context['activeFacture'] = activeFacture
            factureOpList = OperationFacture.objects.filter(facture = activeFacture)
            context['factureOpList'] = factureOpList
            form = budgetGenFactureOpForm(instance = activeFactureOp)
            context['form'] = form
        return render(request, templateName, context)
    else:
        return redirect('\internetAccueil')

def pdfFacture(request, id): 
    buffer = genererBufferFacture(id)
    myFacture = Facture.objects.get(pk = id)
    filename = str(myFacture) + ".pdf"
    return FileResponse(buffer, as_attachment=True, filename = filename)