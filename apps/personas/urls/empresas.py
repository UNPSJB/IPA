from django.conf.urls import url
from django.views.generic import TemplateView
from ..views.empresas import AltaEmpresa

app_name = 'empresas'
urlpatterns = [
	url(r'^alta$', AltaEmpresa.as_view(), name='alta')
]