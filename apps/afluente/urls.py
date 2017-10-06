from django.conf.urls import url

from . import views

urlpatterns = [
	#url(r'^$', views.listar_tiposDocumentacion, name='index_afluente'),
	url(r'^alta_afluente$', alta_afluente, name='alta_afluente'),
	url(r'^listar_afluentes$', listar_afluentes, name='listar_afluentes'),
	
]