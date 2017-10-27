from .forms import *
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from .models import InfraccionActa
from django.views.generic import ListView,CreateView,DeleteView,DetailView,UpdateView

class AltaInfraccionActa(CreateView):
	model = InfraccionActa
	form_class = InfraccionActaForm
	template_name = 'forms.html'
	success_url = reverse_lazy('infraccionActas:listar')


	def get_context_data(self, **kwargs):
		context = super(AltaInfraccionActa, self).get_context_data(**kwargs)
		context['botones'] = {'Alta': reverse ('infraccionActas:alta'), 'Listado':reverse ('infraccionActas:listar')}
		context['nombreForm'] = 'Acta de Infraccion'
		return context

class DetalleInfraccionActa(DetailView):
	model = InfraccionActa
	template_name = 'infraccionActas/detalle.html'		


class ListadoInfraccionActas(ListView):
	model = InfraccionActa
	#form_class = InfraccionActaForm
	template_name = 'infraccionActa/listado.html'
	context_object_name = 'infraccionActas'

	def get_context_data(self, **kwargs):
		context = super(ListadoInfraccionActas, self).get_context_data(**kwargs)
		context['nombreLista'] = 'InfraccionActa'
		context['headers'] = ['Numero','Fecha']
		context['botones'] = {'Alta': reverse ('infraccionActas:alta'), 'Listado':reverse ('infraccionActas:listar')}
		return context

class ModificarInfraccionActa(UpdateView):
	model = InfraccionActa
	form_class = InfraccionActaForm
	template_name = 'infraccionActas/form.html'
	success_url = reverse_lazy('infraccionActas:listar')

	def post(self, request, *args, **kwargs):
		self.object = self.get_object
		id_infraccionActa = kwargs['pk']
		infraccionActa = self.model.objects.get(id=id_infraccionActa)
		form = self.form_class(request.POST, instance=infraccionActa)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(self.get_success_url())
		else:
			return HttpResponseRedirect(self.get_success_url())


class DeleteInfraccionActa(DeleteView):
	model = InfraccionActa
	template_name = 'infraccionActas/delete.html'
	success_url = reverse_lazy('infraccionActas:listar')




