from .forms import *
# Create your views here.
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from .models import Localidad

from django.views.generic import ListView,CreateView,DeleteView,DetailView,UpdateView

class AltaLocalidad(CreateView):
	model = Localidad
	form_class = LocalidadForm
	template_name = 'forms.html'
	success_url = reverse_lazy('localidades:listar_localidades')


	def get_context_data(self, **kwargs):
		context = super(AltaLocalidad, self).get_context_data(**kwargs)
		context['botones'] = {'Alta': '/localidades/alta_localidad', 'Listado': '/localidades/listar_localidades'}
		context['nombreForm'] = 'Localidades'
		return context

class Detalle_Localidad(DetailView):
	model = Localidad
	template_name = 'localidades/detalle_localidad.html'

class ListadoLocalidades(ListView):
	model = Localidad
	template_name = 'localidad/listado.html'
	context_object_name = 'localidades'

	def get_context_data(self, **kwargs):
		context = super(ListadoLocalidades, self).get_context_data(**kwargs)
		context['headers'] = ['Codigo Postal', 'Nombre','Departamento']
		context['botones'] = {'Alta': '/localidades/alta_localidad', 'Listado': '/localidades/listar_localidades'}
		return context



class ModificarLocalidad(UpdateView):
	model = Localidad
	form_class = LocalidadForm
	template_name = 'localidad/form.html'
	success_url = reverse_lazy('localidades:listar_localidades')

	def post(self, request, *args, **kwargs):
		self.object = self.get_object
		id_localidad = kwargs['pk']
		localidad = self.model.objects.get(id=id_localidad)
		form = self.form_class(request.POST, instance=localidad)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(self.get_success_url())
		else:
			return HttpResponseRedirect(self.get_success_url())


class LocalidadDelete(DeleteView):
	model = Localidad
	template_name = 'localidad/delete.html'
	success_url = reverse_lazy('localidades:listar_localidades')