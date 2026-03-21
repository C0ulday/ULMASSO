#Imports externes
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from datetime import datetime, date, timedelta
from math import floor

from Intranet.models import Member, Aeronef, Reservation, Vol, Notification, MaintenanceLog

from ULMASSO.views import dateTimeParis

#************************************************************************************************************

def getLoggedMemberFromRequest(request):
    if 'loggedMemberId' in request.session:
        loggedMemberId = request.session['loggedMemberId']
        loggedMember = Member.objects.get(id=loggedMemberId)
        return loggedMember
    return None

def intranetDeconnect(request):
    logout(request)
    return redirect('internetAccueil')

#************************************************************************************************************

def _jours_restants(date_limite):
    if not date_limite:
        return None
    return (date_limite - date.today()).days

def _statut_maintenance(jours):
    if jours is None:
        return 'neutral', ''
    if jours <= 30:
        return 'danger', 'alert'
    if jours <= 90:
        return 'warning', 'warn'
    return 'success', 'ok'

def _envoyer_notif_admins(sender, message, link=''):
    """Envoie une notification à tous les admins (statut 1-3)."""
    admins = Member.objects.filter(statut__id__in=[1, 2, 3])
    for admin in admins:
        if admin != sender:
            Notification.objects.create(
                recipient=admin,
                sender=sender,
                message=message,
                link=link,
                notif_type='info',
            )

#************************************************************************************************************
# Accueil — Tableau de bord
def intranetAccueil(request):
    loggedMember = getLoggedMemberFromRequest(request)
    if not loggedMember:
        return redirect('/internetAccueil')

    today        = date.today()
    current_year = datetime.now().year

    # Compte pilote
    bilan_compte = loggedMember.bilanComptePilote

    # Mes vols cette année
    mes_vols         = Vol.objects.filter(pilote=loggedMember, date__year=current_year)
    nb_mes_vols      = mes_vols.count()
    duree_min        = sum(v.dureeVol for v in mes_vols)
    duree_mes_vols     = floor(duree_min / 60)
    duree_mes_vols_min = duree_min % 60

    # Prochaine réservation personnelle
    prochaine_resa = Reservation.objects.filter(
        pilote=loggedMember, date__gte=today
    ).order_by('date', 'hInit').first()

    # Réservations 14 prochains jours
    prochaines_resas = Reservation.objects.filter(
        date__gte=today, date__lte=today + timedelta(days=14)
    ).order_by('date', 'hInit')

    # 5 derniers vols
    derniers_vols = Vol.objects.filter(
        pilote=loggedMember, date__year=current_year
    ).order_by('-date')[:5]

    # État maintenance aéronefs
    aeronefs_statut = []
    alertes_maintenance = []
    for aeronef in Aeronef.objects.all():
        j_apt = _jours_restants(aeronef.limiteAptitudeVol)
        j_lsa = _jours_restants(aeronef.limiteLSA)
        j_par = _jours_restants(aeronef.limiteParachute)

        badge_apt, classe_apt = _statut_maintenance(j_apt)
        badge_lsa, classe_lsa = _statut_maintenance(j_lsa)
        badge_par, classe_par = _statut_maintenance(j_par)

        for label, jours, badge in [
            ('Aptitude au vol', j_apt, badge_apt),
            ('Limites LSA',     j_lsa, badge_lsa),
            ('Parachute',       j_par, badge_par),
        ]:
            if badge == 'danger' and jours is not None:
                msg = f'{aeronef.type} — {label} : ' + (
                    f'expiré depuis {abs(jours)}j' if jours < 0 else f'expire dans {jours}j'
                )
                alertes_maintenance.append({'niveau': 'danger', 'message': msg})
            elif badge == 'warning' and jours is not None:
                alertes_maintenance.append({
                    'niveau': 'warning',
                    'message': f'{aeronef.type} — {label} : expire dans {jours}j'
                })

        aeronefs_statut.append({
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
        })

    nb_membres = Member.objects.count()
    nb_pilotes = Member.objects.filter(licenceAUV__value='OUI').count()

    context = {
        'current_date_time':     dateTimeParis(),
        'current_year':          current_year,
        'loggedMember':          loggedMember,
        'allAeronef':            Aeronef.objects.all(),
        'bilan_compte':          bilan_compte,
        'nb_mes_vols':           nb_mes_vols,
        'duree_mes_vols':        duree_mes_vols,
        'duree_mes_vols_min':    duree_mes_vols_min,
        'prochaine_resa':        prochaine_resa,
        'prochaines_resas':      prochaines_resas,
        'derniers_vols':         derniers_vols,
        'aeronefs_statut':       aeronefs_statut,
        'alertes_maintenance':   alertes_maintenance,
        'nb_membres':            nb_membres,
        'nb_pilotes':            nb_pilotes,
    }
    return render(request, 'intranetAccueil.html', context)

#************************************************************************************************************
# Mon Profil — édition
def intranetMonProfil(request):
    loggedMember = getLoggedMemberFromRequest(request)
    if not loggedMember:
        return redirect('/internetAccueil')

    current_year = datetime.now().year
    mes_vols     = Vol.objects.filter(pilote=loggedMember, date__year=current_year)
    nb_vols      = mes_vols.count()
    duree_min    = sum(v.dureeVol for v in mes_vols)
    duree_h      = floor(duree_min / 60)

    context = {
        'loggedMember':    loggedMember,
        'current_date_time': dateTimeParis(),
        'current_year':    current_year,
        'allAeronef':      Aeronef.objects.all(),
        'nb_vols':         nb_vols,
        'duree_h':         duree_h,
        'bilan':           loggedMember.bilanComptePilote,
        'success':         False,
    }

    if request.method == 'POST':
        changed_fields = []

        # Mise à jour des champs
        fields = {
            'name':         ('name',        str),
            'vorname':      ('vorname',     str),
            'phone':        ('phone',       str),
            'email':        ('email',       str),
            'adress':       ('adress',      str),
            'zip':          ('zip',         str),
            'city':         ('city',        str),
            'licenceFFPLUM':('licenceFFPLUM', str),
        }

        for post_key, (model_attr, cast) in fields.items():
            new_val = request.POST.get(post_key, '').strip()
            old_val = str(getattr(loggedMember, model_attr) or '').strip()
            if new_val != old_val:
                setattr(loggedMember, model_attr, new_val or None)
                changed_fields.append(model_attr)

        # Birthday
        birthday_str = request.POST.get('birthday', '').strip()
        if birthday_str:
            try:
                new_bday = datetime.strptime(birthday_str, '%Y-%m-%d').date()
                if new_bday != loggedMember.birthday:
                    loggedMember.birthday = new_bday
                    changed_fields.append('birthday')
            except ValueError:
                pass

        # Mot de passe
        new_pwd  = request.POST.get('new_password', '').strip()
        new_pwd2 = request.POST.get('new_password2', '').strip()
        if new_pwd and new_pwd == new_pwd2:
            loggedMember.password = new_pwd
            changed_fields.append('password')

        loggedMember.save()

        # Notification aux admins si des champs ont changé
        if changed_fields:
            labels = {
                'name': 'Nom', 'vorname': 'Prénom', 'phone': 'Téléphone',
                'email': 'Email', 'adress': 'Adresse', 'zip': 'CP',
                'city': 'Ville', 'birthday': 'Date de naissance',
                'licenceFFPLUM': 'N° licence', 'password': 'Mot de passe',
            }
            fields_str = ', '.join(labels.get(f, f) for f in changed_fields)
            _envoyer_notif_admins(
                sender=loggedMember,
                message=f'{loggedMember} a modifié son profil ({fields_str})',
                link='intranetGererMembers',
            )

        context['success'] = True

    return render(request, 'intranetMonProfil.html', context)

#************************************************************************************************************
# Aéronef interactif (SVG + maintenance log)
def intranetAeronefInteractif(request, aeronef_id):
    loggedMember = getLoggedMemberFromRequest(request)
    if not loggedMember:
        return redirect('/internetAccueil')

    aeronef  = Aeronef.objects.get(pk=aeronef_id)
    all_logs = MaintenanceLog.objects.filter(aeronef=aeronef)

    # Statut maintenance
    j_apt = _jours_restants(aeronef.limiteAptitudeVol)
    j_lsa = _jours_restants(aeronef.limiteLSA)
    j_par = _jours_restants(aeronef.limiteParachute)
    badge_apt, _ = _statut_maintenance(j_apt)
    badge_lsa, _ = _statut_maintenance(j_lsa)
    badge_par, _ = _statut_maintenance(j_par)

    context = {
        'loggedMember':    loggedMember,
        'current_date_time': dateTimeParis(),
        'current_year':    datetime.now().year,
        'allAeronef':      Aeronef.objects.all(),
        'aeronef':         aeronef,
        'all_logs':        all_logs,
        'zones':           MaintenanceLog.ZONES,
        'nb_interventions': all_logs.count(),
        'nb_anomalies':    all_logs.filter(statut='issue').count(),
        'nb_planifies':    all_logs.filter(statut='scheduled').count(),
        'recent_logs':     all_logs.order_by('-date')[:5],
        'badge_aptitude':  badge_apt,
        'badge_lsa':       badge_lsa,
        'badge_parachute': badge_par,
        'today':           date.today(),
    }
    return render(request, 'intranetAeronefInteractif.html', context)

#************************************************************************************************************
# Ajouter entrée maintenance
def intranetMaintenanceAdd(request):
    loggedMember = getLoggedMemberFromRequest(request)
    if not loggedMember:
        return redirect('/internetAccueil')

    if request.method == 'POST':
        aeronef_id  = request.POST.get('aeronef_id')
        zone        = request.POST.get('zone', 'general')
        titre       = request.POST.get('titre', '').strip()
        description = request.POST.get('description', '').strip()
        date_str    = request.POST.get('date', '')
        intervenant = request.POST.get('intervenant', '').strip()
        statut      = request.POST.get('statut', 'done')
        next_due_str = request.POST.get('next_due', '').strip()

        try:
            aeronef  = Aeronef.objects.get(pk=aeronef_id)
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
            next_due = datetime.strptime(next_due_str, '%Y-%m-%d').date() if next_due_str else None

            MaintenanceLog.objects.create(
                aeronef=aeronef,
                zone=zone,
                titre=titre,
                description=description,
                date=date_obj,
                intervenant=intervenant or str(loggedMember),
                membre=loggedMember,
                statut=statut,
                next_due=next_due,
            )

            # Notification admins si anomalie
            if statut == 'issue':
                _envoyer_notif_admins(
                    sender=loggedMember,
                    message=f'Anomalie signalée sur {aeronef} — {dict(MaintenanceLog.ZONES).get(zone, zone)} : {titre}',
                    link=f'intranetAeronefInteractif{aeronef_id}',
                    notif_type='danger',
                ) if False else None  # placeholder — appel direct ci-dessous
                admins = Member.objects.filter(statut__id__in=[1, 2, 3])
                for admin in admins:
                    Notification.objects.create(
                        recipient=admin,
                        sender=loggedMember,
                        message=f'⚠ Anomalie sur {aeronef} ({dict(MaintenanceLog.ZONES).get(zone, zone)}) : {titre}',
                        link=f'intranetAeronefInteractif{aeronef_id}',
                        notif_type='danger',
                    )

        except Exception:
            pass

        return redirect(f'/intranetAeronefInteractif{aeronef_id}')
    return redirect('/intranetAccueil')

#************************************************************************************************************
# Notifications — marquer tout comme lu
def intranetNotificationsRead(request):
    loggedMember = getLoggedMemberFromRequest(request)
    if loggedMember:
        Notification.objects.filter(recipient=loggedMember, is_read=False).update(is_read=True)
    return redirect('/intranetAccueil')
