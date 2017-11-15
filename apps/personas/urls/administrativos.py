from django.conf.urls import url

from ..views.administrativos import *

app_name = 'administrativos'
urlpatterns = [
	url(r'^promover/(?P<pk>.+)/$', AltaAdministrativo.as_view(), name='promover')
]