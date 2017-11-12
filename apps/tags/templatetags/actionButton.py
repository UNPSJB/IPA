from django import template
from django.core.urlresolvers import reverse, reverse_lazy
register = template.Library()


@register.inclusion_tag('actionButtons.html', takes_context=True)
def renderActionButton(context, objectId):
	return {
		'url': reverse(context['nombreReverse'] + ':detalle', args=[objectId] )
		}
