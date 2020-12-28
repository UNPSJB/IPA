import django_filters
from apps.pagos.models import *


class CobrosFilter(django_filters.FilterSet):
    tipo = django_filters.ChoiceFilter(label="Tipo de Cobro",field_name="es_por_canon",choices=((True,"Canon"), (False,"Infraccion")))

class CobrosTodosFilter(django_filters.FilterSet):
    tipo_cobro = django_filters.ChoiceFilter(label="Tipo de Cobro",field_name="es_por_canon",choices=((True,"Canon"), (False,"Infraccion")))
    permiso__tipo__descripcion = django_filters.CharFilter(label="Tipo Permiso",lookup_expr='icontains')


class PagosFilter(django_filters.FilterSet):
    tipo = django_filters.ChoiceFilter(label="Tipo de Pago",field_name="es_por_canon",choices=((True,"Canon"), (False,"Infraccion")))

class PagosTodosFilter(django_filters.FilterSet):
    tipo_pago = django_filters.ChoiceFilter(label="Tipo de Pago",field_name="es_por_canon",choices=((True,"Canon"), (False,"Infraccion")))
    permiso__tipo__descripcion = django_filters.CharFilter(label="Tipo Permiso",lookup_expr='icontains')

class ModulosFilter(django_filters.FilterSet):
    modulo = django_filters.ChoiceFilter(label="Tipo de Modulo",field_name="modulo",choices=((1,"Diesel"), (2,"Kw")))

        
    