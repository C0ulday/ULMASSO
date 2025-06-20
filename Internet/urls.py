from django.urls import path

from Internet.views import internetAccueil,\
                            monEspace,\
                            volsDecouverte

urlpatterns = [
    path('', internetAccueil, name='internetAccueil'),
    path('internetAccueil', internetAccueil, name='internet_Accueil'),
    path('volsDecouverte', volsDecouverte, name='volsDecouverte'),
    #Internet/Intranet
    path('monEspace', monEspace, name ='mon_Espace'),
    ]