
from django.conf.urls import url

from ..views.personas import *

app_name = 'solicitantes'

urlpatterns = [
	url(r'^promover/(?P<pk>.+)/$', promover_a_solicitante, name='promover'),
]