from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag(takes_context=True)
def renderContextMenu(context):
    menu = ' <div class="ui vertical fluid blue inverted large menu right">'
    botones = context['botones']
    for boton in botones:
    	url = botones[boton]
   
    	menu += '<a class="item" href=" ' +  url + ' "></i> ' + boton + ' </a>'
    menu += '</div>'	
    return mark_safe(menu)
