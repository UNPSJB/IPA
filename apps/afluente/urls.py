from django.conf.urls import url

from .views import ListadoAfluentes, AltaAfluente, Detalle_Afluente, AfluenteDelete, ModificarAfluente

app_name = 'afluentes'

urlpatterns = [

	url(r'^alta_afluentes$', AltaAfluente.as_view(), name='alta_afluentes'),
	url(r'^detalle_afluente/(?P<pk>.+)/$', Detalle_Afluente.as_view(), name='detalle_afluente'),
	url(r'^modificar_afluente/(?P<pk>.+)/$', ModificarAfluente.as_view(), name='modificar_afluente'),
	url(r'^listar_afluentes$', ListadoAfluentes.as_view(), name='listar_afluentes'),
	url(r'^eliminar/(?P<pk>.+)/$', AfluenteDelete.as_view(), name='delete_afluente'),
	
]