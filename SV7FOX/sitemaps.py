from django.contrib.sitemaps import Sitemap
from SV7FOX.models import Page, Menu

class GoogleSitemap(Sitemap):
    priority = 0.5
    changefreq = 'weekly'

    def items(self):
        return Menu.objects.all()

    def lastmod(self, obj):
        return obj.page.last_update
