from django.conf.urls import url

from apps.establecimientos.views import AltaEstablecimiento, ListadoEstablecimientos

app_name = 'establecimientos'

urlpatterns = [

	url(r'^alta$', AltaEstablecimiento.as_view(), name='alta'),
	url(r'^listar$', ListadoEstablecimientos.as_view(), name='listar'),
]