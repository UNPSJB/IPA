from django.conf.urls import url

from apps.establecimientos.views import alta_establecimiento

urlpatterns = [

	url(r'^alta_establecimiento$', alta_establecimiento, name='alta_establecimiento'),
	
]