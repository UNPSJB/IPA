from django.conf.urls import url

from . import views

app_name = 'documentos'
urlpatterns = [
	url(r'^$', views.listar_tiposDocumentacion, name='listar')
]