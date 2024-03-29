from django.shortcuts import render
from django.db.models import Q
from apps.permisos.models import Permiso, TipoUso
from apps.pagos.models import Cobro, Pago
from django.views.generic import FormView
from django.views.generic.base import TemplateView
from .forms import FiltroForm, FiltroRecaudacionForm
from django.http import JsonResponse
from django.urls import reverse
from itertools import product
import json
from apps.documentos.models import Documento
from apps.comisiones.models import Comision
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect

class DashBoardReportes(TemplateView):
    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class Recaudacion(LoginRequiredMixin,PermissionRequiredMixin,FormView):
    template_name = 'recaudacion/recaudacion.html'
    form_class = FiltroRecaudacionForm
    permission_required = 'reportes.recaudacion'
    redirect_url = 'pagos:listarModulos'
    
    def handle_no_permission(self):
        messages.error(self.request, 'No posee los permisos necesarios para realizar esta operación')
        return redirect(self.redirect_url)
        
    def get_context_data(self, **kwargs):
        context = super(Recaudacion, self).get_context_data(**kwargs)
        context['nombreReporte'] = "Reportes de Recaudación"
        context['fechas'] = True
        context['url_ajax'] = reverse('reportes:recaudacion')
        return context

    def get(self, request, *args, **kwargs):
        if(request.is_ajax()):
            if request.GET.get('tipo_reporte')=='tipos_permisos':
                return self.get_recaudacion_tp_ajax(request, *args, **kwargs)
            elif request.GET.get('tipo_reporte')=='series_temporales':
                return self.get_recaudacion_st_ajax(request, *args, **kwargs)
            elif request.GET.get('tipo_reporte')=='proyeccion_valores_modulos':
                return self.get_recaudacion_pvm_ajax(request, *args, **kwargs)
            else:
                return super().get(request, *args, **kwargs)
        return super().get(request, *args, **kwargs)
    
    def get_recaudacion_tp_ajax(self, request, *args, **kwargs):
                
        formu = self.form_class(request.GET)

        recaudacion_dict = {}
        dict_tipos = {}

        if formu.is_valid():
            tipos = TipoUso.objects.filter(pk__in=formu.cleaned_data['tipos_permisos']) if len(formu.cleaned_data['tipos_permisos'])>0 else TipoUso.objects.all()
            for t in tipos: 
                dict_tipos[t.descripcion] = {'Canon':{'Pago':0,'Cobro':0,'Diferencia':0},'Infraccion':{'Pago':0,'Cobro':0,'Diferencia':0}} 
            
            l_operaciones = [formu.cleaned_data['operaciones']] if formu.cleaned_data['operaciones'] != '' else ["Cobro","Pago"]

            for m in l_operaciones:
                recaudacion_dict[m] = list(eval(m).operaciones.ingresos(formu.cleaned_data,request.GET.get('fecha_desde'),request.GET.get('fecha_hasta'), False))
                for r in recaudacion_dict[m]:
                    if r['es_por_canon']:
                        dict_tipos[r['permiso__tipo__descripcion']]['Canon'][m] = r['monto']
                    else:
                        dict_tipos[r['permiso__tipo__descripcion']]['Infraccion'][m] = r['monto']
            if len(l_operaciones)==2:
                for dt in dict_tipos:
                    dict_tipos[dt]['Canon']['Diferencia']=round(dict_tipos[dt]['Canon']['Pago']-dict_tipos[dt]['Canon']['Cobro'],2)
                    dict_tipos[dt]['Infraccion']['Diferencia']=round(dict_tipos[dt]['Infraccion']['Pago']-dict_tipos[dt]['Infraccion']['Cobro'],2)

            totales = {'Canon':{'Pago':0,'Cobro':0,'Diferencia':0},'Infraccion':{'Pago':0,'Cobro':0,'Diferencia':0}}
            for mot in ["Canon","Infraccion"]:
                for dt in dict_tipos:
                    totales[mot]['Pago'] += dict_tipos[dt][mot]['Pago']
                    totales[mot]['Cobro'] += dict_tipos[dt][mot]['Cobro']
                    totales[mot]['Diferencia'] += round(dict_tipos[dt][mot]['Diferencia'],2)
            dict_tipos['TOTALES']=totales
            
        return JsonResponse(dict_tipos)

    def get_recaudacion_st_ajax(self, request, *args, **kwargs):
        formu = self.form_class(request.GET)
        operaciones = []
        if formu.is_valid():
            l_operaciones = [formu.cleaned_data['operaciones']] if formu.cleaned_data['operaciones'] != '' else ["Cobro","Pago"]
            for o in l_operaciones:
                l_op_o = list(eval(o).operaciones.ingresos(formu.cleaned_data,request.GET.get('fecha_desde'),request.GET.get('fecha_hasta'), True))
                for e in l_op_o:
                    e['operacion'] = o
                operaciones += l_op_o
            return JsonResponse(operaciones,safe=False)

        return(formu.errors)


    def get_recaudacion_pvm_ajax(self, request, *args, **kwargs):
        formu = self.form_class(request.GET) #TODO ver que datos servirian para personalizar los calculos de modulos
        l = []
        if formu.is_valid():
            l += Permiso.recaudacion_pmv()
            return JsonResponse(l,safe=False)
        return JsonResponse(formu.errors)

class Productividad(FormView):
    template_name = "productividad/productividad.html"
    form_class = FiltroForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nombreReporte'] = "Reporte de Gestion de Permiso"
        context['url_ajax'] = reverse('reportes:gestion')
        context['fechas'] = False
        return context

    def get(self, request, *args, **kwargs):
        if(request.is_ajax()):
            return self.get_productividad_ajax(request, *args, **kwargs)
        return super().get(request, *args, **kwargs)

    def get_productividad_ajax(self, request, *args, **kwargs):
        formu = self.form_class(request.GET)
        if formu.is_valid():
            return JsonResponse(Permiso.estados_productividad(formu.cleaned_data),safe=False)
        return JsonResponse(formu.errors)

class RepComisiones(FormView):
    template_name = "comisiones/comisiones.html"
    form_class = FiltroForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nombreReporte'] = "Reporte de Comisiones"
        context['url_ajax'] = reverse('reportes:comisiones')
        context['fechas'] = True
        return context

    def get(self, request, *args, **kwargs):
        if(request.is_ajax()):
            return self.get_comision_ajax(request, *args, **kwargs)
        return super().get(request, *args, **kwargs)

    def get_comision_ajax(self, request, *args, **kwargs):
        l = []
        formu = self.form_class(request.GET)
        if formu.is_valid():
            data = formu.cleaned_data

            filtros = Q()
            filtros &= Q(tipo__pk__in= data['tipos_permisos']) if data['tipos_permisos'].exists() else Q()
            filtros &= Q(afluente__in=data['afluentes']) if data['afluentes'].exists() else Q()
            filtros &= Q(establecimiento__localidad__pk__in=data['localidades']) if data['localidades'].exists() else Q()
            filtros &= Q(establecimiento__localidad__departamento__pk__in=data['departamentos']) if data['departamentos'].exists() else Q()


            permisos = Permiso.objects.filter(filtros)
            documentos_permisos = []
		    

            for p in permisos:
                documentos_permisos += p.documentos.values_list('id',flat=True)

            doc_reporte = Documento.rep_inspeccion_infraccion(documentos_permisos,request.GET.get('fecha_desde'),request.GET.get('fecha_hasta'))
            l += doc_reporte[1]
            l += Comision.rep_comisiones(doc_reporte[0])
            
            return JsonResponse(l,safe=False)
        return JsonResponse(formu.errors)