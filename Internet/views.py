#Imports externes
from django.shortcuts import render
from ULMASSO.views import dateTimeParis
from django.core.mail import EmailMessage
from datetime import datetime

#imports internes
from Internet.forms import loginForm
from Intranet.models import Member,\
                            Aeronef
from Intranet.views import intranetAccueil


#Internet
def internetAccueil(request):
    templateName = "internetAccueil.html"
    context = {}
    return render(request,templateName, context)

#Connexion intranet
def monEspace(request):
    templateName = "monEspace.html"
    context = {
        'current_date_time' : dateTimeParis(),
        'current_year' : datetime.now().year,
        'allAeronef' : Aeronef.objects.all(),
    }
    if len(request.POST) > 0 :
        form = loginForm(request.POST)
        if form.is_valid():
            email = request.POST['identifiant']
            password = request.POST['password'] 
            if email and password:
                result = Member.objects.filter(email=email,
                                               password = password)
                if len(result) != 1:
                    error = 'Identifiant ou mot de passe erroné'
                    context['error'] = error
                    context['form'] = form
                else:
                    loggedMember = Member.objects.get(email=email)
                    request.session['loggedMemberId'] = loggedMember.id
                    intranetAccueil(request)
                    context['loggedMember'] = loggedMember
                    templateName = 'intranetAccueil.html'
        else:
            form = loginForm()
            context['form'] = form
    else:
        form = loginForm()
        context['form'] = form
    return render(request,templateName, context)

def volsDecouverte(request):
    return render(request,'volsdecouverte.html',context={})