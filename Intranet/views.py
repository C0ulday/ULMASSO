#Imports externes
from django.shortcuts import render,\
                                redirect
from django.contrib.auth import logout
from datetime import datetime

from Intranet.models import Member

from ULMASSO.views import dateTimeParis
from Intranet.models import Aeronef
#************************************************************************************************************

#Gestion des sessions
    #Récupération du loggedMember de la session
def getLoggedMemberFromRequest(request):
    if 'loggedMemberId' in request.session:
        loggedMemberId = request.session['loggedMemberId']
        loggedMember = Member.objects.get(id=loggedMemberId)
        return loggedMember
    else:
        return None

    #Se déconnecter
def intranetDeconnect(request):
    logout(request)
    return redirect('internetAccueil')

#************************************************************************************************************

#Accueil
def intranetAccueil(request):
    loggedMember = getLoggedMemberFromRequest(request)
    if loggedMember:
        templateName = "intranetAccueil.html"
        context = {
                'current_date_time' : dateTimeParis(),
                'current_year' : datetime.now().year,
                'loggedMember' : loggedMember,
                'allAeronef' : Aeronef.objects.all(),
            }             
        return render(request,templateName, context)
    else:
        return redirect('/internetAccueil')
