from django.conf.urls import url

from ..views import *

app_name = 'actas'

urlpatterns = [
	url(r'^inspeccion/alta//(?P<pk>.+)/$', AltaActaDeInspeccion.as_view(), name='altaInspeccion'),
	url(r'^infraccion/alta/(?P<pk>.+)/$', AltaActaDeInfraccion.as_view(), name='altaInfraccion'),

]