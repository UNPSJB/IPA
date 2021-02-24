import django_filters
from apps.permisos.models import *
from django.db.models import Max
from django.db.models import Q

def get_estados_choices():
    choices = []
    for estado in Permiso.ESTADOS:
        evaluado = eval(estado)
        choices.append((evaluado.TIPO, evaluado))
    return choices

class PermisosFilter(django_filters.FilterSet): 
    estados__tipo = django_filters.ChoiceFilter(label='Estado',choices=get_estados_choices(),method='filter_listing')
    solicitante = django_filters.CharFilter(method='search_filter')

    class Meta:
        model = Permiso
        fields = ['estados__tipo']
        
    def filter_listing(self, queryset, name, value):
        return queryset.annotate(maximo=Max('estados__tipo')).filter(maximo=value)

    def search_filter(self, queryset, name, value):
        return queryset.filter(Q(solicitante__nombre__icontains=value) 
                                | Q(solicitante__apellido__icontains=value))

class TipoDeUsoFilter(django_filters.FilterSet): 
    periodo = django_filters.ChoiceFilter(label='Periodo',choices=TipoUso.TipoPeriodo)
    medida = django_filters.ChoiceFilter(label='Medida',choices=TipoUso.TipoMedida)
    tipo_modulo = django_filters.ChoiceFilter(label='Tipo Modulo',choices=TipoUso.TipoModulo)
    