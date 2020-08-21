from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag(takes_context=True)
def renderContextMenu(context):
    """ menu = ' <div class="ui vertical fluid blue inverted large menu right">' """
    menu = '<div class="ui compact menu"> <div class="ui simple dropdown item">Acción<i class="dropdown icon"></i><div class="menu">' 
    botones = context['botones']
    for boton in botones:
    	url = botones[boton]
    	menu += '<a class="item" href=" ' +  str(url) + ' "></i> ' + boton + ' </a>'
    menu += '</div></div></div>'	
    return mark_safe(menu)
