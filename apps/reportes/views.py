from django.shortcuts import render
from apps.permisos.models import Permiso, TipoUso
from apps.pagos.models import Cobro, Pago
from django.views.generic import FormView
from .forms import IngresoForm
from django.http import JsonResponse


class IngresoTipoPermiso(FormView):
    template_name = 'reportes/ingresos.html'
    form_class = IngresoForm
    
    def get_context_data(self, **kwargs):
        context = super(IngresoTipoPermiso, self).get_context_data(**kwargs)
        context['nombreListado'] = "Reporte de Ingresos por Tipo de Permiso"  
        return context

    def get(self, request, *args, **kwargs):
        if(request.is_ajax()):
            return self.get_ingresos_ajax(request, *args, **kwargs)
        return super().get(request, *args, **kwargs)
    
    def get_ingresos_ajax(self, request, *args, **kwargs):
                
        formu = self.form_class(request.GET)
        ingresos_dict = {}

        if formu.is_valid():
            l_operaciones = [formu.cleaned_data['operaciones']] if formu.cleaned_data['operaciones'] != '' else ["Cobro","Pago"]

            for m in l_operaciones:
                ingresos_dict[m] = list(eval(m).operaciones.ingresos(formu.cleaned_data,request.GET.get('fecha_desde'),request.GET.get('fecha_hasta')))
        else:
            print("NO ES VALIDAD EL FORMULARIO")
            print(formu.errors)
        
        return JsonResponse(ingresos_dict)


    def graficos_ajax(self,operaciones):
        labels = []
        data = []

        for c in operaciones: 
            labels.append(TipoUso.objects.get(id=c['permiso__tipo']).descripcion) 
            data.append(c['monto'])

        return JsonResponse({'data':data,'labels':labels})
