#Imports externes
from django.urls import path,\
                        include
from django.contrib import admin

urlpatterns = [ 
    path('', include('Intranet.urls')), 
    path('', include('Internet.urls')),         
    path('admin', admin.site.urls),
    ]