
from django.conf.urls import url

from ..views.personas import *

app_name = 'jefesdepartamento'

urlpatterns = [
	url(r'^promover/(?P<pk>.+)/$', promover_a_jefe_departamento, name='promover'),
]