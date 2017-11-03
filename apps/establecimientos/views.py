from .forms import *
from django.core.urlresolvers import reverse_lazy, reverse
from django.views.generic import ListView,CreateView,DeleteView,DetailView,UpdateView
from django.shortcuts import render
from django.http import HttpResponseRedirect

from .models import Establecimiento, Afluente, Departamento, Localidad


# Establecimiento
def alta_establecimiento(request):
	return render(request, 'establecimientos/altaEstablecimiento.html')

class AltaEstablecimiento(CreateView):
	model = Establecimiento
	form_class = EstablecimientoForm
	template_name = 'forms.html'
	success_url = reverse_lazy('establecimientos:listarEstablecimiento')

	def get_context_data(self, **kwargs):
		context = super(AltaEstablecimiento, self).get_context_data(**kwargs)
		context['botones'] = {'Alta': reverse('establecimientos:altaEstablecimiento'), 'Listado': reverse('establecimientos:listarEstablecimiento')}
		context['nombreForm'] = 'Establecimientos'
		return context

class ListadoEstablecimientos(ListView):
	model = Establecimiento
	#form_class = AfluenteForm
	template_name = 'establecimientos/listado.html'
	context_object_name = 'establecimientos'

	def get_context_data(self, **kwargs):
		context = super(ListadoEstablecimientos, self).get_context_data(**kwargs)
		context['headers'] = ['Nombre', 'Localidad','Código Catastral']
		context['botones'] = {'Alta': reverse('establecimientos:altaEstablecimiento'), 'Listado': reverse('establecimientos:listarEstablecimiento')}
		return context


#Afluente
class AltaAfluente(CreateView):
	model = Afluente
	form_class = AfluenteForm
	template_name = 'forms.html'
	success_url = reverse_lazy('establecimientos:listarAfluente')

	def get_context_data(self, **kwargs):
		context = super(AltaAfluente, self).get_context_data(**kwargs)
		context['botones'] = {'Alta': reverse('establecimientos:altaAfluente'), 'Listado': reverse('establecimientos:listarAfluente')}
		context['nombreForm'] = 'Afluente'
		return context

class DetalleAfluente(DetailView):
	model = Afluente
	template_name = 'afluente/detalle_afluente.html'		

class ListadoAfluentes(ListView):
	model = Afluente
	template_name = 'afluente/listado.html'
	context_object_name = 'afluentes'

	def get_context_data(self, **kwargs):
		context = super(ListadoAfluentes, self).get_context_data(**kwargs)
		context['nombreLista'] = 'Listado de Afluentes'
		context['headers'] = ['Nombre', 'Localidad','Caudal']
		context['botones'] = {'Alta': reverse('establecimientos:altaAfluente'), 'Listado':reverse('establecimientos:listarAfluente')}
		return context

class ModificarAfluente(UpdateView):
	model = Afluente
	form_class = AfluenteForm
	template_name = 'afluentes/form.html'
	success_url = reverse_lazy('establecimientos:listarAfluente')

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

class AfluenteDelete(DeleteView):
	model = Afluente
	template_name = 'afluentes/delete.html'
	success_url = reverse_lazy('establecimientos:listarAfluente')


#Departamento
class AltaDepartamento(CreateView):
	model = Departamento
	form_class = DepartamentoForm
	template_name = 'forms.html'
	success_url = reverse_lazy('establecimientos:listarDepartamento')

	def get_context_data(self, **kwargs):
		context = super(AltaDepartamento, self).get_context_data(**kwargs)
		context['botones'] = {'Alta': reverse('establecimientos:altaDepartamento'), 'Listado': reverse('establecimientos:listarDepartamento')}
		context['nombreForm'] = 'Departamentos'
		return context

class DetalleDepartamento(DetailView):
	model = Departamento
	template_name = 'departamentos/detalle.html'		

class ListadoDepartamentos(ListView):
	model = Departamento
	#form_class = DepartamentoForm
	template_name = 'departamento/listado.html'
	context_object_name = 'departamentos'

	def get_context_data(self, **kwargs):
		context = super(ListadoDepartamentos, self).get_context_data(**kwargs)
		context['nombreLista'] = 'Departamentos'
		context['headers'] = ['Nombre','Poblacion']
		context['botones'] = {'Alta': reverse('establecimientos:altaDepartamento'), 'Listado': reverse('establecimientos:listarDepartamento')}
		return context

class ModificarDepartamento(UpdateView):
	model = Departamento
	form_class = DepartamentoForm
	template_name = 'departamentos/form.html'
	success_url = reverse_lazy('establecimientos:listarDepartamento')

	def post(self, request, *args, **kwargs):
		self.object = self.get_object
		id_departamento = kwargs['pk']
		departamento = self.model.objects.get(id=id_departamento)
		form = self.form_class(request.POST, instance=departamento)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(self.get_success_url())
		else:
			return HttpResponseRedirect(self.get_success_url())

class DeleteDepartamento(DeleteView):
	model = Departamento
	template_name = 'departamentos/delete.html'
	success_url = reverse_lazy('establecimientos:listarDepartamento')


#Localidad
class AltaLocalidad(CreateView):
	model = Localidad
	form_class = LocalidadForm
	template_name = 'forms.html'
	success_url = reverse_lazy('establecimientos:listarLocalidad')

	def get_context_data(self, **kwargs):
		context = super(AltaLocalidad, self).get_context_data(**kwargs)
		context['botones'] = {'Alta': reverse('establecimientos:altaLocalidad') , 'Listado': reverse('establecimientos:listarLocalidad')}
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
		context['nombreLista'] = 'Listado de Localidades'
		context['headers'] = ['Codigo Postal', 'Nombre','Departamento']
		context['botones'] = {'Alta': reverse('establecimientos:altaLocalidad') , 'Listado': reverse('establecimientos:listarLocalidad')}
		return context

class ModificarLocalidad(UpdateView):
	model = Localidad
	form_class = LocalidadForm
	template_name = 'localidad/form.html'
	success_url = reverse_lazy('establecimientos:listarLocalidad')

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
	success_url = reverse_lazy('establecimientos:listarLocalidad')