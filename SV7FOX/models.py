from django.db import models
from SV7FOX import settings
from django.utils.text import *
from unidecode import unidecode
from django.template import defaultfilters
from mptt.models import MPTTModel, TreeForeignKey

class ImageBase(models.Model):
    alt = models.CharField(max_length=256, null=True)

    def get_image_url(self):
        return self.src.url

    def html_img(self, style_class = ""):
        return '<img alt="%s" class="img-thumbnail %s" src ="%s">' %  (self.alt , style_class, self.get_image_url())

    def __unicode__(self):
        return self.html_img("admin-featured-thumb")

class Image(ImageBase):
    src = models.ImageField(upload_to=settings.IMAGES_URL, null=True)


class CarouselImage(ImageBase):
    src = models.ImageField(upload_to=settings.IMAGES_URL + "carousel/", null=True)
    label = models.CharField(max_length=256)
    description = models.CharField(max_length=512, null=True)

class Page(models.Model):
    title = models.CharField(max_length=256, verbose_name="Title")
    image = models.ForeignKey('Image', verbose_name="Featured Image", related_name="featured_image", blank=True, null=True, on_delete=models.SET_NULL)
    summary = models.TextField(max_length=768)
    content = models.TextField(max_length=2048, verbose_name="Page Content")
    promote = models.BooleanField(default=False)
    front_page = models.BooleanField(default=False)
    last_update = models.DateTimeField(auto_now = True)

    def slug(self):
        return defaultfilters.slugify(unidecode(self.title))

    def get_absolute_url(self):
        return '/%s' % self.slug()

    def __unicode__(self):
        return self.title


class Menu(MPTTModel):
    parent = TreeForeignKey('self', null=True, blank=True, related_name='parent_menu', verbose_name="Parent", on_delete=models.SET_NULL)
    page = models.OneToOneField(Page, verbose_name="Page", related_name="menu_page", blank=False, null=False, on_delete=models.PROTECT)
    order = models.PositiveIntegerField()

    class MPTTMeta:
        order_insertion_by = ['order']

    def save(self, *args, **kwargs):
        super(Menu, self).save(*args, **kwargs)
        Menu.objects.rebuild()

    def isTopMenuItem(self):
        return self.get_ancestors().count() == 0

    def getChildren(self):
        #return Menu.objects.filter(submenu_items=self.id).order_by('title')
        return self.get_descendants()

    def hasChildren(self):
        return self.get_descendant_count()

    def isChildOf(self, page):
        return self.is_descendant_of(page)

    def getParent(self):
        return self.parent

    def slug(self):
        return self.page.slug()

    def get_absolute_url(self):
        return self.page.get_absolute_url()

    def __unicode__(self):
        return self.page.title

