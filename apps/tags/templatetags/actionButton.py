from django import template

register = template.Library()


@register.inclusion_tag('actionButtons.html', takes_context=True)
def renderActionButton(context, idObjeto):
    reverseString = '{0}:detalle {1}'.format(context['nombreReverse'], idObjeto)

    return {
        'url': reverse(reverseString)
        }
