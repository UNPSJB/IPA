
from django.conf.urls import url

from ..views.personas import *

app_name = 'sumariantes'

urlpatterns = [
	url(r'^promover/(?P<pk>.+)/$', promover_a_sumariante, name='promover'),
]