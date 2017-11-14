from django.urls import reverse_lazy
from .models import TipoDocumento
from .forms import TipoDocumentoForm
from django.views.generic import ListView,CreateView,DeleteView,DetailView, UpdateView


# Create your views here.
class AltaTipoDocumento(CreateView):
	model = TipoDocumento
	form_class = TipoDocumentoForm
	template_name = 'forms.html'
	success_url = reverse_lazy('tipoDocumento:listar')

	def get_context_data(self, **kwargs):
		context = super(AltaTipoDocumento, self).get_context_data(**kwargs)
		context['nombreForm'] = "Nuevo tipo de documento"
		context['headers'] = ['Nombre']
		context['botones'] = {
			'Listado':reverse('tipoDocumento:listar'),
			}
		return context

class DetalleTipoDocumento(DetailView):
	model = TipoDocumento
	template_name = 'tipoDocumento/detalle.html'		

class ListadoTipoDocumentos(ListView):
	model = TipoDocumento
	template_name = 'tipoDocumento/listado.html'
	context_object_name = 'documentos'

	def get_context_data(self, **kwargs):
		context = super(ListadoTipoDocumento, self).get_context_data(**kwargs)
		context['nombreLista'] = "Listado de tipos de documento"
		context['headers'] = ['Nombre']
		context['botones'] = {
			'Alta': reverse('tipoDocumento:alta')
			}
		return context


class ModificarTipoDocumento(UpdateView):
	model = TipoDocumento
	form_class = TipoDocumentoForm
	template_name = 'forms.html'
	success_url = reverse_lazy('tipoDocumento:listar')

	def post(self, request, *args, **kwargs):
		self.object = self.get_object
		id_afluente = kwargs['pk']
		afluente = self.model.objects.get(id=id_tipoDocumento)
		form = self.form_class(request.POST, instance=tipoDocumento)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(self.get_success_url())
		else:
			return HttpResponseRedirect(self.get_success_url())

class DeleteTipoDocumento(DeleteView):
	model = TipoDocumento
	template_name = 'delete.html'
	success_url = reverse_lazy('tipoDocumento:listar')
