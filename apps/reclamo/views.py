from .forms import *
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from .models import Reclamo
from django.views.generic import ListView,CreateView,DeleteView,DetailView,UpdateView

class AltaReclamo(CreateView):
	model = Reclamo
	form_class = ReclamoForm
	template_name = 'forms.html'
	success_url = reverse_lazy('reclamo:listar')


	def get_context_data(self, **kwargs):
		context = super(AltaReclamo, self).get_context_data(**kwargs)
		context['botones'] = {'Alta': reverse('reclamo:alta'), 'Listado':('reclamo:listar')}
		context['nombreForm'] = 'Reclamo'
		return context

class DetalleReclamo(DetailView):
	model = Reclamo
	template_name = 'reclamo/detalle.html'		


class ListadoReclamo(ListView):
	model = Reclamo
	template_name = 'reclamo/listado.html'
	context_object_name = 'reclamos'


	def get_context_data(self, **kwargs):
		context = super(ListadoReclamo, self).get_context_data(**kwargs)
		context['nombreLista'] = 'Nombre'
		context['headers'] = ['Persona', 'Lugar', 'Fecha']
		context['botones'] = {'Alta': reverse('reclamo:alta'), 'Listado':('reclamo:listar')}
		return context

class ModificarReclamo(UpdateView):
	model = Reclamo
	form_class = ReclamoForm
	template_name = 'reclamo/form.html'
	success_url = reverse_lazy('reclamo:listar')

	def post(self, request, *args, **kwargs):
		self.object = self.get_object
		id_reclamo = kwargs['pk']
		reclamo = self.model.objects.get(id=id_reclamo)
		form = self.form_class(request.POST, instance=reclamo)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(self.get_success_url())
		else:
			return HttpResponseRedirect(self.get_success_url())


class ReclamoDelete(DeleteView):
	model = Reclamo
	template_name = 'reclamo/delete.html'
	success_url = reverse_lazy('reclamo:listar')