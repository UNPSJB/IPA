from django.conf.urls import url

from apps.establecimientos.views import AltaEstablecimiento, ListadoEstablecimientos

app_name = 'establecimientos'

urlpatterns = [

	url(r'^alta_establecimiento$', AltaEstablecimiento.as_view(), name='alta_establecimiento'),
	url(r'^listar_establecimientos$', ListadoEstablecimientos.as_view(), name='listar_establecimientos'),
]