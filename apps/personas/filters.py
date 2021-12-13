import django_filters
from apps.personas.models import *


def get_roles_choices():
    choices = []
    for rol in Persona.tipoRol:
        evaluado = eval(rol)
        choices.append((evaluado.TIPO, rol))
    return choices

class PersonaFilter(django_filters.FilterSet):
    roles__tipo = django_filters.ChoiceFilter(choices=get_roles_choices())
    nombre = django_filters.CharFilter(method='search_filter')
    numeroDocumento = django_filters.CharFilter(label='N° Doc.', lookup_expr='icontains')

    class Meta:
        model = Persona
        fields = ['roles__tipo']

    def search_filter(self, queryset, name, value):
        return queryset.filter(Q(nombre__icontains=value) 
                                | Q(apellido__icontains=value))