import django_filters
from apps.permisos.models import *
from django.db.models import Max
from django.db.models import Q
from datetime import date

def get_estados_choices():
    choices = []
    for estado in Permiso.ESTADOS:
        evaluado = eval(estado)
        choices.append((evaluado.TIPO, evaluado))
    return choices

class PermisosFilter(django_filters.FilterSet): 
    estados__tipo = django_filters.ChoiceFilter(label='Estado',choices=get_estados_choices(),method='listing_filter')
    solicitante = django_filters.CharFilter(method='search_filter')
    situacion = django_filters.ChoiceFilter(label="Situación", choices=[("en_tramite","En Tramite"),("vigente","Vigente"),("vencido","Vencido")],
                            method='situacion_filter')

    class Meta:
        model = Permiso
        fields = ['estados__tipo']
        
    def listing_filter(self, queryset, name, value):
        return queryset.annotate(maximo=Max('estados__tipo')).filter(maximo=value)

    def search_filter(self, queryset, name, value):
        return queryset.filter(Q(solicitante__nombre__icontains=value) 
                                | Q(solicitante__apellido__icontains=value))

    def situacion_filter(self, queryset, name, value):

        sit_dict = {
            'en_tramite': Q(pk__in=[obj.pk for obj in Permiso.objects.all() if obj.estado.tipo < 6]),
            'vigente': Q(pk__in=[obj.pk for obj in Permiso.objects.all() if obj.estado.tipo == 6]),
            'vencido': Q(pk__in=[obj.pk for obj in Permiso.objects.all() if obj.estado.tipo == 6 and obj.fechaVencimiento<=date.today()]),
            'baja': Q(estados__tipo__gt=6)
        }

        return queryset.filter(sit_dict.get(value,[]))
        


class TipoDeUsoFilter(django_filters.FilterSet): 
    periodo = django_filters.ChoiceFilter(label='Periodo',choices=TipoUso.TipoPeriodo)
    medida = django_filters.ChoiceFilter(label='Medida',choices=TipoUso.TipoMedida)
    tipo_modulo = django_filters.ChoiceFilter(label='Tipo Módulo',choices=TipoUso.TipoModulo)
    