
from django.conf.urls import url

from ..views.personas import *

app_name = 'inspectores'

urlpatterns = [
	url(r'^promover/(?P<pk>.+)/$', promover_a_inspector, name='promover'),
]