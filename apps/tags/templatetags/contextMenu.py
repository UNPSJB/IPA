from django import template
from django.utils.safestring import mark_safe
import itertools
register = template.Library()


@register.simple_tag(takes_context=True)
def renderContextMenu(context):
    """ menu = ' <div class="ui vertical fluid blue inverted large menu right">' """
    #menu = '<div class="ui compact menu"> <div class="ui simple dropdown item">Acción<i class="dropdown icon"></i><div class="menu">' 
    menu = '' 
    botones = context['botones']
    if len(botones)>4:
        for boton in dict(itertools.islice(botones.items(),0, 4)):
            url = botones[boton]
            menu += '<a class="ui blue button" href=" ' +  str(url) + ' "></i> ' + boton + ' </a>'
        menu += '<div class="ui right dropdown red item">Más Acciones<i class="dropdown icon"></i> \
                <div class="menu">'
        for boton in dict(itertools.islice(botones.items(),4, len(botones))):
            url = botones[boton]
            menu += '<a class="red item" href=" ' +  str(url) + ' "></i> ' + boton + ' </a>'
        menu += '</div></div>'
    else:
        for boton in botones:
            url = botones[boton]
            menu += '<a class="ui blue button" href=" ' +  str(url) + ' "></i> ' + boton + ' </a>'
    #menu += '</div></div></div>'	
    
    return mark_safe(menu)
