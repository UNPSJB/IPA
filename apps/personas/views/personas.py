from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy, reverse
from apps.personas import models as pmodels
from django.shortcuts import redirect
from apps.personas.forms import *
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from apps.generales.views import GenericAltaView

class AltaPersona(GenericAltaView):
	model = pmodels.Persona
	form_class = PersonaForm
	template_name = 'personas/alta.html'
	success_url = reverse_lazy('personas:listado')
	message_error = "PERSONA YA EXISTE - REINGRESE DATOS"
	cargar_otro_url = reverse_lazy('personas:alta')
	botones = {
		'Volver a listado de Personas':reverse_lazy('personas:listado')
	}

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['empresas'] = pmodels.Empresa.objects.all()
		return context

	def post(self,request, *args, **kwargs):
		response = super(AltaPersona, self).post(request, *args, **kwargs)
		cuitList = request.POST.getlist('empresas')
		persona = pmodels.Persona.objects.get(numeroDocumento=request.POST['numeroDocumento'])
		for cuit in cuitList:
			empresa = pmodels.Empresa.objects.get(cuit=cuit)
			empresa.representantes.add(persona)
			empresa.save()
		return response


class ModificarPersona(UpdateView):
	model = pmodels.Persona
	template_name = 'forms.html'
	form_class = PersonaForm
	success_url = reverse_lazy('personas:listado')

	def get_context_data(self, **kwargs):
		context = super(ModificarPersona, self).get_context_data(**kwargs)
		context['nombreForm'] = 'Editar Persona:'
		context['botones'] = {'Volver a Listado de Personas':reverse('personas:listado')}
		return context

class ListadoPersonas(ListView):
	model = pmodels.Persona
	template_name = 'personas/listado.html'
	context_object_name = 'personas'

	def get_context_data(self, **kwargs):
		context = super(ListadoPersonas, self).get_context_data(**kwargs)
		context['botones'] = {
			'Nueva Persona': reverse('personas:alta'),
		}
		context['nombreReverse'] = 'personas'
		context['headers'] = ['Nombre', 'Apellido','Tipo de Documento', 'Número de Documento']
		context['nombreLista'] = 'Listado de personas'
		context['tipoRoles'] = Persona.tipoRol
		return context

class DetallePersona(DetailView):
	model = pmodels.Persona
	form_class = DetallePersonaForm
	template_name = 'personas/detalle.html'
	context_object_name = 'persona'

	def get_context_data(self, **kwargs):
		context = super(DetallePersona, self).get_context_data(**kwargs)
		context['botones'] = {
			'Volver a Listado de Personas': reverse('personas:listado'),
			'Nueva Persona': reverse('personas:alta'), 
			'Directores': reverse('directores:listado'), 
			'Administrativos':'', 
			'Liquidadores':'',
		}
		context['roles'] = pmodels.Rol.TIPOS 
		return context

class EliminarPersona(DeleteView):
	model = pmodels.Persona
	template_name = 'delete.html'
	success_url = reverse_lazy('personas:listado')

	def get_context_data(self, **kwargs):
		context = super(EliminarPersona, self).get_context_data(**kwargs)
		context['nombreForm'] = 'Eliminar Persona:' + self.object.nombre + self.object.apellido
		context['botones'] = {}
		return context


def promover_a_inspector(request,pk):
	persona = pmodels.Persona.objects.get(pk=pk)
	inspector = Inspector()
	inspector.save()
	persona.agregar_rol(inspector)
	return redirect(reverse('personas:detalle', args=[pk]))

def promover_a_jefe_departamento(request,pk):
	persona = pmodels.Persona.objects.get(pk=pk)
	jefe_departamento = JefeDepartamento()
	jefe_departamento.save()
	persona.agregar_rol(jefe_departamento)
	return redirect(reverse('personas:detalle', args=[pk]))

def promover_a_sumariante(request,pk):
	persona = pmodels.Persona.objects.get(pk=pk)
	sumariante = pmodels.Sumariante()
	sumariante.save()
	persona.agregar_rol(sumariante)
	return redirect(reverse('personas:detalle', args=[pk]))

def promover_a_solicitante(request,pk):
	persona = pmodels.Persona.objects.get(pk=pk)
	solicitante = Solicitante()
	solicitante.save()
	persona.agregar_rol(solicitante)
	return redirect(reverse('personas:detalle', args=[pk]))

def promover_a_liquidador(request,pk):
	persona = pmodels.Persona.objects.get(pk=pk)
	liquidador = Liquidador()
	liquidador.save()
	persona.agregar_rol(liquidador)
	return redirect(reverse('personas:detalle', args=[pk]))

def promover_a_administrativo(request,pk):
	persona = pmodels.Persona.objects.get(pk=pk)
	administrativo = Administrativo()
	administrativo.save()
	persona.agregar_rol(administrativo)
	return redirect(reverse('personas:detalle', args=[pk]))