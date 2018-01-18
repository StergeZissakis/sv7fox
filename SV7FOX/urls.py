import django
from django.conf import settings
from django.contrib import admin
from django.conf.urls import include, url
from django.conf.urls.static import static
from SV7FOX import settings
from SV7FOX import views
from SV7FOX.sitemaps import GoogleSitemap
from django.contrib.sitemaps.views import sitemap


# url(r'^admin/', include(admin.site.urls)),

urlpatterns = [
		url(r'^admin/', admin.site.urls),
    url(r'^static/(?P<path>.*)$', django.views.static.serve, {'document_root': settings.STATIC_ROOT}),
    url(r'^media/(?P<path>.*)$', django.views.static.serve, {'document_root': settings.MEDIA_ROOT}),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^qso$', views.qso),
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': {'sv7fox.com' : GoogleSitemap}}),
    url(r'^(?P<path>.*)$', views.broker),
]
