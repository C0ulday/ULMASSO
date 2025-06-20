#Imports externes
from django.shortcuts import render,\
                            redirect
import requests

#Imports internes
from Internet.views import dateTimeParis
from Intranet.views import getLoggedMemberFromRequest
from Intranet.MenuWeather.forms import cityForm
from Intranet.models import Aeronef,\
                            City

def intranetWeather(request):
    loggedMember = getLoggedMemberFromRequest(request)
    if loggedMember:
        templateName = "intranetWeather.html"
        context = {'loggedMember' : loggedMember,
                   'current_date_time' : dateTimeParis(),
                   'allAeronef' : Aeronef.objects.all(),
                   'actionBtnName' : 'Ajouter',
                   }
        lat = 44.9211909021499
        lon = 4.970743367294972
        API_key = '854cc680bee2016c6bbf147ce46b62a8'
        url = f'https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&appid={API_key}&units=metric&lang=fr'
        # if request.method == 'POST':
        #     form = cityForm(request.POST)
        #     form.save()   
        form = cityForm()
        res = requests.get(url)
        weather_data = res.json()
        print(weather_data)
        weather = {
            'temperature' : weather_data['current']['temp'],
            'description': weather_data['current']['weather'][0]['description'],
            'QNH' : weather_data['current']['pressure'],
            'v_vent' : weather_data['current']['wind_speed'],
            'd_vent' : weather_data['current']['wind_deg'],
            #'rafale' : weather_data['current']['wind_gust'],
            'icon': weather_data['current']['weather'][0]['icon']
            }
        context['weather'] = weather

        # cities = City.objects.all()
        # weather_data = []
        # for city in cities:
        #     city_weather = requests.get(url).json()
        #     weather = {
        #         'city': city,
        #         'temperature': city_weather['main']['temp'],
        #         'description': city_weather['weather'][0]['description'],
        #         'icon': city_weather['weather'][0]['icon']
        #     } 
        #     weather_data.append(weather)
        # context['weather_data'] = weather_data
        context['form'] = form
        return render(request, templateName,context) #returns index.html template
    else:
        return redirect('/internetAccueil')