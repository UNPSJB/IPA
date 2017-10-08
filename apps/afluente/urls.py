from django.conf.urls import url

from .views import ListadoAfluentes, AltaAfluente

urlpatterns = [

	url(r'^alta_afluentes$', AltaAfluente.as_view(), name='alta_afluentes'),
	url(r'^listar_afluentes$', ListadoAfluentes.as_view(), name='listar_afluentes'),
	
]