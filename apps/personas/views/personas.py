from django.core.urlresolvers import reverse_lazy, reverse
from django.views.generic import DeleteView
from django.views import View
from apps.personas.models import *
from apps.personas.forms import PersonaForm, ChoferForm, DirectorForm
from apps.personas.tables import PersonaTable
from apps.personas.filters import PersonaFilter
from django.http import HttpResponseRedirect, JsonResponse
from apps.generales.views import GenericAltaView,GenericDetalleView,GenericListadoView,GenericModificacionView
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin


class ListadoPersonas(GenericListadoView):
	model = Persona
	template_name = 'personas/listado.html'
	table_class = PersonaTable
	paginate_by = 10
	filterset_class = PersonaFilter
	export_name = 'listado_personas'
	permission_required = 'personas.listar_persona'
	redirect_url = '/'

class AltaPersona(GenericAltaView):
	model = Persona
	form_class = PersonaForm
	template_name = 'personas/alta.html'
	success_url = reverse_lazy('personas:listado')
	cargar_otro_url = reverse_lazy('personas:alta')
	permission_required = 'personas.cargar_persona'
	redirect_url = 'personas:listado'

	def get_context_alta(self, context):
		context['roles'] = Persona.tipoRol
		context['director_form'] = DirectorForm()
		context['chofer_form'] = ChoferForm()
		context['nombreForm'] = "Nueva Persona"
		if context['return_label'] == None:
			context['return_label'] = "Listado de Personas"
		context['ayuda'] = 'solicitante.html#como-crear-una-nueva-persona'	
		return context

	def get_context_data(self, *args, **kwargs):
		context = super(AltaPersona, self).get_context_data(**kwargs)
		context['return_path'] = self.request.GET.get('return_path', self.success_url)
		return self.get_context_alta(context)

	def post(self,request, *args, **kwargs):
		form = self.form_class(request.POST)
		if form.is_valid():
			response = super(AltaPersona, self).post(request,*args, **kwargs)
			rolesList = request.POST.get('roles')
			rolesList = [] if (rolesList == '' or rolesList==None) else rolesList.split(',')
			persona = Persona.objects.get(numeroDocumento=request.POST['numeroDocumento'])
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
			#return HttpResponseRedirect(reverse('personas:listado'))
			return response
		return render(request, self.template_name, self.get_context_alta({'form':form,'message_error':form.non_field_errors(),'return_path':'/personas/listado','return_label':'Listado de Personas'}))
		

class ModificarPersona(GenericModificacionView):
	model = Persona
	form_class = PersonaForm
	success_url = reverse_lazy('personas:listado')
	template_name = 'personas/modificar.html'
	permission_required = 'personas.modificar_persona'
	redirect_url = 'personas:listado'


	def get_context_modificar(self, context):
		context['roles'] = Persona.tipoRol
		context['director_form'] = DirectorForm()
		context['chofer_form'] = ChoferForm()
		context['nombreForm'] = "Modificar Persona"
		context['return_label'] = "Listado de Personas"
		context['return_path']= reverse('personas:listado')
		context['empresas'] = Empresa.objects.filter(representantes__in=[self.object])

		if self.object.sos(Director):
			context['director_form'] = DirectorForm(instance=self.object.como(Director))
		else:
			context['director_form'] = DirectorForm()
		if self.object.sos(Chofer):
			context['chofer_form'] = ChoferForm(instance=self.object.como(Chofer))
		else:
			context['chofer_form'] = ChoferForm()
		context['ayuda'] = ''
		return context

	def get_context_data(self, **kwargs):
		context = super(ModificarPersona, self).get_context_data(**kwargs)
		return self.get_context_modificar(context)

	def get (self, request, *args, **kwargs):
		self.object = self.get_object()
		return super(ModificarPersona, self).get(request,*args,**kwargs)

	def post(self,request, *args, **kwargs):
		obj = self.get_object()
		self.object = self.get_object()
		form = self.form_class(request.POST, instance=self.object)

		if form.is_valid():
			response = super(ModificarPersona, self).post(request, *args, **kwargs)
			return response
		return render(request, self.template_name, self.get_context_modificar({'form':form,'message_error':form.non_field_errors(), 'object':self.object,'return_path':'/personas/listado','return_label':'Listado de Personas'}))

class DetallePersona(GenericDetalleView):
	model = Persona
	template_name = 'personas/detalle.html'
	permission_required = 'personas.detalle_persona'
	redirect_url = 'personas:listado'

	def get_context_data(self, **kwargs):
		context = super(DetallePersona, self).get_context_data(**kwargs)
		context['nombreDetalle'] = ' Persona'
		context['return_label'] = 'Listado Personas'
		context['return_path']= reverse('personas:listado')
		context['ayuda'] = 'solicitante.html#como-crear-una-nueva-persona'
		return context

class EliminarPersona(LoginRequiredMixin,DeleteView):
	model = Persona
	success_url = reverse_lazy('personas:listado')
	permission_required = 'personas.eliminar_persona'
	redirect_url = 'personas:listado'
	
	def delete(self, request, *args, **kwargs):
		if not request.user.has_perm(self.permission_required):
			return JsonResponse({"success": False,"message": ('permiso',"No posee los permisos necesarios para realizar esta operación")})
		try:
			self.object = self.get_object()
			self.object.delete()

			return JsonResponse({
				"success": True
			})
		except Exception as e:
			return JsonResponse({
				"success": False,
				"message": ('error',"No se pudo eliminar esta persona")
			})