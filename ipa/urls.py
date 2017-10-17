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

urlpatterns = [
    # Ruta de index
    url(r'^$', login_required(TemplateView.as_view(template_name="index.html"), login_url='login'), name='index'),
    
    # Ruta al admin de Django
    url(r'^admin/', admin.site.urls, name = 'admin'),
    
    # Rutas al login y al logout 
    url(r'^login/', views.Login.as_view(), name='login'),
    url(r'^logout/', logout, name='logout'),  

    # Rutas de recuperacion de contraseña
    url(r'^recovery/password_reset', password_reset, {'template_name':'recovery/password_reset_form.html', 'email_template_name': 'recovery/password_reset_email.html'} ,name='password_reset'),
    url(r'^recovery/password_reset_done', password_reset_done, {'template_name':'recovery/password_reset_done.html'},name='password_reset_done'),

    # Inclusion de rutas de aplicaciones
    url(r'permisos/', include('apps.permisos.urls'), name='permisos'),
    url(r'^establecimientos/', include('apps.establecimientos.urls')),
    url(r'^documentos/', include('apps.tiposDocumentacion.urls'), name= 'documentos'),
    url(r'^tiposDeUso/', include('apps.tiposDeUso.urls'), name= 'tiposDeUso'),
    url(r'^afluentes/', include('apps.afluente.urls')),
    url(r'^edictos/', include('apps.edicto.urls')),
    url(r'^departamento/', include('apps.departamento.urls')),
    url(r'^localidades/', include('apps.localidad.urls')),

    url(r'^departamento/', include('apps.departamento.urls'))
]
