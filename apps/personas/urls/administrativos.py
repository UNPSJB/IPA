from django.conf.urls import url

from ..views.personas import *

app_name = 'administrativos'
urlpatterns = [
	url(r'^promover/(?P<pk>.+)/$', promover_a_administrativo, name='promover')
]