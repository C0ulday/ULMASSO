# Imports externes
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from datetime import datetime

# Imports internes
from ULMASSO.views import dateTimeParis
from Internet.forms import loginForm
from Intranet.models import Member, Aeronef
from Intranet.views import intranetAccueil


# ── Page d'accueil publique ─────────────────────────────────────
def internetAccueil(request):
    return render(request, 'internetAccueil.html', {})


# ── Connexion intranet ──────────────────────────────────────────
def monEspace(request):
    templateName = 'monEspace.html'
    context = {
        'current_date_time': dateTimeParis(),
        'current_year':      datetime.now().year,
        'allAeronef':        Aeronef.objects.all(),
    }
    if request.method == 'POST':
        form = loginForm(request.POST)
        if form.is_valid():
            email    = request.POST.get('identifiant', '')
            password = request.POST.get('password', '')
            if email and password:
                result = Member.objects.filter(email=email, password=password)
                if result.count() != 1:
                    context['error'] = 'Identifiant ou mot de passe erroné'
                    context['form']  = form
                else:
                    loggedMember = result.first()
                    request.session['loggedMemberId'] = loggedMember.id
                    context['loggedMember'] = loggedMember
                    templateName = 'intranetAccueil.html'
                    return intranetAccueil(request)
        else:
            context['form'] = loginForm()
    else:
        context['form'] = loginForm()
    return render(request, templateName, context)


# ── Vols Découverte ─────────────────────────────────────────────
def volsDecouverte(request):
    context = {}
    if request.method == 'POST':
        name    = request.POST.get('name', '').strip()
        phone   = request.POST.get('phone', '').strip()
        email   = request.POST.get('email', '').strip()
        message = request.POST.get('message', '').strip()

        if name and email and message:
            subject = f"[AUV] Nouveau message de {name}"
            body    = (
                f"Nom : {name}\n"
                f"Téléphone : {phone}\n"
                f"E-mail : {email}\n\n"
                f"Message :\n{message}"
            )
            try:
                send_mail(
                    subject,
                    body,
                    settings.DEFAULT_FROM_EMAIL,
                    [settings.CONTACT_EMAIL],
                    fail_silently=False,
                )
                context['form_success'] = True
            except Exception as e:
                context['form_error'] = f"Erreur lors de l'envoi : {e}"
        else:
            context['form_error'] = "Merci de remplir tous les champs obligatoires."

    return render(request, 'volsDecouverte.html', context)


# ── École de Sport ──────────────────────────────────────────────
def ecoleSport(request):
    return render(request, 'ecole.html', {})


# ── Le Club ─────────────────────────────────────────────────────
def leClub(request):
    return render(request, 'leClub.html', {})


# ── Navigation ──────────────────────────────────────────────────
def navigation(request):
    return render(request, 'navigation.html', {})
