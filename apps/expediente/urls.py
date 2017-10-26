from django.conf.urls import url

from . import views

app_name = 'expediente'
urlpatterns = [
	url(r'^alta$', views.AltaExpediente.as_view(), name='alta'),
	url(r'^listar$', views.ListadoExpediente.as_view(), name='listado'),
	url(r'^detalle/(?P<pk>.+)/$', views.DetalleExpediente.as_view(), name='detalle'),
	url(r'^eliminar/(?P<pk>\d+)$', views.DeleteExpediente.as_view(), name='delete'),
	
]