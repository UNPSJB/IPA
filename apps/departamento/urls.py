from django.conf.urls import url

from apps.departamento.views import alta_departamento

urlpatterns = [
	#url(r'^$', views.listar_tiposDocumentacion, name='index_afluente'),
	url(r'^alta_departamento$', alta_departamento, name='alta_departamento'),
	#url(r'^listar_afluentes$', listar_afluentes, name='listar_afluentes'),
	
]