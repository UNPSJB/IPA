from django.conf.urls import url

from . import views

app_name = 'documentos'
urlpatterns = [
	url(r'^$', views.listar_tiposDocumentacion, name='index'),
	url(r'^alta$', views.alta_tiposDocumentos, name='alta'),
	url(r'^listar$', views.listar_tiposDocumentacion, name='listar'),
	
]