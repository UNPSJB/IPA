from django.shortcuts import render
from ..forms import *
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from ..models import Afluente
from django.views.generic import ListView,CreateView,DeleteView,DetailView,UpdateView

#Afluente
class AltaAfluente(CreateView):
	model = Afluente
	form_class = AfluenteForm
	template_name = 'forms.html'
	success_url = reverse_lazy('afluentes:listar')

	def get_context_data(self, **kwargs):
		context = super(AltaAfluente, self).get_context_data(**kwargs)
		context['botones'] = {
			'Listado': reverse('afluentes:listar'),
			'Nueva Localidad': reverse('localidades:alta')
			}
		context['nombreForm'] = 'Nuevo afluente'
		return context

class DetalleAfluente(DetailView):
	model = Afluente
	template_name = 'afluente/detalle.html'	
	context_object_name = 'afluente'

	def get_context_data(self, **kwargs):
		context = super(DetalleAfluente, self).get_context_data(**kwargs)
		context['nombreDetalle'] = 'Detalle de Afluente'
		context['botones'] = {
			'Listado': reverse('afluentes:listar'),
			'Nuevo afluente': reverse('afluentes:alta'),
			'Eliminar afluente': reverse('afluentes:eliminar', args=[self.object.id]),
			'Modificar afluente': reverse('afluentes:modificar', args=[self.object.id]),
		}
		return context	

class ListadoAfluentes(ListView):
	model = Afluente
	template_name = 'afluente/listado.html'
	context_object_name = 'afluentes'

	def get_context_data(self, **kwargs):
		context = super(ListadoAfluentes, self).get_context_data(**kwargs)
		context['nombreLista'] = 'Listado de Afluentes'
		context['nombreReverse'] = 'afluentes'
		context['headers'] = ['Nombre', 'Caudal','Descripción']
		context['botones'] = {
			'Nuevo afluente': reverse('afluentes:alta')
			}
		return context


class ModificarAfluente(UpdateView):
	model = Afluente
	form_class = AfluenteForm
	template_name = 'form.html'
	success_url = reverse_lazy('afluentes:listar')

	def post(self, request, *args, **kwargs):
		self.object = self.get_object
		id_afluente = kwargs['pk']
		afluente = self.model.objects.get(id=id_afluente)
		form = self.form_class(request.POST, instance=afluente)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(self.get_success_url())
		else:
			return HttpResponseRedirect(self.get_success_url())

class DeleteAfluente(DeleteView):
	model = Afluente
	template_name = 'afluentes/delete.html'
	success_url = reverse_lazy('afluentes:listar')

