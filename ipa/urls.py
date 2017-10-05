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
from django.contrib.auth.views import login, logout
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^$', login_required(views.home, login_url='login'), name='index'),
    url(r'^admin/', admin.site.urls, name = 'admin'),
    url(r'^login/', login, {'template_name': 'login/login.html'}, name='login'),
    url(r'^logout/', logout, name='logout'),  
#    url(r'^tipos/', include())
  #  url(r'permisos/' include('apps.permisos.urls'), name='permisos')
    url(r'^documentos/', include('apps.tiposDocumentacion.urls'), name= 'documentos'),
    url(r'^permisos/', include('apps.permisos.urls'), name='solicitudes'),
    url(r'^afluentes/', include('apps.afluentes.urls'))
]
