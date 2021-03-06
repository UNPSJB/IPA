from django.shortcuts import render
from ..forms import *
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from ..models import Afluente
from django.views.generic import ListView,CreateView,DeleteView,DetailView,UpdateView
from ..tables import AfluentesTable
from ..filters import AfluentesFilter
from apps.generales.views import GenericListadoView, GenericAltaView
#Afluente

class AltaAfluente(GenericAltaView):
	model = Afluente
	form_class = AfluenteForm
	template_name = 'establecimientos/afluentes/alta.html'
	success_url = reverse_lazy('afluentes:listar')

	def get_context_data(self, **kwargs):
		context = super(AltaAfluente, self).get_context_data(**kwargs)
		context['nombreForm'] = 'Nuevo Afluente'
		return context

class DetalleAfluente(DetailView):
	model = Afluente
	template_name = 'establecimientos/afluentes/detalle.html'	
	context_object_name = 'afluente'

	def get_context_data(self, **kwargs):
		context = super(DetalleAfluente, self).get_context_data(**kwargs)
		context['nombreDetalle'] = 'Detalle de Afluente'
		context['botones'] = {
			'Modificar Afluente': reverse('afluentes:modificar', args=[self.object.id]),
			'Eliminar Afluente': reverse('afluentes:eliminar', args=[self.object.id]),
		}
		context['return_label'] = 'listado de Afluentes'
		context['return_path'] = reverse('afluentes:listar')
		return context	

class ListadoAfluentes(GenericListadoView):
	model = Afluente
	template_name = 'establecimientos/afluentes/listado.html'
	table_class = AfluentesTable
	paginate_by = 12
	filterset_class = AfluentesFilter
	export_name = 'listado_afluentes'	
	
	def get_context_data(self, **kwargs):
		context = super(ListadoAfluentes, self).get_context_data(**kwargs)
		context['nombreLista'] = 'Listado de Afluentes'
		return context	

class ModificarAfluente(UpdateView):
	model = Afluente
	form_class = AfluenteForm
	template_name = 'establecimientos/afluentes/alta.html'
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

	def get_context_data(self, **kwargs):
		context = super(ModificarAfluente, self).get_context_data(**kwargs)
		context['return_path'] = reverse_lazy('afluentes:listar')
		context['nombreForm'] = 'Modificar Afluente'
		return context

class DeleteAfluente(DeleteView):
	model = Afluente
	template_name = 'delete.html'
	success_url = reverse_lazy('afluentes:listar')

