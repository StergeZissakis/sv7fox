from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from SV7FOX import settings
from SV7FOX.sitemaps import GoogleSitemap



admin.autodiscover()

urlpatterns = patterns('',

    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^qso$', 'SV7FOX.views.qso'),
    url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': {'sv7fox.com' : GoogleSitemap}}),
    url(r'^(?P<path>.*)$', 'SV7FOX.views.broker'),
)

