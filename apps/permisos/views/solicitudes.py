from django.urls import reverse_lazy, reverse
from ..models import Permiso
from ..forms import PermisoForm, SolicitadoForm
from django.views import View
from django.shortcuts import render, redirect
from django.views.generic import ListView,DeleteView,DetailView

class AltaSolicitud(View):
	model = Permiso
	template_name = 'solicitudes/alta.html'
	success_url = reverse_lazy('solicitudes:listar')

	def get(self,request): 
		context = {}
		context['forms'] = {
			'permiso': PermisoForm(),
			'solicitado': SolicitadoForm(),
		} 
		
		context['botones'] = {
				'Listado': reverse('solicitudes:listar'),
				'Agregar Persona' : reverse('personas:alta'),
				'Agregar Establecimiento': reverse('establecimientos:alta'),
				'Agregar Tipo de Uso': reverse('tiposDeUso:alta'),
				'Agregar Afluente': reverse('afluentes:alta'),
		}
		
		return render(request, self.template_name, context)

	def post(self, request):
		permiso_form = PermisoForm(request.POST)
		solicitado_form = SolicitadoForm(request.POST)
		if permiso_form.is_valid() and solicitado_form.is_valid():
			permiso = permiso_form.save()
			solicitado = solicitado_form.save(commit=False)
			solicitado.permiso = permiso
			solicitado.usuario = request.user
			solicitado.save()
			return redirect('solicitudes:listar')
		print(solicitado_form.errors)
		return redirect('solicitudes:alta')

	def form_invalid(self,form):
		print(form)

class DetalleSolicitud(DetailView):
	model = Permiso
	template_name = 'permiso/detalle.html'		

class ListadoSolicitudes(ListView):
	model = Permiso
	template_name = 'solicitudes/listado.html'
	context_object_name = 'solicitudes'

	def get_context_data(self, **kwargs):
		context = super(ListadoSolicitudes, self).get_context_data(**kwargs)
		context['nombreLista'] = "Lista de Solicitudes"
		context['nombreReverse'] = "solicitudes"
		context['headers'] = ['Solicitante', 'Establecimiento', 'Tipo', 'Estado']
		context['botones'] = {'Alta': reverse('solicitudes:alta')}
		return context

class SolicitudDelete(DeleteView):
	model = Permiso
	template_name = 'delete.html'
	success_url = reverse_lazy('solicitudes:listar')
