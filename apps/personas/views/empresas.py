from django.core.urlresolvers import reverse_lazy
from apps.personas import models as pmodels
from apps.personas.forms import *
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from apps.generales.views import GenericAltaView

class AltaEmpresa(GenericAltaView):
	model = pmodels.Empresa
	form_class = EmpresaForm
	template_name = 'empresas/alta.html'
	success_url = reverse_lazy('personas:listado')
	message_error = "Empresa existente"
	cargar_otro_url = reverse_lazy('empresas:alta')