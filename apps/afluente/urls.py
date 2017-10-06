from django.conf.urls import url

from apps.afluente.views import alta_afluentes,listar_afluentes

urlpatterns = [
	#url(r'^$', views.listar_tiposDocumentacion, name='index_afluente'),
	url(r'^alta_afluentes$', alta_afluentes, name='alta_afluentes'),
	url(r'^listar_afluentes$', listar_afluentes, name='listar_afluentes'),
	
]