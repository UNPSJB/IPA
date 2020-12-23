import django_filters
from apps.establecimientos.models import *


def departaments(request):
    return Departamento.protegidos.all()


class LocalidadesFilter(django_filters.FilterSet):
    
    departamento = django_filters.ModelChoiceFilter(label='Departamento',queryset=departaments)
    
    
      
    

        
    