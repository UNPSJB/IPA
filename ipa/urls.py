"""ipa URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.views import logout, password_reset, password_reset_done
from django.views.generic import TemplateView
from . import views
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.views.static import serve

urlpatterns = [
    # Ruta de index
    url(r'^$', login_required(TemplateView.as_view(template_name="index2.html"), login_url='login'), name='index'),
    
    # Ruta al admin de Django
    url(r'^admin/', admin.site.urls, name = 'admin'),
    
    # Rutas al login y al logout 
    url(r'^login/', views.Login.as_view(), name='login'),
    url(r'^logout/', logout, name='logout'),

    # Rutas de recuperacion de contraseña
    url(r'^recovery/password_reset', password_reset, {'template_name':'recovery/password_reset_form.html', 'email_template_name': 'recovery/password_reset_email.html'} ,name='password_reset'),
    url(r'^recovery/password_reset_done', password_reset_done, {'template_name':'recovery/password_reset_done.html'},name='password_reset_done'),

    # Inclusion de rutas de aplicaciones
    url(r'^tiposDocumentos/', include('apps.documentos.urls.tipoDocumentos'), name='tipoDocumentos'),
    url(r'^documentos/', include('apps.documentos.urls.documento'), name='Documento'),
    url(r'^afluentes/', include('apps.establecimientos.urls.afluentes'), name='afluentes'),
    url(r'^departamentos/', include('apps.establecimientos.urls.departamentos'), name='departamentos'),
    url(r'^establecimientos/', include('apps.establecimientos.urls.establecimientos'), name='establecimientos'),
    url(r'^localidades/', include('apps.establecimientos.urls.localidades'), name='localidades'),
    url(r'^permisos/', include('apps.permisos.urls.permisos'), name='permisos'),
    url(r'^tiposDeUso/', include('apps.permisos.urls.tiposUso'), name='tiposDeUso'),
    url(r'^personas/', include('apps.personas.urls.personas'), name='persona'),
    url(r'^comision/', include('apps.comisiones.urls')),
    url(r'^pagos/', include('apps.pagos.urls')),
    url(r'^usuarios/', include('apps.users.urls')),
    url(r'^actas/', include('apps.documentos.urls.actas')),
    
    url(r'^empresas/', include('apps.personas.urls.empresas')),    
    url(r'^archivos/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT,}),    

]
