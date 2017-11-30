from django.conf.urls import url

from ..views import *

app_name = 'actas'

urlpatterns = [
	url(r'^alta/(?P<pk>.+)/$', AltaActaDeInspeccion.as_view(), name='alta'),

]