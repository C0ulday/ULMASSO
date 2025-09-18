from django.urls import path

from Internet.views import internetAccueil,\
                            monEspace,\
                            volsDecouverte,\
                            navigation,\
                                ecoleSport

urlpatterns = [
    path('', internetAccueil, name='internetAccueil'),
    path('internetAccueil', internetAccueil, name='internet_Accueil'),
    path('volsDecouverte', volsDecouverte, name='volsDecouverte'),
    #Internet/Intranet
    path('monEspace', monEspace, name ='mon_Espace'),
    path('navigation', navigation, name ='navigation'),
    path('ecoleSport', ecoleSport, name ='ecoleSport'),
    ]