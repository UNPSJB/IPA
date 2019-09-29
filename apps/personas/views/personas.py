from django.core.urlresolvers import reverse_lazy, reverse
from django.views.generic import DetailView, DeleteView
from django.views import View
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin
from apps.generales.views import GenericAltaView, GenericModificacionView
from apps.personas.models import *
from apps.personas.forms import PersonaForm, ChoferForm, DirectorForm
from apps.personas.tables import PersonaTable, PersonaFilter
from django.http import JsonResponse

class ListadoPersonas(SingleTableMixin, FilterView):
	model = Persona
	template_name = 'personas/listado.html'
	table_class = PersonaTable
	paginate_by = 12
	filterset_class = PersonaFilter

class AltaPersona(GenericAltaView):
	model = Persona
	form_class = PersonaForm
	template_name = 'personas/alta.html'
	success_url = reverse_lazy('personas:listado')
	cargar_otro_url = reverse_lazy('personas:alta')

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['empresas'] = Empresa.objects.all()
		context['roles'] = Persona.tipoRol
		context['director_form'] = DirectorForm
		context['chofer_form'] = ChoferForm
		return context

	def post(self,request, *args, **kwargs):
		import pdb;pdb.set_trace()
		response = super(AltaPersona, self).post(request, *args, **kwargs)
		cuitList = request.POST.getlist('empresas')
		rolesList = request.POST.get('roles')
		rolesList = [] if rolesList == '' else rolesList.split(',')
		persona = Persona.objects.get(numeroDocumento=request.POST['numeroDocumento'])
		for cuit in cuitList:
			empresa = Empresa.objects.get(cuit=cuit)
			empresa.representantes.add(persona)
			empresa.save()
		for rol in rolesList:
			rol_to_add = None
			if rol == 'Director':
				director_form = DirectorForm(request.POST)
				if director_form.is_valid():
					rol_to_add = Director(**director_form.cleaned_data)
			elif rol == 'Chofer':
				chofer_form = ChoferForm(request.POST)
				if chofer_form.is_valid():
					rol_to_add = Chofer(**chofer_form.cleaned_data)
			else:
				rol_to_add = eval(rol)()	
			persona.agregar_rol(rol_to_add)
		return response


class ModificarPersona(GenericModificacionView):
	model = Persona
	form_class = PersonaForm
	success_url = reverse_lazy('personas:listado')
	nombre_form = 'Editar persona'
	botones = {
		'Volver a listado de Personas':reverse_lazy('personas:listado')
	}

class DetallePersona(View):
	def get(self, request, *args, **kwargs):
		persona = Persona.objects.get(id=kwargs.get('pk'))
		return JsonResponse({
			"nombre": persona.nombre,
			"apellido" : persona.apellido,
			"email": persona.email,
			"tipoDocumento": persona.get_tipoDocumento_display(),
			"numeroDocumento":persona.numeroDocumento,
			"direccion": persona.direccion,
			"telefono": persona.telefono
		})



class EliminarPersona(DeleteView):
	model = Persona
	template_name = 'delete.html'
	success_url = reverse_lazy('personas:listado')

	def get_context_data(self, **kwargs):
		context = super(EliminarPersona, self).get_context_data(**kwargs)
		context['nombreForm'] = 'Eliminar Persona:' + self.object.nombre + self.object.apellido
		context['botones'] = {}
		return context
