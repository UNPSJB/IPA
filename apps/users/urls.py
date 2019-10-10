from django.conf.urls import url

from .views import *

app_name = 'usuarios'

urlpatterns = [
	url(r'^listado$', ListadoUsuarios.as_view(), name='listado'),
	url(r'^nuevo$', NuevoUsuario.as_view(), name='alta'),

]