from django.urls import reverse_lazy, reverse
from .models import TipoDocumento, Documento
from .forms import TipoDocumentoForm, DocumentoForm, DocumentoProtegidoForm, DocumentoActaInspeccionProtegidoForm
from django.views.generic import ListView,CreateView,DeleteView,DetailView, UpdateView
from apps.permisos.models import Permiso
from apps.comisiones.models import Comision
from django.http import HttpResponseRedirect
from datetime import date, datetime
from operator import attrgetter
from apps.generales.views import GenericAltaView

class AltaTipoDocumento(GenericAltaView):
	model = TipoDocumento
	form_class = TipoDocumentoForm
	template_name = 'tipoDocumento/alta.html'
	success_url = reverse_lazy('tipoDocumentos:listado')
	cargar_otro_url = reverse_lazy('tipoDocumentos:alta')

class DetalleTipoDocumento(DetailView):
	model = TipoDocumento
	template_name = 'tipoDocumento/detalle.html'		
	context_object_name = 'tipoDocumento'
	
	def get_context_data(self, **kwargs):
		context = super(DetalleTipoDocumento, self).get_context_data(**kwargs)
		context['nombreDetalle'] = 'Detalle de Tipo de Documento'
		context['botones'] = {
			'ir a Listado': reverse('tipoDocumentos:listado'),
			'Nuevo Tipo de Documento': reverse ('tipoDocumentos:alta'),
			'Modificar Tipo de Documento': reverse('tipoDocumentos:modificar', args=[self.object.id]),
			'Eliminar Tipo de Documento': reverse('tipoDocumentos:eliminar', args=[self.object.id]),
		}
		return context


class ListadoTipoDocumentos(ListView):
	model = TipoDocumento
	template_name = 'tipoDocumento/listado.html'
	context_object_name = 'tipoDocumentos'

	def get_context_data(self, **kwargs):
		context = super(ListadoTipoDocumentos, self).get_context_data(**kwargs)
		context['nombreLista'] = "Listado Tipos de Documento"
		context['nombreReverse'] = 'tipoDocumentos'
		context['headers'] = ['Nombre']
		context['botones'] = {
			'Nuevo Tipo de Documento': reverse('tipoDocumentos:alta'),
			'Ir a Tipos de Uso': reverse ('tiposDeUso:listar'),
			}
		return context


class ModificarTipoDocumento(UpdateView):
	model = TipoDocumento
	form_class = TipoDocumentoForm
	template_name = 'forms.html'
	success_url = reverse_lazy('tipoDocumentos:listado')

	def post(self, request, *args, **kwargs):
		self.object = self.get_object
		id_tipoDocumento = kwargs['pk']
		tipoDocumento = self.model.objects.get(id=id_tipoDocumento)
		form = self.form_class(request.POST, instance=tipoDocumento)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(self.get_success_url())
		else:
			return HttpResponseRedirect(self.get_success_url())

	def get_context_data(self, **kwargs):
		context = super(ModificarTipoDocumento, self).get_context_data(**kwargs)
		context['nombreForm'] = "Modificar Tipo Documento"
		context['botones'] = {
			'Ir a Listado': reverse('tipoDocumentos:listado'),
			}
		return context

class DeleteTipoDocumento(DeleteView):
	model = TipoDocumento
	template_name = 'delete.html'
	success_url = reverse_lazy('tipoDocumentos:listado')

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
		context['form'].fields['tipo'].queryset = Permiso.objects.get(pk=self.permiso_pk).tipos_de_documentos_faltantes()
		return context
	
	def get (self, request, *args, **kwargs):
		self.permiso_pk = kwargs.get('pk')
		return super(AltaDocumento, self).get(request,*args,**kwargs)

	def post(self, request, *args, **kwargs):
		self.object = self.get_object
		self.permiso_pk = kwargs.get('pk')

		form = self.form_class(request.POST, request.FILES)
		permiso = Permiso.objects.get(pk=kwargs.get('pk'))
		fs = datetime.strptime(form.data['fecha'], "%Y-%m-%d").date()
		if form.is_valid() and (permiso.fechaSolicitud <= fs): #AGREGAR CONDICION DE QUE LA DOCUMENTACION NO ESTE DUPLICADO
			documento = form.save()
			permiso.agregar_documentacion(documento)
			return HttpResponseRedirect(reverse('solicitudes:detalle', args=[permiso.id]))
		messages = []
		messages = ['La fecha del documento presentado debe ser igual o mayor que la fecha de la solicitud de permiso (' + permiso.fechaSolicitud.strftime("%d/%m/%Y")+')']
		return self.render_to_response(self.get_context_data(form=form, messages=messages))

class DetalleDocumento(DetailView):
	model = Documento
	template_name = 'Documento/detalle.html'

	
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
	form_class = DocumentoProtegidoForm
	template_name = 'Documento/expediente.html'

	def get_success_url(self):
		return reverse('permisos:detalle', args=(self.permiso_pk, ))

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
		#Refactorizar a una funcion de modelo
		lista_fechas = [documento.fecha for documento in permiso.documentos.all() if documento.fecha > fechaExpediente]
		if len(lista_fechas) != 0:
			lista_fechas.sort()
			ultima_fecha = lista_fechas.pop()
		
		if form.is_valid(): #AGREGAR CONDICION DE QUE LA DOCUMENTACION NO ESTE DUPLICADO
			if len(lista_fechas) == 0:
				documento = form.save()
				documento.tipo = TipoDocumento.get_protegido('pase')
				documento.visado = True
				documento.save()
				permiso.hacer('completar',request.user,fechaExpediente, int(request.POST['expediente']), documento)
				return HttpResponseRedirect(self.get_success_url())
			else:
				return self.render_to_response(self.get_context_data(form=form, 
					message = 'La fecha de Expediente debe ser posterior a la fecha de la ultima documentacion presentada ('+(ultima_fecha).strftime("%d-%m-%Y")+')'))
		return self.render_to_response(self.get_context_data(form=form))

class AgregarEdicto(CreateView):
	model = Documento
	form_class = DocumentoProtegidoForm
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
		pase = [documento for documento in documentos if (documento.tipo.slug == 'pase')] #FIXME: VA TIPO DEFINIDO PARA PASE
		
		fecha_pase = pase[0].fecha

		fechaEdicto=datetime.strptime(form.data['fecha'], "%Y-%m-%d").date()

		tiempo = int(form.data['tiempo'])

		if form.is_valid():
			if (fechaEdicto >= fecha_pase) and (tiempo > 0):
				edicto = form.save()
				edicto.tipo = TipoDocumento.get_protegido('edicto')
				edicto.visado = True
				edicto.save()
				permiso.hacer('publicar',request.user,edicto.fecha, tiempo, edicto)
				return HttpResponseRedirect(self.get_success_url())
			else:
				return self.render_to_response(self.get_context_data(form=form, 
					message = 'La fecha del Edicto debe igual o posterior a la fecha del Expediente ('+(fecha_pase).strftime("%d-%m-%Y")+
					') y el tiempo de publicación mayor a CERO'))
		return self.render_to_response(self.get_context_data(form=form))

class AgregarResolucion(CreateView):
	model = Documento
	form_class = DocumentoProtegidoForm
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
		#listaResoluciones = [documento for documento in documentos if (documento.tipo.nombre == 'Resolucion')] #FIXME: VA TIPO DEFINIDO PARA PASE
		#listaResolucionesFecha = sorted(listaResoluciones, key=attrgetter('fecha'), reverse=True)
		

		#if len(listaResolucionesFecha) > 0:
		if permiso.fechaVencimiento != None:
			#ultimoVencimientoResolucion = listaResolucionesFecha[0].fecha
			ultimoVencimientoResolucion = permiso.fechaVencimiento
			fechaCorrecta = fechaResolucion >= ultimoVencimientoResolucion
		else:
			vencimientoPublicacion = permiso.estado().vencimientoPublicacion()
			fechaCorrecta = fechaResolucion > vencimientoPublicacion
		
		fechaCorrecta = fechaCorrecta and (fechaVencimiento >= fechaResolucion) and (fechaResolucion <= date.today())
		
		messages = []
		messages = ['La Fecha de Resolucion debe ser mayor a la fecha de vencimiento de publicacion, y menor o igual a la fecha actual',
		'La Fecha de Resolucion debe ser mayor o igual a la Fecha de Vencimiento de la Ultima Resolución cargada (si la hubiera)',
		'La Fecha de Vencimiento debe ser mayor o igual a la Fecha de la Resolución',
		'La Unidad mayor a CERO']
		
		if form.is_valid():
			if fechaCorrecta and (unidad > 0):
				resolucion = form.save(commit=False)
				resolucion.tipo = TipoDocumento.get_protegido('resolucion')
				resolucion.visado = True
				try:
					permiso.hacer('resolver',request.user,resolucion.fecha, unidad, resolucion, fechaPrimerCobro, fechaVencimiento)
					resolucion.save()
					return HttpResponseRedirect(self.get_success_url())
				except:
					return self.render_to_response(self.get_context_data(form=form, message_modulo='Cargue el valor de modulo ' + permiso.tipo.getTipoModuloString()+ ' para la fecha de la resolucion ' + form.data['fecha']))
			elif (unidad <= 0) or fechaCorrecta:
				return self.render_to_response(self.get_context_data(form=form, 
					messages = messages))
			else:
				return self.render_to_response(self.get_context_data(form=form, messages=messages))
		return self.render_to_response(self.get_context_data(form=form))


class AgregarOposicion(CreateView):
	model = Documento
	form_class = DocumentoProtegidoForm
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
			oposicion = form.save()
			oposicion.tipo = TipoDocumento.get_protegido('oposicion')
			oposicion.visado = True
			permiso.hacer('darDeBaja',request.user,date.today(), oposicion)
			return HttpResponseRedirect(self.get_success_url())

		return self.render_to_response(self.get_context_data(form=form))

class AltaActaDeInfraccion(CreateView):
	model = Documento
	form_class = DocumentoActaInspeccionProtegidoForm
	template_name = 'Acta/actaInspeccion.html'
	success_url = reverse_lazy('comisiones:listar')

	def get_context_data(self, **kwargs):
		context = super(AltaActaDeInfraccion, self).get_context_data(**kwargs)
		context['botones'] = {
			'Listado Comisiones': reverse('comisiones:listar'),
			'Volver al permiso': reverse('permisos:detalle', args=[self.permiso_pk])
			}
		context['nombreForm'] = 'Nueva Acta de Infraccion'
		return context

	def get (self, request, *args, **kwargs):
		self.permiso_pk = kwargs.get('pk')
		return super(AltaActaDeInfraccion, self).get(request,*args,**kwargs)

	def post(self, request, *args, **kwargs):
		self.object = self.get_object
		self.permiso_pk = kwargs.get('pk')
		form = self.form_class(request.POST, request.FILES)
		permiso = Permiso.objects.get(pk=self.permiso_pk)

		comision_pk = (int(form.data['comision']))
		comision = Comision.objects.get(pk=comision_pk)
		fechaSolicitud = permiso.fechaSolicitud
		fechaSolicitudString = fechaSolicitud.strftime("%d-%m-%Y")
		fechaActa = datetime.strptime(form.data['fecha'], "%Y-%m-%d").date()
		fechaCorrecta = ( fechaActa >= fechaSolicitud) and (fechaActa <= date.today()) and (fechaActa >= comision.fechaInicio) and (fechaActa <= comision.fechaFin)

		if form.is_valid() and fechaCorrecta:
			documento = form.save(commit=False)
			documento.tipo = TipoDocumento.get_protegido('acta-de-infraccion')
			documento.visado = True
			documento = form.save()
			permiso.agregar_documentacion(documento)
			comision.agregar_documentacion(documento)
			return HttpResponseRedirect(reverse('solicitudes:detalle', args=[permiso.id]))
		messages = []
		messages = ['La fecha del acta de infraccion debe ser:', 'Igual o mayor a la fecha de solicitud (' + fechaSolicitudString + ')',
		'Estar entre las fechas de la comision','Menor o igual a la fecha actual']
		return self.render_to_response(self.get_context_data(form=form, messages=messages))

class AltaActaDeInspeccion(CreateView):
	model = Documento
	form_class = DocumentoActaInspeccionProtegidoForm
	template_name = 'Acta/actaInspeccion.html'
	success_url = reverse_lazy('comisiones:listar')

	def get (self, request, *args, **kwargs):
		self.permiso_pk = kwargs.get('pk')
		return super(AltaActaDeInspeccion, self).get(request,*args,**kwargs)

	def get_context_data(self, **kwargs):
		context = super(AltaActaDeInspeccion, self).get_context_data(**kwargs)
		context['botones'] = {
			'Nueva comisión': reverse('comisiones:alta'),
			'Listado Comisiones': reverse('comisiones:listar'),
			'Volver al permiso': reverse('permisos:detalle', args=[self.permiso_pk])
			}
		context['nombreForm'] = 'Nueva Acta de Inspección'
		return context

	def post(self, request, *args, **kwargs):
		self.object = self.get_object
		self.permiso_pk = kwargs.get('pk')
		form = self.form_class(request.POST, request.FILES)
		permiso = Permiso.objects.get(pk=self.permiso_pk)

		comision_pk = (int(form.data['comision']))
		comision = Comision.objects.get(pk=comision_pk)

		fechaSolicitud = permiso.fechaSolicitud
		fechaSolicitudString = fechaSolicitud.strftime("%d-%m-%Y")
		fechaActa = datetime.strptime(form.data['fecha'], "%Y-%m-%d").date()
		fechaCorrecta = ( fechaActa >= fechaSolicitud) and (fechaActa <= date.today()) and (fechaActa >= comision.fechaInicio) and (fechaActa <= comision.fechaFin)


		if form.is_valid() and fechaCorrecta:
			documento = form.save(commit=False)
			documento.tipo = TipoDocumento.get_protegido('acta-de-inspeccion')
			documento.visado = True
			documento = form.save()
			permiso.agregar_documentacion(documento)
			comision.agregar_documentacion(documento)
			return HttpResponseRedirect(reverse('solicitudes:detalle', args=[permiso.id]))
		messages = []
		messages = ['La fecha del acta de Inspección debe ser:', 'Igual o mayor a la fecha de solicitud (' + fechaSolicitudString + ')',
		'Estar entre las fechas de la comision','Menor o igual a la fecha actual']
		return self.render_to_response(self.get_context_data(form=form, messages=messages))