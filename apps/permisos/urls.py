from django.conf.urls import url

from . import views

app_name = 'permisos'
urlpatterns = [
	url(r'^solicitudes/listar$', views.listarSolicitudes, name='listarSolicitudes'),
]