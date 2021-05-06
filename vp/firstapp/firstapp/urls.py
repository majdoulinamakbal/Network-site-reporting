"""firstapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from adminpage.views import *
from django.conf.urls import *
from django.urls import path
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin', admin.site.urls),
    path('logout', logout),
    path("menu", menu),
    path("login",login),
    path('',home),
    path("element", element),
    path("download", download),
    path("downloadmod",downloadmod),
    path("downloadram",downloadram),
    path("RAMCPU",RAMCPU),
    path("uploadvul",uploadvul),
    path("updatevul",updatevul),
    path("vul",vul),
    path("FAN",FAN),
    path('upload',upload),
    path('uploadram',uploadram),
    path("eox",eox)

    
    


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)