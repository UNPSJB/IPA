from django.urls import reverse_lazy, reverse
from .models import TipoDocumento, Documento
from .forms import TipoDocumentoForm, DocumentoForm
from django.views.generic import ListView,CreateView,DeleteView,DetailView, UpdateView
from django.views import View
from apps.permisos.models import Permiso
from django.shortcuts import render
from django.http import HttpResponseRedirect
from datetime import date, datetime
from operator import attrgetter

class AltaTipoDocumento(CreateView):
	model = TipoDocumento
	form_class = TipoDocumentoForm
	template_name = 'forms.html'
	success_url = reverse_lazy('tipoDocumentos:listar')

	def get_context_data(self, **kwargs):
		context = super(AltaTipoDocumento, self).get_context_data(**kwargs)
		context['nombreForm'] = "Nuevo Tipo de Documento"
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
		context['nombreLista'] = "Listado de Tipos de Documento"
		context['headers'] = ['Nombre']
		context['botones'] = {
			'Nuevo Tipo de Documento': reverse('tipoDocumentos:alta'),
			'Salir': reverse('index')
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

	def get_context_data(self, *args, **kwargs):
		context = super(AltaDocumento, self).get_context_data(**kwargs)
		context['botones'] = {
		'Volver a Detalle de Solicitud': reverse('solicitudes:detalle', args=[self.permiso_pk])
		}
		context['nombreForm'] = 'Documentos'
		return context

	def get (self, request, *args, **kwargs):
		self.permiso_pk = kwargs.get('pk')
		return super(AltaDocumento, self).get(request,*args,**kwargs)

	def post(self, request, *args, **kwargs):
		self.object = self.get_object
		form = self.form_class(request.POST, request.FILES)
		permiso = Permiso.objects.get(pk=kwargs.get('pk'))
		
		if form.is_valid(): #AGREGAR CONDICION DE QUE LA DOCUMENTACION NO ESTE DUPLICADO
			documento = form.save()
			permiso.agregar_documentacion(documento)
			return HttpResponseRedirect(reverse('solicitudes:detalle', args=[permiso.id]))
		return self.render_to_response(self.get_context_data(form=form))

class DetalleDocumento(DetailView):
	model = Documento
	template_name = 'Documento/detalle.html'

class ListadoDocumentacionPresentada(ListView):
	model = Documento
	template_name = 'Documento/listado.html'
	context_object_name = 'documentos'

	def get_context_data(self, **kwargs):
		context = super(ListadoDocumentacionPresentada, self).get_context_data(**kwargs)
		context['nombreLista'] = 'Listado de Documentos'
		context['headers'] = ['Tipo', 'Descripcion', 'Fecha']
		context['botones'] = {
		#'Alta': reverse('documentos:alta') , 
		'Listado': reverse('documentos:listar'),
        #'Volver a Detalle de Solicitud': reverse('solicitudes:detalle', args=[self.permiso_pk])
		}
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


class AgregarExpediente(CreateView):
	model = Documento
	form_class = DocumentoForm
	template_name = 'Documento/expediente.html'

	def get_success_url(self):
		return reverse('permisos:detallePermisoCompleto', args=(self.permiso_pk, ))

	def get_context_data(self, *args, **kwargs):
		context = super(AgregarExpediente, self).get_context_data(**kwargs)
		context['botones'] = {
		'Volver a Detalle de Solicitud': reverse('solicitudes:detalle', args=[self.permiso_pk])
		}
		context['nombreForm'] = 'Agregar Expediente a Permiso'
		return context

	def get (self, request, *args, **kwargs):
		self.permiso_pk = kwargs.get('pk')
		return super(AgregarExpediente, self).get(request,*args,**kwargs)

	def post(self, request, *args, **kwargs):
		self.object = self.get_object
		self.permiso_pk = kwargs.get('pk')
		form = self.form_class(request.POST, request.FILES)
		permiso = Permiso.objects.get(pk=self.permiso_pk)
		
		fechaExpediente=datetime.strptime(form.data['fecha'], "%Y-%m-%d").date()
		lista_fechas = [documento.fecha for documento in permiso.documentos.all() if documento.fecha > fechaExpediente]
		if len(lista_fechas) != 0:
			lista_fechas.sort()
			ultima_fecha = lista_fechas.pop()

		if form.is_valid(): #AGREGAR CONDICION DE QUE LA DOCUMENTACION NO ESTE DUPLICADO
			if len(lista_fechas) == 0:
				documento = form.save()
				permiso.hacer('completar',request.user,fechaExpediente, request.POST['expediente'], documento)
				return HttpResponseRedirect(self.get_success_url())
			else:
				return self.render_to_response(self.get_context_data(form=form, 
					message = 'La fecha de Expediente debe ser posterior a la fecha de la ultima documentacion presentada ('+(ultima_fecha).strftime("%d-%m-%Y")+')'))
		return self.render_to_response(self.get_context_data(form=form))

class AgregarEdicto(CreateView):
	model = Documento
	form_class = DocumentoForm
	template_name = 'Documento/edicto.html'
	
	def get_success_url(self):
		return reverse('permisos:detallePermisoPublicado', args=(self.permiso_pk, ))

	def get_context_data(self, *args, **kwargs):
		context = super(AgregarEdicto, self).get_context_data(**kwargs)
		context['botones'] = {
		'Volver a Detalle de Solicitud': reverse('solicitudes:detalle', args=[self.permiso_pk])
		}
		context['nombreForm'] = 'Agregar Edicto a Permiso'
		return context

	def get (self, request, *args, **kwargs):
		self.permiso_pk = kwargs.get('pk')
		return super(AgregarEdicto, self).get(request,*args,**kwargs)

	def post(self, request, *args, **kwargs):
		self.object = self.get_object
		self.permiso_pk = kwargs.get('pk')
		form = self.form_class(request.POST, request.FILES)
		permiso = Permiso.objects.get(pk=self.permiso_pk)
		documentos = permiso.documentos.all()
		pase = [documento for documento in documentos if (documento.tipo.nombre == 'Pase')] #FIXME: VA TIPO DEFINIDO PARA PASE
		
		fecha_pase = pase[0].fecha

		fechaEdicto=datetime.strptime(form.data['fecha'], "%Y-%m-%d").date()

		tiempo = int(form.data['tiempo'])

		if form.is_valid():
			if (fechaEdicto > fecha_pase) and (tiempo > 0):
				edicto = form.save()
				permiso.hacer('publicar',request.user,edicto.fecha, tiempo, edicto)
				return HttpResponseRedirect(self.get_success_url())
			else:
				return self.render_to_response(self.get_context_data(form=form, 
					message = 'La fecha del Edicto debe ser posterior a la fecha del Expediente ('+(fecha_pase).strftime("%d-%m-%Y")+
					') y el tiempo de publicación mayor a CERO'))
		return self.render_to_response(self.get_context_data(form=form))

class AgregarResolucion(CreateView):
	model = Documento
	form_class = DocumentoForm
	template_name = 'Documento/resolucion.html'

	def get_success_url(self):
		return reverse('permisos:detallePermisoOtorgado', args=(self.permiso_pk, ))

	def get_context_data(self, *args, **kwargs):
		context = super(AgregarResolucion, self).get_context_data(**kwargs)
		context['botones'] = {
		'Volver a Detalle de Solicitud': reverse('solicitudes:detalle', args=[self.permiso_pk])
		}
		context['permiso'] = Permiso.objects.get(pk=self.permiso_pk)
		context['nombreForm'] = 'Agregar Resolución a Permiso'
		return context

	def get (self, request, *args, **kwargs):
		self.permiso_pk = kwargs.get('pk')
		return super(AgregarResolucion, self).get(request,*args,**kwargs)

	def post(self, request, *args, **kwargs):
		self.object = self.get_object
		self.permiso_pk = kwargs.get('pk')
		form = self.form_class(request.POST, request.FILES)
		permiso = Permiso.objects.get(pk=self.permiso_pk)
		documentos = permiso.documentos.all()

		fechaResolucion=datetime.strptime(form.data['fecha'], "%Y-%m-%d").date()
		fechaPrimerCobro=datetime.strptime(form.data['fechaPrimerCobro'], "%Y-%m-%d").date()
		fechaVencimiento=datetime.strptime(form.data['fechaVencimiento'], "%Y-%m-%d").date()
		unidad = int(request.POST['unidad'])

		lista_resoluciones = [documento for documento in documentos if (documento.tipo.nombre == 'Resolucion')] #FIXME: VA TIPO DEFINIDO PARA PASE
		lista_resoluciones_fecha = sorted(lista_resoluciones, key=attrgetter('fecha'), reverse=True)
		
		if len(lista_resoluciones_fecha) > 0:
			ultimo_vencimiento_resolucion = lista_resoluciones_fecha[0].fechaVencimiento
			fecha_correcta = fechaResolucion > ultimo_vencimiento_resolucion
		else:
			fecha_correcta = fechaResolucion > permiso.estado().vencimientoPublicacion()

		if form.is_valid():
			if fecha_correcta and (unidad > 0) and (fechaVencimiento > fechaResolucion):
				resolucion = form.save()
				permiso.hacer('resolver',request.user,resolucion.fecha, unidad, resolucion, fechaPrimerCobro, fechaVencimiento)
				return HttpResponseRedirect(self.get_success_url())
			elif (unidad <= 0) or (fechaVencimiento < fechaResolucion):
				return self.render_to_response(self.get_context_data(form=form, 
					message="La Fecha de Vencimiento debe ser mayor a la Fecha de la Resolución, y la Unidad mayor a CERO"))
			else:
				return self.render_to_response(self.get_context_data(form=form, 
					message="La Fecha de la Resolucion debe ser mayor a la Fecha de Vencimiento de la Ultima Resolución cargada (" +  (ultimo_vencimiento_resolucion).strftime("%d-%m-%Y") + ")"))
		return self.render_to_response(self.get_context_data(form=form))


class AgregarOposicion(CreateView):
	model = Documento
	form_class = DocumentoForm
	template_name = 'formsInput.html'
	success_url = reverse_lazy('documentos:listar')

	def get_context_data(self, *args, **kwargs):
		context = super(AgregarOposicion, self).get_context_data(**kwargs)
		context['botones'] = {
			#'Volver a Permiso Publicado': reverse('permisos:detallePermisoPublicado', args=[self.permiso_pk])
		}
		context['nombreForm'] = 'Agregar Oposición a Permiso'
		context['message_error'] = ''
		return context

	def get (self, request, *args, **kwargs):
		self.permiso_pk = kwargs.get('pk')
		return super(AgregarOposicion, self).get(request,*args,**kwargs)

	def post(self, request, *args, **kwargs):
		self.object = self.get_object
		form = self.form_class(request.POST, request.FILES)
		permiso = Permiso.objects.get(pk=kwargs.get('pk'))
		
		fechaVencimiento = permiso.estado().vencimientoPublicacion()

		if form.is_valid() and (request.POST['fecha'] <= fechaVencimiento.strftime('%d/%m/%Y')):
			resolucion = form.save()
			permiso.hacer('darDeBaja',request.user,date.today(), resolucion)
			return HttpResponseRedirect(self.get_success_url())

		return self.render_to_response(self.get_context_data(form=form))

class AgregarInfraccion(CreateView):
	model = Documento
	form_class = DocumentoForm
	template_name = 'Documento/infraccion.html'
	success_url = reverse_lazy('documentos:listar')

	def get_context_data(self, *args, **kwargs):
		context = super(AgregarInfraccion, self).get_context_data(**kwargs)
		context['botones'] = {
		'Volver a Detalle de Solicitud': reverse('solicitudes:detalle', args=[self.permiso_pk])
		}
		context['nombreForm'] = 'Acta de Infraccion'
		return context

	def get (self, request, *args, **kwargs):
		self.permiso_pk = kwargs.get('pk')
		return super(AgregarInfraccion, self).get(request,*args,**kwargs)

	def post(self, request, *args, **kwargs):
		self.object = self.get_object
		form = self.form_class(request.POST, request.FILES)
		permiso = Permiso.objects.get(pk=kwargs.get('pk'))
		
		if form.is_valid():
			documento = form.save()
			permiso.agregar_documentacion(documento)
			return HttpResponseRedirect(reverse('solicitudes:detalle', args=[permiso.id]))
			return self.render_to_response(self.get_context_data(form=form))
