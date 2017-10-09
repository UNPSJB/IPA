from django.conf.urls import url

from .views import ListadoAfluentes, AltaAfluente, Detalle_Afluente, AfluenteDelete

urlpatterns = [

	url(r'^alta_afluentes$', AltaAfluente.as_view(), name='alta_afluentes'),
	url(r'^detalle_afluente/(?P<pk>.+)/$', Detalle_Afluente.as_view(), name='detalle_afluente'),
	url(r'^listar_afluentes$', ListadoAfluentes.as_view(), name='listar_afluentes'),
	url(r'^eliminar/(?P<pk>\d+)$', AfluenteDelete.as_view(), name='delete_afluente'),
	
]