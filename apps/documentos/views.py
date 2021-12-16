import sys
from django.shortcuts import render,redirect
from django.urls import reverse_lazy, reverse
from .models import TipoDocumento, Documento
from apps.permisos.models import TipoUso
from .forms import TipoDocumentoForm, DocumentoForm, ModificarDocumentoForm, DocumentoProtegidoForm, OposicionForm, DocumentoActaInspeccionProtegidoForm
from django.views.generic import ListView,CreateView,DeleteView,DetailView, UpdateView
from apps.permisos.models import Permiso
from apps.comisiones.models import Comision
from django.http import HttpResponseRedirect, JsonResponse
from datetime import date, datetime
from operator import attrgetter
from apps.generales.views import GenericAltaView, GenericListadoView, GenericEliminarView,GenericModificacionView,GenericDetalleView
from .tables import TipoDocumentosTable
from .filters import TipoDocumentosFilter
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.contrib import messages as Messages
import decimal

class AltaTipoDocumento(GenericAltaView):
	model = TipoDocumento
	form_class = TipoDocumentoForm
	template_name = 'documentos/alta.html'
	success_url = reverse_lazy('tipoDocumentos:listado')
	cargar_otro_url = reverse_lazy('tipoDocumentos:alta')
	permission_required = 'documentos.cargar_tipo_documento'
	redirect_url = 'tipoDocumentos:listado'

	def get_context_data(self, **kwargs):
		context = super(AltaTipoDocumento, self).get_context_data(**kwargs)
		context['nombreForm'] = "Alta Tipo de Documento"
		context['return_label'] = 'Listado de Tipo de Documentos'
		context['ayuda'] = 'permiso_gestion.html#como-crear-un-nuevo-tipo-de-documento'
		return context

	def post(self, request):
		tipo_doc_form = self.form_class(request.POST)
		if tipo_doc_form.is_valid():
			nombre = tipo_doc_form.cleaned_data['nombre']
			if not len(TipoDocumento.objects.filter(nombre=nombre))>0:
				tipo_doc_form.save()
				return redirect('tipoDocumentos:listado')
			return render(request, self.template_name, {'form':tipo_doc_form, 'message_error': ["El nombre del Tipo Documento ya existe"]})
		return render(request, self.template_name, {'form':tipo_doc_form, 'message_error': tipo_doc_form.non_field_errors()})


class ListadoTipoDocumentos(GenericListadoView):
	model = TipoDocumento
	template_name = 'documentos/listado.html'
	table_class = TipoDocumentosTable
	paginate_by = 20
	filterset_class = TipoDocumentosFilter
	context_object_name = 'tipoDocumentos'
	permission_required = 'documentos.listar_tipo_documento'
	redirect_url = '/'

	def get_context_data(self, **kwargs):
		context = super(ListadoTipoDocumentos, self).get_context_data(**kwargs)
		context['nombreListado'] = "Listado Tipo de Documento"
		context['url_nuevo'] = reverse('tipoDocumentos:listado')
		return context

class ModificarTipoDocumento(GenericModificacionView):
	model = TipoDocumento
	form_class = TipoDocumentoForm
	template_name = 'documentos/alta.html'
	success_url = reverse_lazy('tipoDocumentos:listado')
	permission_required = 'documentos.modificar_tipo_documento'
	redirect_url = 'tipoDocumentos:listado'

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
		context['return_label'] = 'Listado de Tipo de Documentos'
		context['return_path'] = reverse_lazy('tipoDocumentos:listado')
		return context


class DeleteTipoDocumento(GenericEliminarView):
	model = TipoDocumento
	permission_required = 'documentos.eliminar_tipo_documento'
	redirect_url = 'tipoDocumentos:listado'
	
	def post(self, request, *args, **kwargs):
		if request.user.has_perm(self.permission_required):
			self.object = self.get_object()
			tipos_de_usos = TipoUso.objects.filter(documentos__in=[self.object.pk])
			if len(tipos_de_usos)>0: 
				return JsonResponse({
				"success": False,
				"message": ('error',"Existen Tipo de Uso con este Tipo de Documento")
				})
			else:
				self.object.delete()
				return JsonResponse({
					"success": True,
					"message": "Tipo de Documento eliminado con exito"
				})
		else:
			return JsonResponse({
					"success": False,
					"message": ('permiso','No posee los permisos necesarios para realizar para realizar esta operación')
			})

# Documentos
class AltaDocumento(LoginRequiredMixin, CreateView):
	model = Documento
	form_class = DocumentoForm
	template_name = 'documentos/alta.html'
	permission_required = 'documentos.cargar_documento'

	def get_context_data(self, *args, **kwargs):
		context = super(AltaDocumento, self).get_context_data(**kwargs)
		context['nombreForm'] = 'Nuevo Documento'
		context['return_label'] = 'Detalle de Permiso'
		context['return_path'] = reverse('permisos:detalle', args=[self.permiso_pk])
		context['form'].fields['tipo'].queryset = Permiso.objects.get(pk=self.permiso_pk).tipos_de_documentos_faltantes()
		return context
	
	def get (self, request, *args, **kwargs):
		self.permiso_pk = kwargs.get('pk')
		if not request.user.has_perm(self.permission_required):
			Messages.error(self.request, 'No posee los permisos necesarios para realizar esta operación')
			return HttpResponseRedirect(reverse('permisos:detalle', args=[self.permiso_pk]))
		return super(AltaDocumento, self).get(request,*args,**kwargs)

	def post(self, request, *args, **kwargs):
		self.object = self.get_object
		self.permiso_pk = kwargs.get('pk')
		if not request.user.has_perm(self.permission_required):
			Messages.error(self.request, 'No posee los permisos necesarios para realizar esta operación')
			return HttpResponseRedirect(reverse('permisos:detalle', args=[self.permiso_pk]))
		form = self.form_class(request.POST, request.FILES)
		permiso = Permiso.objects.get(pk=kwargs.get('pk'))
		
		messages = ['La fecha del documento presentado debe ser igual o mayor que la fecha de la solicitud de permiso (' + permiso.fechaSolicitud.strftime("%d/%m/%Y")+')']
		if form.is_valid() :
			if (permiso.fechaSolicitud <= form.cleaned_data['fecha']):
				documento = form.save()
				permiso.agregar_documentacion(documento)
				return HttpResponseRedirect(reverse('permisos:detalle', args=[permiso.id]))
			return self.render_to_response(self.get_context_data(form=form, message_error=messages))
		return self.render_to_response(self.get_context_data(form=form, message_error=messages))

class DetalleDocumento(GenericDetalleView):
	model = Documento
	template_name = 'Documento/detalle.html'
	permission_required = 'documentos.detalle_documento'
	redirect_url = '/'

	
class ModificarDocumento(LoginRequiredMixin,UpdateView):
	model = Documento
	template_name = 'documentos/modificar.html'
	permission_required = 'documentos.modificar_documento'
	redirect_url = 'permisos:listar'
	
	def get_context_modificar(self, context, pk):
		context['nombreForm'] = 'Modificar Documento'
		context['return_label'] = 'Documentación de Permiso'
		context['return_path'] = reverse('permisos:listarDocumentacionPermiso', args=[pk])

		if (self.object.tipo.protegido == True):
			context['form'].fields['tipo'].queryset = [self.object.tipo]
		else:
			documentacion_faltante = Permiso.objects.get(pk=pk).tipos_de_documentos_faltantes()
			context['form'].fields['tipo'].queryset = documentacion_faltante.union([self.object.tipo])

		context['form'].fields['tipo'].disabled = True

		return context

	def get_context_data(self, *args, **kwargs):
		context = super(ModificarDocumento, self).get_context_data(**kwargs)
		return self.get_context_modificar(context, self.permiso_pk)

	def get (self, request, *args, **kwargs):
		self.object = self.get_object()
		self.permiso_pk = kwargs.get('pkp')
		if not request.user.has_perm(self.permission_required):
			Messages.error(self.request, 'No posee los permisos necesarios para realizar esta operación')
			return HttpResponseRedirect(reverse('permisos:listarDocumentacionPermiso', args=[self.permiso_pk]))
		if (self.object.tipo.protegido == True or self.object.estado == 2):
			self.form_class = DocumentoForm
		else:
			self.form_class = ModificarDocumentoForm
		return super(ModificarDocumento, self).get(request,*args,**kwargs)

	def post(self, request, *args, **kwargs):
		self.object = self.get_object()
		permiso = Permiso.objects.get(pk=kwargs.get('pkp'))

		if not request.user.has_perm(self.permission_required):
			Messages.error(self.request, 'No posee los permisos necesarios para realizar esta operación')
			return HttpResponseRedirect(reverse('permisos:listarDocumentacionPermiso', args=[permiso.pk]))

		try:
			es_documento_nuevo=request.POST['documento_nuevo']
			es_documento_nuevo = eval(es_documento_nuevo)
			form = ModificarDocumentoForm(request.POST, instance=self.object)	
		except:
			form = DocumentoForm(request.POST, instance=self.object)
			es_documento_nuevo = False

		if form.is_valid():
			documento = form.save()
			if not documento.tipo.protegido:
				documento.verificar_transicion_estado(es_documento_nuevo)
				permiso.estado.verificar_transicion_estado(request.user,documento.fecha,es_documento_nuevo)
			return HttpResponseRedirect(reverse('permisos:listarDocumentacionPermiso', args=[kwargs.get('pkp')]))
		else:
			messages = ['Error en la carga del formulario']
			return render(request, self.template_name, self.get_context_modificar({'form':form,'message_error':[messages]}, permiso.pk))
			#return self.render_to_response(self.get_context_data(form=form, message_error=messages))
			

class DeleteDocumento(LoginRequiredMixin,DeleteView):
	model = Documento
	permission_required = 'documentos.eliminar_documento'
	
	def get_success_url(self, **kwargs):
		return reverse('permisos:listarDocumentacionPermiso', kwargs.get('pkp'))

	def post(self, request, *args, **kwargs):
		if request.user.has_perm(self.permission_required):
			permiso = Permiso.objects.get(pk=kwargs.get('pkp'))
			documento = Documento.objects.get(pk=kwargs.get('pk'))
			if documento.tipo.slug in permiso.estado.documentos_modificar_eliminar():
				#documento.delete()
				mensaje = permiso.hacer('eliminar_documento',request.user, datetime.now(), documento)
				return JsonResponse({
					"success": mensaje[0],
					"message": mensaje[1]
				})
			return JsonResponse({
					"success": False,
					"message": ('error','Este documento no se puede eliminar')
			})
		else:
			return JsonResponse({
					"success": False,
					"message": ('permiso','No posee los permisos necesarios para realizar esta operación')
			})

class AgregarExpediente(LoginRequiredMixin, CreateView):
	model = Documento
	form_class = DocumentoProtegidoForm
	template_name = 'documentos/expediente.html'
	permission_required = 'documentos.cargar_expediente'

	def get_success_url(self):
		return reverse('permisos:detalle', args=(self.permiso_pk, ))

	def get_context_data(self, *args, **kwargs):
		context = super(AgregarExpediente, self).get_context_data(**kwargs)
		context['nombreForm'] = 'Agregar Expediente a Permiso'
		context['form'].fields['fecha'].label = 'Fecha de Creación'
		context['form'].fields['archivo'].label = 'Archivo de Caratula/Pase del Expediente'
		context['return_path'] = reverse('permisos:detalle', args=[self.permiso_pk])
		context['ayuda'] = 'solicitud.html#agregar-expediente'
		return context

	def get (self, request, *args, **kwargs):
		self.permiso_pk = kwargs.get('pk')
		if not request.user.has_perm(self.permission_required):
			Messages.error(self.request, 'No posee los permisos necesarios para realizar esta operación')
			return HttpResponseRedirect(reverse('permisos:detalle', args=[self.permiso_pk]))
		return super(AgregarExpediente, self).get(request,*args,**kwargs)

	def post(self, request, *args, **kwargs):
		self.object = self.get_object
		self.permiso_pk = kwargs.get('pk')
		if not request.user.has_perm(self.permission_required):
			Messages.error(self.request, 'No posee los permisos necesarios para realizar esta operación')
			return HttpResponseRedirect(reverse('permisos:detalle', args=[self.permiso_pk]))
		form = self.form_class(request.POST, request.FILES)
		permiso = Permiso.objects.get(pk=self.permiso_pk)
		
		fechaExpediente=datetime.strptime(form.data['fecha'], "%Y-%m-%d").date()
		#Refactorizar a una funcion de modelo
		lista_fechas = [documento.fecha for documento in permiso.documentos.filter(tipo__protegido=False) if documento.fecha > fechaExpediente]
		if len(lista_fechas) != 0:
			lista_fechas.sort()
			ultima_fecha = lista_fechas.pop()
		
		numero = request.POST['expediente']
		fecha_string = "{}/{}-IPA".format(numero,fechaExpediente.year)
		if form.is_valid(): #AGREGAR CONDICION DE QUE LA DOCUMENTACION NO ESTE DUPLICADO
			if len(lista_fechas) == 0:
				documento = form.save()
				documento.tipo = TipoDocumento.get_protegido('pase')
				documento.estado = 2
				documento.save()
				try:
					permiso.hacer('completar',request.user,fechaExpediente, fecha_string, documento)
					return HttpResponseRedirect(self.get_success_url())
				except Exception as e:
					return self.render_to_response(self.get_context_data(form=form,expediente=numero, 
					message_error = [str(e)]))
			else:
				return self.render_to_response(self.get_context_data(form=form, expediente=numero,
					message_error = ['La fecha de Expediente debe ser posterior a la fecha de la ultima documentación presentada ('+(ultima_fecha).strftime("%d-%m-%Y")+')']))
		return self.render_to_response(self.get_context_data(form=form,expediente=numero))

class AgregarEdicto(LoginRequiredMixin, CreateView):
	model = Documento
	form_class = DocumentoProtegidoForm
	template_name = 'documentos/edicto.html'
	permission_required = 'documentos.cargar_edicto'
		
	def get_success_url(self):
		return reverse('permisos:detalle', args=[self.permiso_pk])

	def get_context_data(self, *args, **kwargs):
		context = super(AgregarEdicto, self).get_context_data(**kwargs)
		context['nombreForm'] = 'Agregar Edicto a Permiso'
		context['form'].fields['archivo'].label = 'Archivo del Edicto que se publica'
		context['return_path'] = reverse('permisos:detalle', args=[self.permiso_pk])
		context['ayuda'] = 'solicitud.html#agregar-edicto'
		return context

	def get (self, request, *args, **kwargs):
		self.permiso_pk = kwargs.get('pk')
		if not request.user.has_perm(self.permission_required):
			Messages.error(self.request, 'No posee los permisos necesarios para realizar esta operación')
			return HttpResponseRedirect(reverse('permisos:detalle', args=[self.permiso_pk]))
		return super(AgregarEdicto, self).get(request,*args,**kwargs)

	def post(self, request, *args, **kwargs):
		self.object = self.get_object
		self.permiso_pk = kwargs.get('pk')
		if not request.user.has_perm(self.permission_required):
			Messages.error(self.request, 'No posee los permisos necesarios para realizar esta operación')
			return HttpResponseRedirect(reverse('permisos:detalle', args=[self.permiso_pk]))
		form = self.form_class(request.POST, request.FILES)
		permiso = Permiso.objects.get(pk=self.permiso_pk)
		documentos = permiso.documentos.all()
		pase = [documento for documento in documentos if (documento.tipo.slug == 'pase')] #FIXME: VA TIPO DEFINIDO PARA PASE
		
		fecha_pase = pase[0].fecha

		fechaEdicto=datetime.strptime(form.data['fecha'], "%Y-%m-%d").date()

		tiempo = int(form.data['tiempo'])

		if form.is_valid():
			if (fechaEdicto >= fecha_pase) and (tiempo > 0):
				edicto = form.save(commit=False)
				edicto.tipo = TipoDocumento.get_protegido('edicto')
				edicto.estado = 2
				edicto.save()
				permiso.hacer('publicar',request.user,edicto.fecha, tiempo, edicto)
				return HttpResponseRedirect(self.get_success_url())
			else:
				return self.render_to_response(self.get_context_data(form=form, 
					message_error = ['La fecha del Edicto debe igual o posterior a la fecha del Expediente ('+(fecha_pase).strftime("%d-%m-%Y")+
					') y el tiempo de publicación mayor a CERO']))
		return self.render_to_response(self.get_context_data(form=form))

class AgregarResolucion(LoginRequiredMixin, CreateView):
	model = Documento
	form_class = DocumentoProtegidoForm
	template_name = 'documentos/resolucion.html'
	permission_required = 'documentos.cargar_resolucion'

	def get_success_url(self):
		return reverse('permisos:detalle', args=(self.permiso_pk, ))

	def get_context_data(self, *args, **kwargs):
		context = super(AgregarResolucion, self).get_context_data(**kwargs)
		permiso = Permiso.objects.get(pk=self.permiso_pk)
		context['permiso'] = permiso
		context['utilizando'] = 'Si' if permiso.getEstados(1)[0].utilizando else 'No'
		context['renovacion'] = True if permiso.fechaVencimiento != None else False
		context['unidadAnterior'] = '- Unidad de la anterior Resolución: ' + str(permiso.unidad) + permiso.tipo.get_medida_display() if permiso.unidad != None else ''
		context['nombreForm'] = '{} Resolución a Permiso'.format('Renovar' if context['renovacion'] else 'Agregar')
		context['form'].fields['fecha'].label = 'Fecha de aprobación de la Resolución'
		context['return_path'] = reverse('permisos:detalle', args=[self.permiso_pk])
		context['ayuda'] = 'solicitud.html#agregar-resolucion'
		return context

	def get (self, request, *args, **kwargs):
		self.permiso_pk = kwargs.get('pk')
		if not request.user.has_perm(self.permission_required):
			Messages.error(self.request, 'No posee los permisos necesarios para realizar esta operación')
			return HttpResponseRedirect(reverse('permisos:detalle', args=[self.permiso_pk]))
		return super(AgregarResolucion, self).get(request,*args,**kwargs)

	def validacion_resolucion_form(self,request,form):
		campos_correctos = True
		try:
			self.fechaPrimerCobro = datetime.strptime(form.data['fechaPrimerCobro'], "%Y-%m-%d").date()
		except:
			campos_correctos = False
			self.messages_error.append("La Fecha a partir de la cual se comienza a calcular el primer Cobro es incorrecta")
		try:
			self.fechaVencimiento = datetime.strptime(form.data['fechaVencimiento'], "%Y-%m-%d").date()
		except:
			campos_correctos = False
			self.messages_error.append("Fecha de Vencimiento del Permiso es incorrecta")
		try:
			self.unidad = decimal.Decimal(request.POST['unidad'])
		except:
			campos_correctos = False
			self.messages_error.append("La Unidad ingresada es incorrecta")
		return campos_correctos

	
	def post(self, request, *args, **kwargs):
		self.object = self.get_object
		self.permiso_pk = kwargs.get('pk')
		self.messages_error = []
		if not request.user.has_perm(self.permission_required):
			Messages.error(self.request, 'No posee los permisos necesarios para realizar esta operación')
			return HttpResponseRedirect(reverse('permisos:detalle', args=[self.permiso_pk]))
		form = self.form_class(request.POST, request.FILES)

		if form.is_valid() and self.validacion_resolucion_form(request,form):

			permiso = Permiso.objects.get(pk=self.permiso_pk)

			fechaResolucion=form.cleaned_data['fecha']

			try:
				fechaPrimerCobro=datetime.strptime(form.data['fechaPrimerCobro'], "%Y-%m-%d").date()
				vencimientoPublicacion = permiso.estado.vencimientoPublicacion()
			except:
				fechaPrimerCobro = None

			fechaVencimiento=datetime.strptime(form.data['fechaVencimiento'], "%Y-%m-%d").date()
			
			unidad = decimal.Decimal(request.POST['unidad'])

			messages_error = ['La Fecha de Vencimiento debe ser mayor a la Fecha de la Resolución', 'La Unidad mayor a CERO']
			
			if permiso.fechaVencimiento != None:
				ultimoVencimientoResolucion = permiso.fechaVencimiento
				fechaCorrecta = fechaResolucion >= ultimoVencimientoResolucion
				accion = 'renovar'
				messages_error.append('La Fecha de Resolución debe ser mayor o igual a la Fecha de Vencimiento de la Ultima Resolución cargada (' + ultimoVencimientoResolucion.strftime('%d/%m/%Y') + ') y menor o igual a la fecha actual.')
			else:
				fechaCorrecta = fechaResolucion > vencimientoPublicacion
				accion = 'resolver'
				messages_error.append('La Fecha de Resolución debe ser mayor a la fecha de vencimiento de publicacion (' + vencimientoPublicacion.strftime('%d/%m/%Y') + ') y menor o igual a la fecha actual.')
				messages_error.append('La Fecha de Resolución debe ser mayor a la fecha de primero cobro que ingreso (' + fechaPrimerCobro.strftime('%d/%m/%Y') + ') y menor o igual a la fecha actual.')

			fechaCorrecta = fechaCorrecta and (fechaVencimiento >= fechaResolucion) and (fechaResolucion <= date.today() and (fechaResolucion > fechaPrimerCobro))
		
			if fechaCorrecta and (unidad > 0):
				resolucion = form.save(commit=False)
				resolucion.tipo = TipoDocumento.get_protegido('resolucion')
				resolucion.estado = 2
				try:
					permiso.hacer(accion,request.user,resolucion.fecha, unidad, resolucion, fechaPrimerCobro, fechaVencimiento)
					return HttpResponseRedirect(self.get_success_url())
				except Exception as e:
					print("Unexpected error:", sys.exc_info()[0])
					return self.render_to_response(self.get_context_data(form=form, message_error=[e,'Cargue el valor de módulo ' + permiso.tipo.getTipoModuloString()+ ' para la fecha de la resolución (' + fechaResolucion.strftime('%d/%m/%Y')+')']))
			elif (unidad <= 0) or fechaCorrecta:
				return self.render_to_response(self.get_context_data(form=form, message_error = messages_error,fechaPrimerCobro=form.data['fechaPrimerCobro'], fechaVencimiento=form.data['fechaVencimiento'], unidad=request.POST['unidad']))
			else:
				return self.render_to_response(self.get_context_data(form=form, message_error=messages_error,fechaPrimerCobro=form.data['fechaPrimerCobro'], fechaVencimiento=form.data['fechaVencimiento'], unidad=request.POST['unidad']))
		return self.render_to_response(self.get_context_data(form=form,message_error = self.messages_error,
		fechaPrimerCobro=form.data['fechaPrimerCobro'], fechaVencimiento=form.data['fechaVencimiento'], unidad=request.POST['unidad']))


class AgregarOposicion(LoginRequiredMixin, CreateView):
	model = Documento
	form_class = DocumentoProtegidoForm
	template_name = 'documentos/alta.html'
	permission_required = 'documentos.cargar_oposicion'

	def get_success_url(self):
		return reverse('permisos:detalle', args=[self.permiso_pk])

	def get_context_data(self, *args, **kwargs):
		context = super(AgregarOposicion, self).get_context_data(**kwargs)
		context['nombreForm'] = 'Agregar Oposición a Permiso'
		context['return_label'] = 'Detalle de Permiso'
		context['return_path'] = reverse('permisos:detalle', args=[self.permiso_pk])
		context['form'].fields['archivo'].label = 'Archivo de la oposición'
		context['form2'] = OposicionForm()
		context['ayuda'] = 'solicitud.html#agregar-oposicion'
		return context


	def get (self, request, *args, **kwargs):
		self.permiso_pk = kwargs.get('pk')
		if not request.user.has_perm(self.permission_required):
			Messages.error(self.request, 'No posee los permisos necesarios para realizar esta operación')
			return HttpResponseRedirect(reverse('permisos:detalle', args=[self.permiso_pk]))
		return super(AgregarOposicion, self).get(request,*args,**kwargs)

	def post(self, request, *args, **kwargs):
		self.object = self.get_object
		self.permiso_pk = kwargs.get('pk')
		if not request.user.has_perm(self.permission_required):
			Messages.error(self.request, 'No posee los permisos necesarios para realizar esta operación')
			return HttpResponseRedirect(reverse('permisos:detalle', args=[self.permiso_pk]))
		form = self.form_class(request.POST, request.FILES)
		second_form = OposicionForm(request.POST)

		
		if form.is_valid():
			fecha_oposicion = form.cleaned_data['fecha']

			valido = eval(second_form.data['valido'])
		
			permiso = Permiso.objects.get(pk=kwargs.get('pk'))
			fechaVencimiento = permiso.estado.vencimientoPublicacion()
			
			if (fecha_oposicion>=permiso.estado.fecha and fecha_oposicion <= fechaVencimiento):
			#if form.is_valid() and (request.POST['fecha'] <= fechaVencimiento.strftime('%d/%m/%Y')):
				oposicion = form.save(commit=False)
				oposicion.tipo = TipoDocumento.get_protegido('oposicion')
				oposicion.estado = 2
				permiso.hacer('darDeBaja',request.user,fecha_oposicion, oposicion, valido)
				return HttpResponseRedirect(self.get_success_url())
			
			return self.render_to_response(self.get_context_data(form=form, message_error = ['La fecha debe ser menor o igual a la fecha de vencimiento de publicacion ('+(fechaVencimiento).strftime("%d-%m-%Y") +
			') y mayor o igual a la fecha de publicacion ('+permiso.estado.fecha.strftime("%d-%m-%Y")+")"]))
		
		return self.render_to_response(self.get_context_data(form=form))

class BajaPermiso(LoginRequiredMixin, CreateView):
	model = Documento
	form_class = DocumentoProtegidoForm
	template_name = 'documentos/alta.html'
	permission_required = 'documentos.baja_permiso'

	def get_success_url(self):
		return reverse('permisos:detalle', args=[self.permiso_pk])

	def get_context_data(self, *args, **kwargs):
		context = super(BajaPermiso, self).get_context_data(**kwargs)
		context['nombreForm'] = 'Trámite de Baja del Permiso'
		context['return_label'] = 'Detalle de Permiso'
		context['return_path'] = reverse('permisos:detalle', args=[self.permiso_pk])
		context['form'].fields['archivo'].label = 'Archivo del documento de baja'
		context['form'].fields['fecha'].label = 'Fecha de la Resolución que adjunta'
		return context

	def get (self, request, *args, **kwargs):
		self.permiso_pk = kwargs.get('pk')
		if not request.user.has_perm(self.permission_required):
			Messages.error(self.request, 'No posee los permisos necesarios para realizar esta operación')
			return HttpResponseRedirect(reverse('permisos:detalle', args=[self.permiso_pk]))
		return super(BajaPermiso, self).get(request,*args,**kwargs)

	def post(self, request, *args, **kwargs):
		self.object = self.get_object
		self.permiso_pk = kwargs.get('pk')
		if not request.user.has_perm(self.permission_required):
			Messages.error(self.request, 'No posee los permisos necesarios para realizar esta operación')
			return HttpResponseRedirect(reverse('permisos:detalle', args=[self.permiso_pk]))
		form = self.form_class(request.POST, request.FILES)

		if form.is_valid():
			fecha_de_baja = datetime.strptime(form.data['fecha'], "%Y-%m-%d").date()
		
			permiso = Permiso.objects.get(pk=kwargs.get('pk'))
			if (fecha_de_baja >= permiso.estado.fecha):
				resolucion = form.save(commit=False)
				resolucion.tipo = TipoDocumento.get_protegido('resolucion')
				resolucion.estado = 2
				permiso.hacer('darDeBaja',request.user,fecha_de_baja, resolucion, True)
				return HttpResponseRedirect(self.get_success_url())
			return self.render_to_response(self.get_context_data(form=form, message_error = ['La fecha debe ser mayor o igual a '+(permiso.estado.fecha).strftime("%d-%m-%Y")+' (Permiso '+permiso.estado.getEstadoString().title()+')']))
		return self.render_to_response(self.get_context_data(form=form))

class ArchivarPermiso(LoginRequiredMixin, CreateView):
	model = Documento
	form_class = DocumentoProtegidoForm
	template_name = 'documentos/alta.html'
	permission_required = 'documentos.archivar_permiso'

	def get_success_url(self):
		return reverse('permisos:detalle', args=[self.permiso_pk])

	def get_context_archivar(self, context, pk):
		context['nombreForm'] = 'Trámite para Archivar el Permiso'
		context['return_label'] = 'Detalle de Permiso'
		context['return_path'] = reverse('permisos:detalle', args=[pk])
		context['form'].fields['archivo'].label = 'Documento de para archivar expediente de permiso'
		context['form'].fields['fecha'].label = 'Fecha del documento que adjunta'
		return context

	def get_context_data(self, *args, **kwargs):
		context = super(ArchivarPermiso, self).get_context_data(**kwargs)
		return self.get_context_archivar(context, self.permiso_pk)

	def get (self, request, *args, **kwargs):
		self.permiso_pk = kwargs.get('pk')
		if not request.user.has_perm(self.permission_required):
			Messages.error(self.request, 'No posee los permisos necesarios para realizar esta operación')
			return HttpResponseRedirect(reverse('permisos:detalle', args=[self.permiso_pk]))
		return super(ArchivarPermiso, self).get(request,*args,**kwargs)

	def post(self, request, *args, **kwargs):
		self.object = self.get_object
		self.permiso_pk = kwargs.get('pk')
		if not request.user.has_perm(self.permission_required):
			Messages.error(self.request, 'No posee los permisos necesarios para realizar esta operación')
			return HttpResponseRedirect(reverse('permisos:detalle', args=[self.permiso_pk]))
		form = self.form_class(request.POST, request.FILES)

		if form.is_valid():
			fecha_de_archivo = form.cleaned_data['fecha']
			permiso = Permiso.objects.get(pk=kwargs.get('pk'))
			documento = form.save(commit=False)
			documento.tipo = TipoDocumento.get_protegido('pase')
			documento.estado = 2
			try: 
				permiso.hacer('archivar',request.user,fecha_de_archivo, documento)
				return HttpResponseRedirect(self.get_success_url())
			except Exception as e:
				return render(request, self.template_name, self.get_context_archivar({'form':form,'message_error':[e]}, self.permiso_pk))
		return self.render_to_response(self.get_context_data(form=form))

class AltaActaDeInfraccion(LoginRequiredMixin, CreateView):
	model = Documento
	form_class = DocumentoActaInspeccionProtegidoForm
	template_name = 'documentos/actas.html'
	permission_required = 'documentos.cargar_acta_infraccion'

	def get_success_url(self):
		return reverse('permisos:detalle', args=[self.permiso_pk])

	def get_context_data(self, **kwargs):
		context = super(AltaActaDeInfraccion, self).get_context_data(**kwargs)
		context['botones'] = {}
		context['nombreForm'] = 'Nueva Acta de Infraccion'
		context['form'].fields['comision'].queryset = Comision.objects.filter(Q(fechaInicio__lte=self.permiso.fechaSolicitud,fechaFin__gte=self.permiso.fechaSolicitud)|Q(fechaInicio__gte=self.permiso.fechaSolicitud))
		context['return_path'] = reverse('permisos:detalle', args=[self.permiso_pk])
		context['ayuda'] = 'comision.html#como-crear-una-nueva-infraccion'
		return context

	def get (self, request, *args, **kwargs):
		self.permiso_pk = kwargs.get('pk')
		self.permiso = Permiso.objects.get(pk=self.permiso_pk)
		if not request.user.has_perm(self.permission_required):
			Messages.error(self.request, 'No posee los permisos necesarios para realizar esta operación')
			return HttpResponseRedirect(reverse('permisos:detalle', args=[self.permiso_pk]))
		return super(AltaActaDeInfraccion, self).get(request,*args,**kwargs)

	def post(self, request, *args, **kwargs):
		self.object = self.get_object
		self.permiso_pk = kwargs.get('pk')
		if not request.user.has_perm(self.permission_required):
			Messages.error(self.request, 'No posee los permisos necesarios para realizar esta operación')
			return HttpResponseRedirect(reverse('permisos:detalle', args=[self.permiso_pk]))
		form = self.form_class(request.POST, request.FILES)
		self.permiso = Permiso.objects.get(pk=self.permiso_pk)

		if form.is_valid():
		
			comision_pk = (int(form.data['comision']))
			comision = Comision.objects.get(pk=comision_pk)
			fechaSolicitud = self.permiso.fechaSolicitud
			fechaSolicitudString = fechaSolicitud.strftime("%d-%m-%Y")
			fechaActa = datetime.strptime(form.data['fecha'], "%Y-%m-%d").date()
			fechaCorrecta = ( fechaActa >= fechaSolicitud) and (fechaActa <= date.today()) and (fechaActa >= comision.fechaInicio) and (fechaActa <= comision.fechaFin)

			if fechaCorrecta:
				documento = form.save(commit=False)
				documento.tipo = TipoDocumento.get_protegido('acta-de-infraccion')
				documento.estado = 2
				documento = form.save()	#TODO se esta guardando mal la información
				self.permiso.agregar_documentacion(documento)
				comision.agregar_documentacion(documento)
				return HttpResponseRedirect(reverse('permisos:detalle', args=[self.permiso.id]))
				
			messages = ['La fecha del acta de infraccion debe ser:', 'Igual o mayor a la fecha de solicitud (' + fechaSolicitudString + ')',
			'Estar entre las fechas de la comisión','Menor o igual a la fecha actual']
			return self.render_to_response(self.get_context_data(form=form, message_error=messages))
		
		return self.render_to_response(self.get_context_data(form=form))

class AltaActaDeInspeccion(LoginRequiredMixin, CreateView):
	model = Documento
	form_class = DocumentoActaInspeccionProtegidoForm
	template_name = 'documentos/actas.html'
	permission_required = 'documentos.cargar_acta_inspeccion'

	def get_success_url(self):
		return reverse('permisos:detalle', args=[self.permiso_pk])

	def get (self, request, *args, **kwargs):
		self.permiso_pk = kwargs.get('pk')
		self.permiso = Permiso.objects.get(pk=self.permiso_pk)
		if not request.user.has_perm(self.permission_required):
			Messages.error(self.request, 'No posee los permisos necesarios para realizar esta operación')
			return HttpResponseRedirect(reverse('permisos:detalle', args=[self.permiso_pk]))
		return super(AltaActaDeInspeccion, self).get(request,*args,**kwargs)

	def get_context_data(self, **kwargs):
		context = super(AltaActaDeInspeccion, self).get_context_data(**kwargs)
		context['botones'] = {}
		context['nombreForm'] = 'Nueva Acta de Inspección'
		context['return_path'] = reverse('permisos:detalle', args=[self.permiso_pk])
		context['form'].fields['comision'].queryset = Comision.objects.filter(Q(fechaInicio__lte=self.permiso.fechaSolicitud,fechaFin__gte=self.permiso.fechaSolicitud)|Q(fechaInicio__gte=self.permiso.fechaSolicitud))
		context['ayuda'] = 'comision.html#como-crear-una-nueva-acta-de-inspeccion'
		return context

	def post(self, request, *args, **kwargs):
		self.object = self.get_object
		self.permiso_pk = kwargs.get('pk')
		self.permiso = Permiso.objects.get(pk=self.permiso_pk)

		if not request.user.has_perm(self.permission_required):
			Messages.error(self.request, 'No posee los permisos necesarios para realizar esta operación')
			return HttpResponseRedirect(reverse('permisos:detalle', args=[self.permiso_pk]))
		form = self.form_class(request.POST, request.FILES)
		permiso = Permiso.objects.get(pk=self.permiso_pk)

		fechaSolicitud = permiso.fechaSolicitud
		fechaSolicitudString = fechaSolicitud.strftime("%d-%m-%Y")

		if form.is_valid():
			comision_pk = (int(form.data['comision']))
			comision = Comision.objects.get(pk=comision_pk)

			fechaActa = datetime.strptime(form.data['fecha'], "%Y-%m-%d").date()
			fechaCorrecta = ( fechaActa >= fechaSolicitud)  and (fechaActa >= comision.fechaInicio) and (fechaActa <= comision.fechaFin)

			if fechaCorrecta:
				documento = form.save(commit=False)
				documento.tipo = TipoDocumento.get_protegido('acta-de-inspeccion')
				documento.estado = 2
				documento = form.save()
				permiso.agregar_documentacion(documento)
				comision.agregar_documentacion(documento)
				return HttpResponseRedirect(reverse('permisos:detalle', args=[permiso.id]))
			
			form.fields['comision'].queryset = Comision.objects.filter(Q(fechaInicio__lte=self.permiso.fechaSolicitud,fechaFin__gte=self.permiso.fechaSolicitud)|Q(fechaInicio__gte=self.permiso.fechaSolicitud))
			messages = ['La fecha del acta de Inspección debe ser:', 'Igual o mayor a la fecha de solicitud (' + fechaSolicitudString + ')',
			'Estar entre las fechas de la comisión','Menor o igual a la fecha actual']
			return self.render_to_response(self.get_context_data(form=form, message_error=messages))
		return self.render_to_response(self.get_context_data(form=form))