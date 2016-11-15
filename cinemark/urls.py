"""cinemark URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
import filmes.views
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url, include
from django.contrib import admin

from django.contrib.auth.views import logout

urlpatterns = [
    url(r'^$', filmes.views.HomeList.as_view(), name="home"),
    url(r'^filme/(?P<pk>[0-9]+)/$', filmes.views.FilmeDetail.as_view(), name="filmes.detail"),


    url(r'^admin/', admin.site.urls),
    url(r'^'+settings.NAME_ADMIN+'/filmes/$', filmes.views.index, name="filmes.index"),
    url(r'^'+settings.NAME_ADMIN+'/filmes/(?P<id>[0-9]+)/$', filmes.views.view, name="filmes.view"),
    url(r'^'+settings.NAME_ADMIN+'/filmes/store/$', filmes.views.store, name="filmes.store"),
    url(r'^'+settings.NAME_ADMIN+'/filmes/create/$', filmes.views.create, name="filmes.create"),
    url(r'^'+settings.NAME_ADMIN+'/filmes/edit/(?P<pk>[0-9]+)/$', filmes.views.edit, name="filmes.edit"),
    url(r'^'+settings.NAME_ADMIN+'/filmes/delete/(?P<pk>[0-9]+)/$', filmes.views.FilmeDelete.as_view(), name="filmes.delete"),
    url(
        r'^logout/$',
        logout,
        name='logout',
        kwargs={'next_page': '/'}
    ),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]