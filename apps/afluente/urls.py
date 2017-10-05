from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.listar_tiposDocumentacion, name='index_afluente'),
	url(r'^alta$', views.alta_tiposDocumentos, name='alta_afluente'),
	url(r'^listar$', views.listar_tiposDocumentacion, name='listar_afluente'),
	
]