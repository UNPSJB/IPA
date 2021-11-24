from django.core.urlresolvers import reverse_lazy, reverse
from django.views.generic import DetailView, DeleteView, UpdateView
from django.views import View
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin
from apps.generales.views import GenericAltaView
from apps.personas.models import *
from apps.personas.forms import PersonaForm, ChoferForm, DirectorForm
from apps.personas.tables import PersonaTable, PersonaFilter
from django.http import JsonResponse

from apps.generales.views import GenericListadoView

class ListadoPersonas(GenericListadoView):
	model = Persona
	template_name = 'personas/listado.html'
	table_class = PersonaTable
	paginate_by = 12
	filterset_class = PersonaFilter
	export_name = 'listado_personas'

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
		context['director_form'] = DirectorForm()
		context['chofer_form'] = ChoferForm()
		context['return_path'] = self.request.GET.get('return_path', self.success_url)
		context['ayuda'] = 'solicitante.html#como-crear-una-nueva-persona'
		return context

	def post(self,request, *args, **kwargs):
		response = super(AltaPersona, self).post(request,*args, **kwargs)
		cuitList = request.POST.get('empresas')
		cuitList = [] if cuitList == '' else cuitList.split(',')
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

class ModificarPersona(UpdateView):
	model = Persona
	form_class = PersonaForm
	success_url = reverse_lazy('personas:listado')
	template_name = 'personas/alta.html'

	def get_context_data(self, **kwargs):
		context = super(ModificarPersona, self).get_context_data(**kwargs)
		obj = context['object']
		context['empresas'] = obj.empresa_set.values('id').all()
		context['roles'] = Persona.tipoRol		
		if obj.sos(Director):
			context['director_form'] = DirectorForm(instance=obj.como(Director))
		else:
			context['director_form'] = DirectorForm()
		if obj.sos(Chofer):
			context['chofer_form'] = ChoferForm(instance=obj.como(Chofer))
		else:
			context['chofer_form'] = ChoferForm()
		return context

	def post(self,request, *args, **kwargs):
		response = super(ModificarPersona, self).post(request, *args, **kwargs)
		cuitList = request.POST.get('empresas')
		cuitList = [] if cuitList == '' else cuitList.split(',')
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

class DetallePersona(View):
	def get(self, request, *args, **kwargs):
		persona = Persona.objects.get(id=kwargs.get('pk'))
		empresas_relacionadas = persona.empresa_set.all()		
		lista_empresas = []
		for empresa in empresas_relacionadas:
			lista_empresas.append({ "cuit": empresa.cuit, "razonSocial": empresa.razonSocial })

		roles_relacionados = persona.roles_related()		
		lista_roles = []
		for rol in roles_relacionados:
			lista_roles.append({"tipo": rol.roleName()})

		return JsonResponse({
			"nombre": persona.nombre,
			"apellido" : persona.apellido,
			"email": persona.email,
			"tipoDocumento": persona.get_tipoDocumento_display(),
			"numeroDocumento":persona.numeroDocumento,
			"direccion": persona.direccion,
			"telefono": persona.telefono,
			"empresas": lista_empresas,
			"roles": lista_roles
		})

class EliminarPersona(DeleteView):
	model = Persona
	success_url = reverse_lazy('personas:listado')
	
	def delete(self, request, *args, **kwargs):
		try:
			self.object = self.get_object()
			self.object.delete()

			return JsonResponse({
				"success": True
			})
		except Error as e:
			return JsonResponse({
				"success": False,
				"message": e.value()
			})