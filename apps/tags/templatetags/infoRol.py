from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag()
def renderInfoRol(rol):
	stringreturn = ''
	if rol.getInfo() is None:
		return ''
	
	for info in rol.getInfo():
		stringreturn += '<p> '
		stringreturn += info
		stringreturn += ': '
		stringreturn += rol.getInfo()[info]
		stringreturn += '</p> '
	return mark_safe(stringreturn)