from django.shortcuts import render
from .forms import *
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from .models import Comision
from django.views.generic import ListView,CreateView,DeleteView,DetailView,UpdateView

class AltaComision(CreateView):
	model = Comision
	form_class = ComisionForm
	template_name = 'forms.html'
	success_url = reverse_lazy('comisiones:listar')

	def get_context_data(self, **kwargs):
		context = super(AltaComision, self).get_context_data(**kwargs)
		context['botones'] = {
			'Listado comisiones': reverse('comisiones:listar'),
			'Nuevo Empleado': reverse('personas:alta'),
			'Nueva Localidad': reverse('localidades:alta'),
			'Nuevo Departamento': reverse('departamentos:alta')
			}
		context['nombreForm'] = 'Nueva comisión'
		return context

class DetalleComision(DetailView):
	model = Comision
	template_name = 'comision/detalle.html'

class ListadoComision(ListView):
	model = Comision
	template_name = 'comision/listado.html'
	context_object_name = 'comisiones'

	def get_context_data(self, **kwargs):
		context = super(ListadoComision, self).get_context_data(**kwargs)
		context['nombreLista'] = 'Listado de comisiones'
		context['headers'] = ['Empleado', 'Departamento']
		context['botones'] = {'Nueva comisión': reverse('comisiones:alta')}
		return context

class ModificarComision(UpdateView):
	model = Comision
	form_class = ComisionForm
	template_name = 'comision/form.html'
	success_url = reverse_lazy('comisiones:listar')

	def post(self, request, *args, **kwargs):
		self.object = self.get_object
		id_comision = kwargs['pk']
		comision = self.mod-el.objects.get(id=id_comision)
		form = self.form_class(request.POST, instance=comision)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(self.get_success_url())
		else:
			return HttpResponseRedirect(self.get_success_url())

class DeleteComision(DeleteView):
	model = Comision
	template_name = 'delete.html'
	success_url = reverse_lazy('comisiones:listar')