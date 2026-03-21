#Imports externes
from django.shortcuts import render,\
                                HttpResponseRedirect,\
                                redirect
from datetime import datetime
from math import floor

#Imports internes
from Intranet.MenuMembres.forms import loggedMemberPasswordModifyForm,\
                                        memberForm,\
                                        memberListForm
from Intranet.models import Member, Statut

from ULMASSO.views import dateTimeParis
from Intranet.views import getLoggedMemberFromRequest

from Intranet.MenuMembres import config
from Intranet.models import Aeronef

#************************************************************************************************************
#Bouton modifier mot de passe
def memberPassword(request):
    loggedMember = getLoggedMemberFromRequest(request)
    if loggedMember:
        context = {'loggedMember' : loggedMember,
                   'current_date_time' : dateTimeParis(),
                   'actionBtnName' : 'Modifier mot de passe',
                   'allAeronef' : Aeronef.objects.all(),
            }
        if request.method == 'POST':
            form = loggedMemberPasswordModifyForm(request.POST)
            if form.is_valid():
                loggedMember.password = form.cleaned_data['password']
                loggedMember.save()
                templateName = "IntranetAccueil.html"
                return render(request, templateName, context)
        else:
            form = loggedMemberPasswordModifyForm(instance = loggedMember)
            templateName = "memberProfile.html"
            context['form'] = form
            return render(request, templateName, context)
    else:
        return redirect('/internetAccueil')
    
#************************************************************************************************************
#Membres/Gérer Membres
    #Créer Membre    
def intranetMemberAddShow(request):
    #global idMember
    loggedMember = getLoggedMemberFromRequest(request)
    if loggedMember:
        templateName = "intranetGererMembers.html"
        context = {'loggedMember' : loggedMember,
                   'current_date_time' : dateTimeParis(),
                   'current_year' : datetime.now().year,
                   'actionBtnName' : 'Créer un membre',
                   'allAeronef' : Aeronef.objects.all(),
            }
        memberAll = Member.objects.all()
        context['memberAll'] = memberAll
        if request.method == 'POST':
            form = memberForm(request.POST)
            if form.is_valid():
                if config.idMember == 0:
                    form.save()
                else:
                    activeMember = Member.objects.get(pk=config.idMember)
                    activeMember.name = request.POST.get('name')
                    activeMember.vorname = request.POST.get('vorname')
                    activeMember.genre=form.cleaned_data['genre']
                    activeMember.birthday=form.cleaned_data['birthday']
                    activeMember.email = request.POST.get('email')
                    activeMember.phone=request.POST.get('phone')
                    activeMember.zip=request.POST.get('zip')
                    activeMember.city=request.POST.get('city')
                    activeMember.adress=request.POST.get('adress')
                    activeMember.licenceFFPLUM=request.POST.get('licenceFFPLUM')
                    activeMember.licenceAUV=form.cleaned_data['licenceAUV']
                    activeMember.instructeur=form.cleaned_data['brevetInstructeur']
                    activeMember.datePiloteC2 = form.cleaned_data['datePiloteC2']
                    activeMember.datePiloteC3 = form.cleaned_data['datePiloteC3']
                    activeMember.datePiloteC4 = form.cleaned_data['datePiloteC4']
                    activeMember.dateEmportC2 = form.cleaned_data['dateEmportC2']
                    activeMember.dateEmportC3 = form.cleaned_data['dateEmportC3']
                    activeMember.dateEmportC4 = form.cleaned_data['dateEmportC4']
                    activeMember.dateBaptemeC2 = form.cleaned_data['dateBaptemeC2']
                    activeMember.dateBaptemeC3 = form.cleaned_data['dateBaptemeC3']
                    activeMember.dateBaptemeC4 = form.cleaned_data['dateBaptemeC4']
                    activeMember.reportComptePilote2024 = request.POST.get('reportComptePilote2024')
                    activeMember.save()
                    config.idMember = 0
                return HttpResponseRedirect(request.path) #Evite de créer le même objet quand on rafraichit la page
        else:
            form = memberForm()
        context["form"] = form
        return render(request, templateName, context)
    else:
        return redirect('/internetAccueil')
    
    #Supprimer Membre
def intranetMemberDelete(request,id):
    loggedMember = getLoggedMemberFromRequest(request)
    if loggedMember:
        if request.method == 'POST':
            activeMember = Member.objects.get(pk=id)
            activeMember.delete()
            return HttpResponseRedirect("/intranetGererMembers")
    else:
        return redirect('/internetAccueil')
    
    #Modifier Membre
def intranetMemberModify(request, id):
    #global idMember
    loggedMember = getLoggedMemberFromRequest(request)
    if loggedMember:
        templateName = "intranetGererMembers.html"
        context = {'loggedMember' : loggedMember,
                    'current_date_time' : dateTimeParis(),
                    'current_year' : datetime.now().year,
                    'actionBtnName' : 'Modifier un membre',
                    'allAeronef' : Aeronef.objects.all(),
            }
        memberAll = Member.objects.all()
        context['memberAll'] = memberAll
        config.idMember = id 
        if request.method == "POST": 
            activeMember = Member.objects.get(pk=config.idMember)
            form = memberForm(instance = activeMember)
        context["form"] = form
        return render(request, templateName, context)
    else:
        return redirect('/internetAccueil')

#************************************************************************************************************
#Membres/Statistiques
def intranetStatsMembres(request):
    loggedMember = getLoggedMemberFromRequest(request)
    if not loggedMember:
        return redirect('/internetAccueil')

    membres = Member.objects.select_related('statut', 'licenceAUV', 'brevetInstructeur').all()
    nb_total = membres.count()

    # Comptages simples
    nb_licencies    = membres.filter(licenceAUV__value='OUI').count()
    nb_instructeurs = membres.filter(brevetInstructeur__value='OUI').count()

    # Brevets par classe
    nb_pilote_c2 = membres.exclude(datePiloteC2=None).count()
    nb_pilote_c3 = membres.exclude(datePiloteC3=None).count()
    nb_pilote_c4 = membres.exclude(datePiloteC4=None).count()
    nb_emport_c2 = membres.exclude(dateEmportC2=None).count()
    nb_emport_c3 = membres.exclude(dateEmportC3=None).count()
    nb_emport_c4 = membres.exclude(dateEmportC4=None).count()
    nb_bapteme_c2 = membres.exclude(dateBaptemeC2=None).count()
    nb_bapteme_c3 = membres.exclude(dateBaptemeC3=None).count()
    nb_bapteme_c4 = membres.exclude(dateBaptemeC4=None).count()

    # Répartition par statut
    par_statut = []
    for statut in Statut.objects.all():
        nb = membres.filter(statut=statut).count()
        pct = floor(nb * 100 / nb_total) if nb_total > 0 else 0
        par_statut.append({'statut': statut, 'nb': nb, 'pct': pct})

    context = {
        'loggedMember':     loggedMember,
        'current_date_time': dateTimeParis(),
        'current_year':     datetime.now().year,
        'allAeronef':       Aeronef.objects.all(),
        'membres':          membres,
        'nb_total':         nb_total,
        'nb_licencies':     nb_licencies,
        'nb_instructeurs':  nb_instructeurs,
        'nb_pilotes_c3':    nb_pilote_c3,
        'nb_pilote_c2':     nb_pilote_c2,
        'nb_pilote_c3':     nb_pilote_c3,
        'nb_pilote_c4':     nb_pilote_c4,
        'nb_emport_c2':     nb_emport_c2,
        'nb_emport_c3':     nb_emport_c3,
        'nb_emport_c4':     nb_emport_c4,
        'nb_bapteme_c2':    nb_bapteme_c2,
        'nb_bapteme_c3':    nb_bapteme_c3,
        'nb_bapteme_c4':    nb_bapteme_c4,
        'par_statut':       par_statut,
    }
    return render(request, 'intranetStatsMembres.html', context)


#************************************************************************************************************
#Membres/Afficher Membre
def intranetMemberShow(request):
    loggedMember = getLoggedMemberFromRequest(request)
    if loggedMember:
        templateName = 'intranetVoirMembers.html'
        context = {'loggedMember' : loggedMember,
                   'current_date_time' : dateTimeParis(),
                   'current_year' : datetime.now().year,
                   'actionBtnName' : 'Visualiser',
                   'allAeronef' : Aeronef.objects.all(),
                   }
        if request.method == 'POST':
            form = memberListForm(request.POST)   
            idMember = request.POST.get('memberSelect')
            context['member']= Member.objects.get(pk=idMember)
        else :
            form = memberListForm()    
        context["form"] = form
        return render(request, templateName, context)
    else:
        return redirect('/internetAccueil')