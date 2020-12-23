import django_filters
from apps.establecimientos.models import *
from apps.personas.models import Persona


def empleados(request):
    return Persona.getEmpleadosParaComision()	


class ComisionFilter(django_filters.FilterSet):
    
    empleados = django_filters.ModelChoiceFilter(label='Empleados',queryset=empleados)
    
    
      