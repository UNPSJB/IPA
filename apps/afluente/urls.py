from django.conf.urls import url

from apps.afluente.views import alta_afluente

urlpatterns = [
	#url(r'^$', views.listar_tiposDocumentacion, name='index_afluente'),
	url(r'^alta_afluente$', alta_afluente, name='alta_afluente'),
	#url(r'^listar$', views.listar_tiposDocumentacion, name='listar_afluente'),
	
]