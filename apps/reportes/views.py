from django.shortcuts import render
from apps.permisos.models import Permiso, TipoUso
from apps.pagos.models import Cobro, Pago
from django.views.generic import FormView
from django.views.generic.base import TemplateView
from .forms import FiltroRecaudacionForm
from django.http import JsonResponse
from django.urls import reverse
from itertools import product

class DashBoardReportes(TemplateView):
    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class Recaudacion(FormView):
    template_name = 'recaudacion/base.html'
    form_class = FiltroRecaudacionForm
    
    def get_context_data(self, **kwargs):
        context = super(Recaudacion, self).get_context_data(**kwargs)
        context['nombreReporte'] = "Reportes de Recaudación"
        
        context['url_ajax'] = reverse('reportes:recaudacion')
        return context

    def get(self, request, *args, **kwargs):
        if(request.is_ajax()):
            print(request)
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

            print(dict_tipos)
            totales = {'Canon':{'Pago':0,'Cobro':0,'Diferencia':0},'Infraccion':{'Pago':0,'Cobro':0,'Diferencia':0}}
            for mot in ["Canon","Infraccion"]:
                for dt in dict_tipos:
                    totales[mot]['Pago'] += dict_tipos[dt][mot]['Pago']
                    totales[mot]['Cobro'] += dict_tipos[dt][mot]['Cobro']
                    totales[mot]['Diferencia'] += round(dict_tipos[dt][mot]['Diferencia'],2)
            dict_tipos['TOTALES']=totales
            
        else:
            print("NO ES VALIDAD EL FORMULARIO")
            print(formu.errors)

        return JsonResponse(dict_tipos)


    def graficos_ajax(self,operaciones):
        labels = []
        data = []

        for c in operaciones: 
            labels.append(TipoUso.objects.get(id=c['permiso__tipo']).descripcion) 
            data.append(c['monto'])

        return JsonResponse({'data':data,'labels':labels})

    
    def get_recaudacion_st_ajax(self, request, *args, **kwargs):
        formu = self.form_class(request.GET)

        dict_tipos = {}

        if formu.is_valid():
            print("ES VALIDAD EL FORMULARIO")
            tipos = TipoUso.objects.filter(pk__in=formu.cleaned_data['tipos_permisos']) if len(formu.cleaned_data['tipos_permisos'])>0 else TipoUso.objects.all()
            l_operaciones = [formu.cleaned_data['operaciones']] if formu.cleaned_data['operaciones'] != '' else ["Cobro","Pago"]
            
            l_motivos = [self.MOVIMIENTO[formu.cleaned_data['motivos']]] if formu.cleaned_data['motivos'] != '' else ["Canon","Infraccion"]
            
            for t in tipos: 
                dict_tipos[t.descripcion] = {} 
                for o in l_operaciones:
                    dict_tipos[t.descripcion][o] = {}
                    for m in l_motivos:
                        dict_tipos[t.descripcion][o][m] = []

            for o in l_operaciones:
                operaciones = list(eval(o).operaciones.ingresos(formu.cleaned_data,request.GET.get('fecha_desde'),request.GET.get('fecha_hasta'), True))
                for r in operaciones:
                    if r['es_por_canon']:
                        dict_tipos[r['permiso__tipo__descripcion']][o]["Canon"].append({'monto':r['monto'],'fecha':r['fecha']})
                    else:
                        dict_tipos[r['permiso__tipo__descripcion']][o]['Infraccion'].append({'monto':r['monto'],'fecha':r['fecha']})
        else:
            print("NO ES VALIDAD EL FORMULARIO")
            print(formu.errors)

        print(dict_tipos)
        return JsonResponse(dict_tipos)


    def get_recaudacion_pvm_ajax(self, request, *args, **kwargs):
        formu = self.form_class(request.GET)

        dict_tipos = {}

        if formu.is_valid():
            print("ES VALIDAD EL FORMULARIO")

            
            #LISTAR TODOS LOS PERMISOS EN ESTADO OTORGADO ----> LOS VENCIDOS IGUALMENTE SE PUEDEN CALCULAR LA PARTE ADEUDADA
            #Permiso.objects.en_estado(Otorgado)

            #CALCULAR COBRO CON EL VALOR MAS ACTUAL --> cobro = permiso.estado.recalcular(request.user, documento, fecha, permiso.unidad)
            #cobros.append(cobro)
            
            #VER EN DONDE CALCULAR LOS ACUMULADOS - SI EN BACKEND O FRONTED

            #DEVOLVER JSON CON
            #TIPO_PERMISO - MONTO - FECHA HASTA CALCULADO - VALOR DE MODULO UTILIZADO - DEFINITIVO / PROVISORIO (valor de modulo maximo al vencimiento, o bien valor a fecha actual - hoy ## tener en cuenta maximo valor de modulo cargado en sistema)

            

        else:
            print("NO ES VALIDAD EL FORMULARIO")
            print(formu.errors)
        print(dict_tipos)
        return JsonResponse(dict_tipos)