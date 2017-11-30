
from django.conf.urls import url

from ..views.personas import *

app_name = 'liquidadores'

urlpatterns = [
	url(r'^promover/(?P<pk>.+)/$', promover_a_liquidador, name='promover'),
]