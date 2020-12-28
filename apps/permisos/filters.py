import django_filters
from apps.permisos.models import *
from django.db.models import Max

def get_estados_choices():
    choices = []
    for estado in Permiso.ESTADOS:
        evaluado = eval(estado)
        choices.append((evaluado.TIPO, evaluado))
    return choices

class PermisosFilter(django_filters.FilterSet): 
    estados__tipo = django_filters.ChoiceFilter(label='Estado',choices=get_estados_choices(),method='filter_listing')
    
    class Meta:
        model = Permiso
        fields = ['estados__tipo']
        
    def filter_listing(self, queryset, name, value):
        return queryset.annotate(maximo=Max('estados__tipo')).filter(maximo=value)

class TipoDeUsoFilter(django_filters.FilterSet): 
    periodo = django_filters.ChoiceFilter(label='Periodo',choices=TipoUso.TipoPeriodo)
    medida = django_filters.ChoiceFilter(label='Medida',choices=TipoUso.TipoMedida)
    tipo_modulo = django_filters.ChoiceFilter(label='Tipo Modulo',choices=TipoUso.TipoModulo)
    