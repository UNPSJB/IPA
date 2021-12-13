from django import template
register = template.Library()

@register.filter(name='has_group') 
def has_group(user, group_name):

    list_group = group_name.split(' ')

    if "JefedeDepartamento" in list_group:
        list_group["JefedeDepartamento"] = "Jefe de departamento"

    print(list_group)

    return user.groups.filter(name__in=list_group).exists() 