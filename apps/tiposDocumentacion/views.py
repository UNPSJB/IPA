from django.urls import reverse_lazy
from .models import TipoDocumentacion
from .forms import TipoDocumentacionForm
from django.views.generic import ListView,CreateView,DeleteView,DetailView, UpdateView


# Create your views here.
class AltaTipoDocumentacion(CreateView):
	model = TipoDocumentacion
	form_class = TipoDocumentacionForm
	template_name = 'forms.html'
	success_url = reverse_lazy('tipoDocumentacion:listado')

	def get_context_data(self, **kwargs):
		context = super(AltaTipoDocumentacion, self).get_context_data(**kwargs)
		context['nombreLista'] = "Tipos de Documentación"
		context['headers'] = ['Nombre']
		context['botones'] = {'Alta': '/documentos/alta', 'Listado':'/documentos/listar'}
		return context

class DetalleTipoDocumentacion(DetailView):
	model = TipoDocumentacion
	template_name = 'tipoDocumentacion/detalle.html'		

class ListadoTipoDocumentacion(ListView):
	model = TipoDocumentacion
	template_name = 'tipoDocumentacion/listado.html'
	context_object_name = 'documentos'

	def get_context_data(self, **kwargs):
		context = super(ListadoTipoDocumentacion, self).get_context_data(**kwargs)
		context['nombreLista'] = "Tipos de Documentación"
		context['headers'] = ['Nombre']
		context['botones'] = {'Alta': '/documentos/alta', 'Listado':'/documentos/listar'}
		return context


class ModificarTipoDocumentacion(UpdateView):
	model = TipoDocumentacion
	form_class = TipoDocumentacionForm
	template_name = 'forms.html'
	success_url = reverse_lazy('tipoDocumentacion:listar')

	def post(self, request, *args, **kwargs):
		self.object = self.get_object
		id_afluente = kwargs['pk']
		afluente = self.model.objects.get(id=id_tipoDocumentacion)
		form = self.form_class(request.POST, instance=tipoDocumentacion)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(self.get_success_url())
		else:
			return HttpResponseRedirect(self.get_success_url())

class TipoDocumentacionDelete(DeleteView):
	model = TipoDocumentacion
	template_name = 'tipoDocumentacion/delete.html'
	success_url = reverse_lazy('tipoDocumentacion:listado')
