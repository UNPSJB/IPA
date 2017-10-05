from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.alta_afluente, name='index_afluente'),
	url(r'^alta$', views.alta_afluente, name='alta_afluente'),
	url(r'^listar$', views.alta_afluente, name='listar_afluente'),
	
]