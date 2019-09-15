from django.conf.urls import url
from django.views.generic import TemplateView
from ..views.empresas import *

app_name = 'empresas'
urlpatterns = [
	url(r'^alta$', TemplateView.as_view(template_name='test.html'), name='alta')
]