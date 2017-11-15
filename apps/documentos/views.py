from django.urls import reverse_lazy, reverse
from .models import TipoDocumento, Documento
from .forms import TipoDocumentoForm, DocumentoForm
from django.views.generic import ListView,CreateView,DeleteView,DetailView, UpdateView


# Create your views here.
class AltaTipoDocumento(CreateView):
	model = TipoDocumento
	form_class = TipoDocumentoForm
	template_name = 'forms.html'
	success_url = reverse_lazy('tipoDocumentos:listar')

	def get_context_data(self, **kwargs):
		context = super(AltaTipoDocumento, self).get_context_data(**kwargs)
		context['nombreForm'] = "Nuevo tipo de documento"
		context['headers'] = ['Nombre']
		context['botones'] = {
			'Listado':reverse('tipoDocumentos:listar'),
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
		context = super(ListadoTipoDocumentos, self).get_context_data(**kwargs)
		context['nombreLista'] = "Listado de tipos de documento"
		context['headers'] = ['Nombre']
		context['botones'] = {
			'Alta': reverse('tipoDocumentos:alta')
			}
		return context


class ModificarTipoDocumento(UpdateView):
	model = TipoDocumento
	form_class = TipoDocumentoForm
	template_name = 'forms.html'
	success_url = reverse_lazy('tipoDocumentos:listar')

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
	success_url = reverse_lazy('tipoDocumentos:listar')

# Documentos
class AltaDocumento(CreateView):
	model = Documento
	form_class = DocumentoForm
	template_name = 'formsInput.html'
	success_url = reverse_lazy('documentos:listar')

	def get_context_data(self, **kwargs):
		context = super(AltaDocumento, self).get_context_data(**kwargs)
		context['botones'] = {'Alta': reverse('documentos:alta') , 'Listado': reverse('documentos:listar')}
		context['nombreForm'] = 'documentos'
		return context

class DetalleDocumento(DetailView):
	model = Documento
	template_name = 'Documento/detalle.html'

class ListadoDocumento(ListView):
	model = Documento
	template_name = 'Documento/listado.html'
	context_object_name = 'Documentos'

	def get_context_data(self, **kwargs):
		context = super(ListadoDocumento, self).get_context_data(**kwargs)
		context['nombreLista'] = 'Listado de Documentos'
		context['headers'] = ['Tipo', 'Descripcion', 'Fecha']
		context['botones'] = {'Alta': reverse('documentos:alta') , 'Listado': reverse('documentos:listar')}
		return context

class ModificarDocumento(UpdateView):
	model = Documento
	form_class = DocumentoForm
	template_name = 'Documento/form.html'
	success_url = reverse_lazy('documentos:listar')

	def post(self, request, *args, **kwargs):
		self.object = self.get_object
		id_documento = kwargs['pk']
		documento = self.model.objects.get(id=id_documento)
		form = self.form_class(request.POST, instance=documento)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(self.get_success_url())
		else:
			return HttpResponseRedirect(self.get_success_url())

class DeleteDocumento(DeleteView):
	model = Documento
	template_name = 'Documento/delete.html'
	success_url = reverse_lazy('documentos:listar')
