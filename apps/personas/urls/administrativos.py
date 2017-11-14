from django.conf.urls import url

from ..views import AltaAdministrativo

app_name = 'administrativos'
urlpatterns = [
	url(r'^promover/(?P<pk>.+)/$', AltaAdministrativo.as_view(), name='promover')
]