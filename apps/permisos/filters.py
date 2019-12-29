import django_filters
from apps.permisos.models import *

def get_estados_choices():
    choices = []
    for estado in Estado.ESTADOS:
        evaluado = eval(estado)
        choices.append((evaluado.TIPO, evaluado))
    return choices


class PermisosFilter(django_filters.FilterSet): 
    estados = django_filters.ChoiceFilter(choices=get_estados_choices())
    