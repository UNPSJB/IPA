# Create your views here.
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from .models import ValorDeModulo, Cobro, Pago
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from .forms import RegistrarValorDeModuloForm, CobroForm, PagoForm
from apps.documentos.forms import DocumentoForm, DocumentoProtegidoForm
from django.views.generic import ListView,CreateView,DeleteView,UpdateView, View
from apps.permisos.models import Permiso,Baja,Otorgado,Archivado
from datetime import date, datetime
from apps.documentos.models import TipoDocumento, Documento
from django.shortcuts import redirect
from apps.generales.views import GenericListadoView,GenericAltaView, GenericEliminarView,GenericModificacionView
from .filters import CobrosFilter,CobrosTodosFilter, ModulosFilter, PagosFilter, PagosTodosFilter
from .tables import CobrosTable, ModulosTable, CobrosTodosTable, PagosTable, PagosTodosTable
from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django_tables2.views import SingleTableMixin
from django_filters.views import FilterView
from django_tables2.export.views import ExportMixin
from django.contrib import messages as Messages
from django.contrib.auth.decorators import permission_required
from django.contrib import messages

class AltaValorDeModulo(GenericAltaView):
	model = ValorDeModulo
	form_class = RegistrarValorDeModuloForm
	template_name = 'pagos/modulos/alta.html'
	success_url = reverse_lazy('pagos:listarModulos')
	permission_required = 'pagos.cargar_valor_de_modulo'
	redirect_url = 'pagos:listarModulos'

	def get_context_data(self, **kwargs):
		context = super(AltaValorDeModulo, self).get_context_data(**kwargs)
		context['nombreForm'] = "Alta Valor de Modulo"
		context['ayuda'] = 'general.html#como-crear-un-nuevo-valor-de-modulo'
		return context

class ModificarValorDeModulo(GenericModificacionView):
	model = ValorDeModulo
	form_class = RegistrarValorDeModuloForm
	template_name = 'pagos/modulos/alta.html'
	success_url = reverse_lazy('pagos:listarModulos')
	permission_required = 'pagos.modificar_valor_de_modulo'
	redirect_url = 'pagos:listarModulos'

	def get_context_data(self, **kwargs):
		context = super(ModificarValorDeModulo, self).get_context_data(**kwargs)
		context['nombreForm'] = "Modificar Valor de Modulo"
		context['return_path'] = reverse('pagos:listarModulos')
		return context

class ListadoValoresDeModulo(GenericListadoView):
	model = ValorDeModulo
	template_name = 'pagos/modulos/listado.html'
	table_class = ModulosTable
	paginate_by = 11
	filterset_class = ModulosFilter
	export_name = 'listado_valores_modulos'
	context_object_name = 'modulos'
	permission_required = 'pagos.listar_valor_de_modulo'
	redirect_url = '/'

	def get_context_data(self, **kwargs):
		context = super(ListadoValoresDeModulo, self).get_context_data(**kwargs)
		context['nombreLista'] = "Listado de tipos de documento"
		context['url_nuevo'] = reverse('pagos:altaModulo')
		return context

class EliminarValorDeModulo(GenericEliminarView):
	model = ValorDeModulo
	permission_required = 'pagos.eliminar_valor_de_modulo'

	def post(self, request, *args, **kwargs):
		if request.user.has_perm(self.permission_required):
			self.object = self.get_object()
			try:
				self.object.delete()
				return JsonResponse({
					"success": True,
					"message": 'Valor de Módulo eliminado correctamente'
				})
			except Exception:
				return JsonResponse({
				"success": False,
				"message": ('error',"No se pudo eliminar el valor de módulo")
				})
		else:
			return JsonResponse({
					"success": False,
					"message": ('permiso','No posee los permisos necesarios para realizar esta operación')
			}) 

class AltaCobro(LoginRequiredMixin, CreateView):
	model = Cobro
	form_class = CobroForm
	template_name = 'pagos/cobros/alta.html'
	success_url = reverse_lazy('pagos:listarCobros')
	permission_required = 'pagos.cargar_cobro'

	def get(self, request, *args, **kwargs):
		permiso = Permiso.objects.get(pk=kwargs.get('pk'))
		if not request.user.has_perm(self.permission_required):
			Messages.error(self.request, 'No posee los permisos necesarios para realizar esta operación')
			return HttpResponseRedirect(reverse('pagos:listarCobros', args=[permiso.pk]))
		fecha = date.today() if date.today() <= permiso.fechaVencimiento else permiso.fechaVencimiento
		cobro = permiso.estado.recalcular(usuario=request.user, documento=None, fecha=fecha, unidad=permiso.unidad) #TODO corregir fecha, el limite es HOY y el VENC. de permiso
		return render(request, self.template_name, {'form':self.form_class(initial={'fecha_desde':cobro.fecha_desde,'fecha':cobro.fecha}), 'cobro': cobro, 
			'return_path':reverse('pagos:listarCobros', args=[permiso.id]),
			'permiso': permiso, 'nombreForm':"Nuevo Cobro de Canon"})

	def post(self, request, *args, **kwargs):
		self.object = self.get_object
		permiso = Permiso.objects.get(pk=kwargs.get('pk'))
		if not request.user.has_perm(self.permission_required):
			Messages.error(self.request, 'No posee los permisos necesarios para realizar esta operación')
			return HttpResponseRedirect(reverse('permisos:detalle', args=[permiso.pk]))
		documento_form = self.form_class(request.POST, request.FILES)

		if documento_form.is_valid():
			fecha = datetime.strptime(request.POST['fecha'], '%Y-%m-%d').date()
			descripcion = request.POST['descripcion']
			archivo = request.POST['fecha']
			documento = Documento(tipo=TipoDocumento.get_protegido('cobro'), descripcion=descripcion, archivo=archivo, estado = 2, fecha=fecha)
			documento.save()
			cobro = permiso.estado.recalcular(request.user, documento, fecha, permiso.unidad)
			cobro.save()
			permiso.agregar_documentacion(documento)
			return HttpResponseRedirect(reverse('pagos:listarCobros', args=[permiso.id]))
		return render(request, self.template_name, {'form':documento_form, 'cobro': cobro, 'permiso': permiso})


def recalcular_cobro(request):
	permiso = Permiso.objects.get(pk=request.GET['permiso_pk'])
	fecha = datetime.strptime(request.GET['fecha'], '%Y-%m-%d').date()
	if not request.user.has_perm('pagos.recalcular_cobro'):
		Messages.error(self.request, 'No posee los permisos necesarios para realizar esta operación')
		return JsonResponse({"success": False,"message": "No posee los permisos necesarios"})

	if fecha <= permiso.fechaVencimiento:
		try:
			cobro = permiso.estado.recalcular(usuario=request.user, documento=None, fecha=fecha, unidad=permiso.unidad)
			return JsonResponse({"success": True,"message": "Nuevo monto calculado con exito", "monto": cobro.monto, 
			"fecha_desde": cobro.fecha_desde.strftime("%d/%m/%Y"),"fecha":cobro.fecha.strftime("%d/%m/%Y")})
		except:
			return JsonResponse({"success": False,"message": "No se puede calcular el cobro fecha incorrectas"})
	else:
		return JsonResponse({"success": False,"message": "La fecha ingresada hasta donde se calcula el canon de agua es mayor a la fecha de vencimiento del permiso ("+permiso.fechaVencimiento.strftime("%d/%m/%Y")+")"})

class EliminarCobro(GenericEliminarView):
	model = Cobro
	permission_required = 'pagos.eliminar_cobro'

	def post(self, request, *args, **kwargs):
		self.object = self.get_object()

		if not request.user.has_perm(self.permission_required):
			return JsonResponse({"success": False,"message": ('permiso',"No posee los permisos necesarios para realizar esta operación")})

		try:
			if self.object == self.object.permiso.cobros.latest() and self.object.documento.tipo.slug != 'resolucion':
				self.object.delete()
				return JsonResponse({"success": True,"message": "Cobro eliminado"})
			else:
				return JsonResponse({"success": False,"message": ('error',"No se puede eliminar el primer cobro, o bien existen otros cobros posteriores al que desea eliminar")})
		except:
			return JsonResponse({"success": False,"message": ('error',"No se ha podido realizar la eliminación del cobro")})


class ListarCobros(ExportMixin, SingleTableMixin, LoginRequiredMixin,FilterView):
	model = Cobro
	template_name = 'pagos/cobros/listado.html'
	table_class = CobrosTable
	paginate_by = 12
	filterset_class = CobrosFilter
	export_name = 'listado_cobros'
	context_object_name = 'cobros'
	permission_required = 'pagos.listar_cobro'

	def get_table_data(self):
		return self.permiso.cobros.all()

	def get(self, request, *args, **kwargs):
		self.permiso = Permiso.objects.get(pk=kwargs.get('pk'))
		if not request.user.has_perm(self.permission_required):
			Messages.error(self.request, 'No posee los permisos necesarios para realizar esta operación')
			return HttpResponseRedirect(reverse('permisos:detalle', args=[self.permiso.pk]))
		return super(ListarCobros,self).get(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(ListarCobros, self).get_context_data(**kwargs)
		context['nombreListado'] = 'Listado de Cobros del Permiso'
		context['return_path'] = reverse('permisos:detalle', args=[self.permiso.pk])
		context['particular'] = True
		estado_otorgado = True if len(self.permiso.estados.all().filter(tipo=6))>0 else False
		if isinstance(self.permiso.estado, (Otorgado,Baja)) and estado_otorgado:
			context['url_nuevo'] = reverse('pagos:altaCobro',args=[self.permiso.pk])
		if not isinstance(self.permiso.estado, Archivado):
			context['url_nuevo2'] = reverse('pagos:altaCobroInfraccion',args=[self.permiso.pk])
		return context

class AltaPago(LoginRequiredMixin,CreateView):
	model = Pago
	form_class = DocumentoProtegidoForm
	template_name = 'pagos/alta.html'
	permission_required = 'pagos.cargar_pago'

	def get_context_data(self, **kwargs):
		context = super(AltaPago, self).get_context_data(**kwargs)
		context['nombreForm'] = 'Nuevo Pago Canon'

	def get(self, request, *args, **kwargs):
		self.permiso_pk = kwargs.get('pk')
		if not request.user.has_perm(self.permission_required):
			Messages.error(self.request, 'No posee los permisos necesarios para realizar esta operación')
			return HttpResponseRedirect(reverse('pagos:listarPagos', args=[self.permiso_pk]))
		permiso = Permiso.objects.get(pk=kwargs.get('pk'))
		documento_form = self.form_class()
		documento_form.fields['fecha'].label = 'Fecha de Pago'
		return render(request, self.template_name, {'form':documento_form, 
			'return_path':reverse('permisos:detalle', args=[permiso.id]),
			'return_label':'Volver al Detalle de Permiso',
			'permiso': permiso, 'nombreForm':"Nuevo Pago Canon"})

	def post(self, request, *args, **kwargs):
		self.object = self.get_object
		permiso = Permiso.objects.get(pk=kwargs.get('pk'))
		documento_form = self.form_class(request.POST, request.FILES)
		return post_pago_nuevo_modificado(self, request, documento_form, None, permiso)


class ModificarPago(LoginRequiredMixin,UpdateView):
	model = Pago
	form_class = DocumentoProtegidoForm
	template_name = 'pagos/alta.html'
	context_object_name = 'pago'
	success_url = reverse_lazy('pagos:listarTodosLosPagos')
	permission_required = 'pagos.modificar_pago'


	def get_context_data(self, **kwargs):
		context = super(ModificarPago, self).get_context_data(**kwargs)
		context['nombreForm'] = 'Modificar Pago de Canon'
		context['return_path'] = reverse('pagos:listarPagos',args=[self.pago.permiso.pk])
		context['return_label'] = 'Volver al listado de pagos'		
		context['form'] = self.formulario
		context['monto'] = self.pago_monto
		return context

	def get(self, request, *args, **kwargs):
			if not request.user.has_perm(self.permission_required):
				Messages.error(self.request, 'No posee los permisos necesarios para realizar esta operación')
				return HttpResponseRedirect(reverse('pagos:listarPagos', args=[kwargs.get('pkp')]))
			self.pago = self.get_object()
			self.pago_monto = self.pago.monto
			self.formulario = DocumentoProtegidoForm(initial={'descripcion': self.pago.documento.descripcion, 'archivo': self.pago.documento.archivo, 'fecha': self.pago.documento.fecha})
			return super(ModificarPago, self).get(request,*args,**kwargs)

	def post(self, request, *args, **kwargs):
		self.pago = self.get_object()
		self.object = self.get_object()
		if not request.user.has_perm(self.permission_required):
			Messages.error(self.request, 'No posee los permisos necesarios para realizar esta operación')
			return HttpResponseRedirect(reverse('pagos:listarPagos', args=[kwargs.get('pk')]))
		documento_form = self.form_class(request.POST, request.FILES)
		documento_form.fields['archivo'].required = False
		self.formulario = documento_form
		self.pago_monto = float(request.POST['monto'])
		return post_pago_nuevo_modificado(self, request, documento_form, self.pago, self.pago.permiso)


def post_pago_nuevo_modificado(self, request, documento_form, pago, permiso):
	monto = float(request.POST['monto'])
	
	if documento_form.is_valid():
		
		fecha_de_pago = datetime.strptime(documento_form.data['fecha'], "%Y-%m-%d").date()
		lista_resoluciones = permiso.documentos.filter(tipo__nombre = 'Resolución') 
		fecha_primer_resolucion = lista_resoluciones[0].fecha
		if (monto > 0) and (fecha_de_pago >= fecha_primer_resolucion) and (fecha_de_pago <= date.today()):
			documento_nuevo = documento_form.save(commit=False)
			if pago == None:
				documento_nuevo.tipo = TipoDocumento.get_protegido('pago')
				documento_nuevo.estado = 2
				documento_nuevo.save()
				pago = Pago(permiso=permiso, monto=monto, documento=documento_nuevo, fecha=fecha_de_pago)
				permiso.agregar_documentacion(documento_nuevo)
			else:
				if len(request.FILES.getlist('archivo')) != 0:
					pago.documento.archivo = documento_nuevo.archivo
				pago.documento.descripcion = documento_nuevo.descripcion
				pago.documento.fecha = documento_nuevo.fecha
				pago.documento.save()
				pago.fecha = fecha_de_pago
				pago.monto = monto
			pago.save()
			return HttpResponseRedirect(reverse('pagos:listarPagos', args=[pago.permiso.id,]))
		else:
			return self.render_to_response({'form':documento_form, 'return_path':reverse('pagos:listarPagos', args=[permiso.pk]), 'return_label':'Volver al listado de pagos', 'message_error' : ['El monto debe ser mayor a 0']})
			#else:
			#	return self.render_to_response(self.get_context_data(form=documento_form, return_path=reverse('pagos:listarPagos', args=[permiso.pk]), message_error = ['La fecha de Pago debe ser mayor o igual a la fecha de de la resolución de otorgamiento de permiso y menor o igual a la fecha actual']))
	return self.render_to_response(self.get_context_data(formulario=documento_form, pago_monto = monto, message_error=['Datos Incorrectos']))


class ListarPagos(ExportMixin, SingleTableMixin, LoginRequiredMixin,FilterView):
	model = Pago
	template_name = 'pagos/listado.html'
	table_class = PagosTable
	paginate_by = 12
	filterset_class = PagosFilter
	export_name = 'listado_pagos'
	context_object_name = 'pagos'
	permission_required = 'pagos.listar_pago'

	def get_table_data(self):
		return self.permiso.pagos.all()

	def get(self, request, *args, **kwargs):
		self.permiso = Permiso.objects.get(pk=kwargs.get('pk'))
		if not request.user.has_perm(self.permission_required):
			Messages.error(self.request, 'No posee los permisos necesarios para realizar esta operación')
			return HttpResponseRedirect(reverse('permisos:detalle', args=[self.permiso.pk]))
		return super(ListarPagos,self).get(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(ListarPagos, self).get_context_data(**kwargs)
		context['nombreListado'] = 'Listado de Pagos del Permiso'
		context['return_path'] = reverse('permisos:detalle', args=[self.permiso.pk])
		context['particular'] = True
		estado_otorgado = True if len(self.permiso.estados.all().filter(tipo=6))>0 else False
		if isinstance(self.permiso.estado, (Otorgado,Baja)) and estado_otorgado:
			context['url_nuevo'] = reverse('pagos:altaPago',args=[self.permiso.pk])
		if not isinstance(self.permiso.estado, Archivado):
			context['url_nuevo2'] = reverse('pagos:AltaPagoInfraccion',args=[self.permiso.pk])
		return context

class EliminarPago(GenericEliminarView):
	model = Pago
	permission_required = 'pagos.eliminar_pago'

	def post(self, request, *args, **kwargs):
		if not request.user.has_perm(self.permission_required):
			return JsonResponse({"success": False,"message": ('permiso',"No posee los permisos necesarios para realizar esta operación")})
		self.object = self.get_object()
		self.object.delete()
		try:
			return JsonResponse({"success": True,"message": "Pago eliminado"})
		except:
			return JsonResponse({"success": False,"message": ('error',"No se puede eliminar el pago de ")})

class ListarTodosLosCobros(GenericListadoView):
	model = Cobro
	template_name = 'pagos/cobros/listado.html'
	table_class = CobrosTodosTable
	paginate_by = 12
	filterset_class = CobrosTodosFilter
	export_name = 'listado_cobros_todos'
	context_object_name = 'cobros'
	permission_required = 'pagos.listar_todos_cobros'
	redirect_url = '/'

	def get_context_data(self, **kwargs):
		context = super(ListarTodosLosCobros, self).get_context_data(**kwargs)
		context['nombreListado'] = "Listado de Cobros Generales"
		return context

class ListarTodosLosPagos(GenericListadoView):
	model = Pago
	template_name = 'pagos/listado.html'
	table_class = PagosTodosTable
	paginate_by = 12
	filterset_class = PagosTodosFilter
	export_name = 'listado_pagos_todos'
	permission_required = 'pagos.listar_todos_pagos'
	redirect_url = '/'

	def get_context_data(self, **kwargs):
		context = super(ListarTodosLosPagos, self).get_context_data(**kwargs)
		context['nombreListado'] = "Listado de Pagos Generales"
		return context


class AltaCobroInfraccion(LoginRequiredMixin,CreateView):
	model = Cobro
	form_class = DocumentoProtegidoForm
	template_name = 'pagos/alta.html'
	success_url = reverse_lazy('pagos:listarCobros')
	permission_required = 'pagos.cargar_cobro_infraccion'

	def get_context_data(self, **kwargs):
		context = super(AltaCobroInfraccion, self).get_context_data(**kwargs)
		context['nombreForm'] = "Cobro de Infraccion"
		context['form'].fields['archivo'].label = 'Archivo de Cobro de Infracción'
		context['return_path'] = reverse('permisos:detalle', args=[self.permiso_pk])
		context['return_label'] = 'Volver al Detalle de Permiso'
		return context

	def get (self, request, *args, **kwargs):
		self.permiso_pk = kwargs.get('pk')
		if not request.user.has_perm(self.permission_required):
			Messages.error(self.request, 'No posee los permisos necesarios para realizar esta operación')
			return HttpResponseRedirect(reverse('permisos:detalle', args=[self.permiso_pk]))
		return super(AltaCobroInfraccion, self).get(request,*args,**kwargs)	

	def post(self, request, *args, **kwargs):
		permiso = Permiso.objects.get(pk=kwargs.get('pk'))
		if not request.user.has_perm(self.permission_required):
			Messages.error(self.request, 'No posee los permisos necesarios para realizar esta operación')
			return HttpResponseRedirect(reverse('permisos:detalle', args=[permiso.pk]))

		documento_form = DocumentoProtegidoForm(request.POST, request.FILES)
		
		if documento_form.is_valid():
			documento = documento_form.save(commit=False)
			fecha_de_cobro = documento.fecha
			try:
				monto = float(request.POST['monto'])
			except Exception:
				monto = None

			if fecha_de_cobro >= permiso.fechaSolicitud and monto != None:
				documento.tipo = TipoDocumento.get_protegido('cobro-infraccion')
				documento.estado = 2
				documento = documento_form.save()
				cobro = Cobro(permiso=permiso, monto=monto, documento=documento, 
					fecha_desde=fecha_de_cobro, fecha=fecha_de_cobro, es_por_canon=False)
				cobro.save()
				permiso.agregar_documentacion(documento)
				return HttpResponseRedirect(reverse('permisos:detalle', args=[permiso.pk,]))
			else:
				return render(request, self.template_name, {'form': documento_form, 'monto':str(monto), 'nombreForm': 'Cobro de Infraccion','return_label':'Volver al Detalle de Permiso','return_path': reverse('permisos:detalle', args=[permiso.pk]),
					'message_error': ['La fecha de cobro debe ser igual o mayor a la fecha de solicitud (' + permiso.fechaSolicitud.strftime('%d/%m/%Y'+')'),"Ingresar un monto correcto"]})
		
		documento_form.fields['archivo'].label = 'Archivo de Cobro de Infracción'
		return render(request, self.template_name, {'form':documento_form, 'nombreForm':"Cobro de Infraccion",'return_label':'Volver al Detalle de Permiso','return_path': reverse('permisos:detalle', args=[permiso.pk]), 'message_error':['Error en la carga']})


class AltaPagoInfraccion(LoginRequiredMixin,CreateView):
	model = Pago
	form_class = DocumentoProtegidoForm
	template_name = 'pagos/alta.html'
	success_url = reverse_lazy('pagos:listarPagos')
	permission_required = 'pagos.cargar_pago_infraccion'

	def get_context_data(self, **kwargs):
		context = super(AltaPagoInfraccion, self).get_context_data(**kwargs)
		context['nombreForm'] = "Pago de Infraccion"
		context['return_path'] = reverse('permisos:detalle', args=[self.permiso_pk])
		context['return_label'] = 'Volver al Detalle de Permiso'
		context['form'].fields['archivo'].label = 'Archivo del Pago de Infracción'
		return context

	def get(self, request, *args, **kwargs):
		self.permiso_pk = kwargs.get('pk')
		if not request.user.has_perm(self.permission_required):
			Messages.error(self.request, 'No posee los permisos necesarios para realizar esta operación')
			return HttpResponseRedirect(reverse('permisos:detalle', args=[self.permiso_pk]))
		return super(AltaPagoInfraccion, self).get(request,*args,**kwargs)

	def post(self, request, *args, **kwargs):
		self.object = self.get_object
		self.permiso_pk = kwargs.get('pk')
		permiso = Permiso.objects.get(pk=kwargs.get('pk'))
		if not request.user.has_perm(self.permission_required):
			Messages.error(self.request, 'No posee los permisos necesarios para realizar esta operación')
			return HttpResponseRedirect(reverse('permisos:detalle', args=[permiso.pk]))
		documento_form = self.form_class(request.POST, request.FILES)
		
		if documento_form.is_valid():
			try:
				monto = float(request.POST['monto'])
			except Exception:
				monto = None
			fecha_de_pago = datetime.strptime(documento_form.data['fecha'], "%Y-%m-%d").date()
			fechaSolicitud = permiso.fechaSolicitud

			if (monto != None) and (fecha_de_pago >= fechaSolicitud) and (fecha_de_pago <= date.today()):
				documento = documento_form.save(commit=False)
				documento.tipo = TipoDocumento.get_protegido('pago-infraccion')
				documento.estado = 2
				documento.save()
				pago = Pago(permiso=permiso, monto=monto, documento=documento, fecha=fecha_de_pago, es_por_canon=False)
				pago.save()
				permiso.agregar_documentacion(documento)
				return HttpResponseRedirect(reverse('permisos:detalle', args=[permiso.id,]))
			else:
				return render(request, self.template_name, self.get_context_data(form=documento_form, message_error = ['La fecha de Pago debe ser mayor o igual a la fecha de Solicitud de permiso y menor o igual a la fecha actual ('
				+ (fechaSolicitud).strftime("%d-%m-%Y") + ' - ' + (date.today()).strftime("%d-%m-%Y") + ')',"El monto debe ser mayor a 0"]))
		return self.render_to_response(self.get_context_data(form=documento_form, message_error=['Error en la carga',"El monto debe ser mayor a 0"]))


