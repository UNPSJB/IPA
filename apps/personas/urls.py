from django.conf.urls import url

from .views import AltaPersona, AltaDirector

app_name = 'personas'


urlpatterns = [

	url(r'^alta_personas$', AltaPersona.as_view(), name='alta_personas'),
	url(r'^alta_director$', AltaDirector.as_view(), name='alta_director'),
	
]