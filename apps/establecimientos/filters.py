import django_filters
from apps.establecimientos.models import *


def departaments(request):
    return Departamento.protegidos.all()

class LocalidadesFilter(django_filters.FilterSet):
    departamento = django_filters.ModelChoiceFilter(label='Departamento',queryset=departaments)
    
    
class DepartamentosFilter(django_filters.FilterSet):
    nombre = django_filters.CharFilter(lookup_expr='iexact')

class AfluentesFilter(django_filters.FilterSet):
    nombre = django_filters.CharFilter(label='Nombre', lookup_expr='icontains')
    localidad__nombre = django_filters.CharFilter(label='Localidad', lookup_expr='icontains')
    
class EstablecimientosFilter(django_filters.FilterSet):
    localidad__nombre = django_filters.CharFilter(label='Localidad', lookup_expr='icontains')
    #codigo catastral
         
    

        
    