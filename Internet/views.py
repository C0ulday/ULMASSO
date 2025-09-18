#Imports externes
from django.shortcuts import render
from ULMASSO.views import dateTimeParis
from django.core.mail import EmailMessage
from datetime import datetime

from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages


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

def ecoleSport(request):
    return render(request,'ecole.html',context={})


def fomulaireDecouverte(request):
    
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # Contenu du mail
        subject = f"Nouveau message de {name} via le formulaire de contact"
        message_body = f"""
        Nom : {name}
        Téléphone : {phone}
        E-mail : {email}

        Message :
        {message}
        """

        try:
            send_mail(
                subject,
                message_body,
                settings.DEFAULT_FROM_EMAIL,  # l’expéditeur configuré
                [settings.CONTACT_EMAIL],   # le destinataire configuré
                fail_silently=False,
            )
            messages.success(request, "Votre message a été envoyé avec succès !")
        except Exception as e:
            messages.error(request, f"Erreur lors de l'envoi du message : {e}")

        return redirect('vols_decouverte')  # redirige vers la même page

    return render(request, 'volsDecouverte.html')


def navigation(request):
    return render(request,'navigation.html',context={})
