#Imports externes
from django.shortcuts import render,\
                            HttpResponseRedirect,\
                            redirect

#Imports internes
from Internet.views import dateTimeParis
from Intranet.views import getLoggedMemberFromRequest
from Intranet.MenuReservation.forms import reservationForm,\
                                            reservationListForm
from Intranet.models import Reservation, Aeronef
from Intranet.MenuReservation import config

def intranetReservationCalendrier(request, myAeronef):
    loggedMember = getLoggedMemberFromRequest(request)
    if loggedMember:
        templateName = 'intranetReservationCalendrier.html'
        myAeronef = Aeronef.objects.filter(type = myAeronef)
        myAeronef = myAeronef[0]
        context = {'loggedMember' : loggedMember,
                   'current_date_time' : dateTimeParis(),
                   'myAeronef' : myAeronef,
                   'allAeronef' : Aeronef.objects.all(),
                   }
        allReservation = Reservation.objects.filter(aeronef = myAeronef)
        context['allReservation'] = allReservation
        idReservation = config.idReservation
        if request.method == 'POST':
            form = reservationForm(request.POST)
            if form.is_valid():
                if idReservation == 0:
                    activeReservation = Reservation()
                    activeReservation.pilote = loggedMember
                    activeReservation.aeronef = myAeronef
                    activeReservation.typeVol = request.POST.get('typeVol')
                    activeReservation.date = request.POST.get('date')
                    activeReservation.hInit = request.POST.get('hInit')
                    activeReservation.hEnd = request.POST.get('hEnd')
                    activeReservation.save()
                else:
                    activeReservation = Reservation.objects.get(pk = idReservation)
                    activeReservation.typeVol = request.POST.get('typeVol')
                    activeReservation.date = request.POST.get('date')
                    activeReservation.hInit = request.POST.get('hInit')
                    activeReservation.hEnd = request.POST.get('hEnd')
                    activeReservation.save() 
                    config.idReservation = 0
                    idReservation = config.idReservation             
            return HttpResponseRedirect(request.path)        
        else:
            form = reservationForm()
        context['idReservation'] = idReservation
        context['form']=form
        return render(request, templateName, context)     
    else:
        return redirect('/internetAccueil')
    
def intranetReservationCreate(request, myAeronef):
    loggedMember = getLoggedMemberFromRequest(request)
    if loggedMember:
        templateName = 'intranetReservationCreate.html'
        myAeronef = Aeronef.objects.filter(type = myAeronef)
        myAeronef = myAeronef[0]
        context = {'loggedMember' : loggedMember,
                   'current_date_time' : dateTimeParis(),
                   'myAeronef' : myAeronef,
                   'allAeronef' : Aeronef.objects.all(),
                   }
        idReservation = config.idReservation
        context['idReservation'] = idReservation
        if idReservation == 0:
            context['actionBtnName'] = 'Créer'
        else:
            context['actionBtnName'] = 'Modifier'
        allReservation = Reservation.objects.filter(aeronef = myAeronef)
        context['allReservation'] = allReservation
        if request.method == 'POST':
            form = reservationForm(request.POST)
            return HttpResponseRedirect(request.path)        
        else:
            if idReservation == 0:
                form = reservationForm() 
            else:
                myReservation = Reservation.objects.get(pk = idReservation)
                form = reservationForm(initial = {'date' : myReservation.date,
                                                   'hInit' : myReservation.hInit,
                                                   'hEnd' : myReservation.hEnd,
                                                   'textVol' : myReservation.textVol,
                                                   'typeVol' : myReservation.typeVol})
        context['form'] = form
        return render(request, templateName, context)     
    else:
        return redirect('/internetAccueil')
    
def intranetReservationModify(request, myAeronef):
    loggedMember = getLoggedMemberFromRequest(request)
    if loggedMember:
        templateName = 'intranetReservationModify.html'
        myAeronef = Aeronef.objects.filter(type = myAeronef)
        myAeronef = myAeronef[0]
        context = {'loggedMember' : loggedMember,
                   'current_date_time' : dateTimeParis(),
                   'actionBtnName' : 'Sélectionner',
                   'myAeronef' : myAeronef,
                   'allAeronef' : Aeronef.objects.all(),
                   }
        allReservation = Reservation.objects.filter(aeronef = myAeronef)
        context['allReservation'] = allReservation
        allMyReservation = Reservation.objects.filter(aeronef = myAeronef, pilote = loggedMember)
        context['allMyReservation'] = allMyReservation
        if request.method == 'POST':
            form = reservationListForm(request.POST)
            form.fields['reservation'].queryset = allMyReservation
            if form.is_valid():
                activeReservation = form.cleaned_data['reservation']
                config.idReservation = activeReservation.id
                return redirect('intranet_Reservation_Create', myAeronef = myAeronef) 
            return HttpResponseRedirect(request.path)       
        else:
            form = reservationListForm() 
            form.fields['reservation'].queryset = allMyReservation 
        context['form'] = form
        return render(request, templateName, context)     
    else:
        return redirect('/internetAccueil')
    
def intranetReservationDelete(request, myAeronef):
    loggedMember = getLoggedMemberFromRequest(request)
    if loggedMember:
        templateName = 'intranetReservationDelete.html'
        myAeronef = Aeronef.objects.filter(type = myAeronef)
        myAeronef = myAeronef[0]
        context = {'loggedMember' : loggedMember,
                   'current_date_time' : dateTimeParis(),
                   'actionBtnName' : 'Supprimer',
                   'myAeronef' : myAeronef,
                   'allAeronef' : Aeronef.objects.all(),
                   }
        allReservation = Reservation.objects.filter(aeronef = myAeronef)
        context['allReservation'] = allReservation
        allMyReservation = Reservation.objects.filter(aeronef = myAeronef, pilote = loggedMember)
        context['allMyReservation'] = allMyReservation
        if request.method == 'POST':
            form = reservationListForm(request.POST)
            form.fields['reservation'].queryset = allMyReservation
            if form.is_valid():
                activeReservation = form.cleaned_data['reservation']
                activeReservation.delete()
            return HttpResponseRedirect(request.path)       
        else:
            form = reservationListForm() 
            form.fields['reservation'].queryset = allMyReservation
        context['form'] = form
        return render(request, templateName, context)     
    else:
        return redirect('/internetAccueil')

