from django.contrib import admin
from SV7FOX.models import Page, Image, CarouselImage, Menu
from ckeditor.widgets import CKEditorWidget
from django import forms
from mptt.admin import MPTTModelAdmin
from suit.admin import SortableModelAdmin

class AdminStatics:
    class Media:
        #js = ('js/admin/my_own_admin.js',)
        css = {
             'all': ('css/admin/my_style.css',)
        }

class ImageBaseAdmin(admin.ModelAdmin, AdminStatics):
    list_display = ('alt', 'html_img')
    model = Image

    def alt(self):
        return self.get_alt()

    def html_img(self, obj):
        return obj.html_img("admin-featured-thumb")
    html_img.allow_tags = True
    html_img.short_description = "Image"


class ImageAdmin(ImageBaseAdmin):
    pass


class CarouselImageAdmin(ImageBaseAdmin, AdminStatics):
    list_display = ('label', 'description', 'alt', 'html_img')
    ordering = ['alt']

    def label(self):
        return self.label()

    def description(self):
        return self.descirption()


class AltImageModelChoiceField(forms.ModelChoiceField):
     def label_from_instance(self, obj):
         return "%s" % (obj.alt, )

class PageAdminForm(forms.ModelForm):

    class Meta:
        model = Page
        fields = ('title', 'image', 'summary', 'content', 'promote', 'front_page', )
        exclude = []

    image = AltImageModelChoiceField(Image.objects.all())
    content = forms.CharField(widget=CKEditorWidget())

    def __init__(self,*args,**kwargs):
        super(PageAdminForm, self).__init__(*args,**kwargs)
        #self.fields['parent'].queryset = self.fields['parent'].queryset.exclude(pk = self.instance.pk)



class PageAdmin(admin.ModelAdmin, AdminStatics):
    list_display = ('title', 'summary', 'promote', 'front_page', 'feat_image', )

    form = PageAdminForm

    def feat_image(self, obj):
        return obj.image.html_img("admin-page-thumb")
    feat_image.allow_tags = True
    feat_image.short_description = "Featured Image"

    def front_page(self, obj):
        return self.front_page(obj)
    front_page.short_description = "On Front Page"


class MenuPageTitleChoiceField(forms.ModelChoiceField):
     def label_from_instance(self, obj):
         return "%s" % (obj.title, )

class MenuParentTitleChoiceField(forms.ModelChoiceField):
     def label_from_instance(self, obj):
         return "%s" % (obj.page.title, )


class MenuAdminForm(forms.ModelForm):

    class Meta:
        model = Menu
        fields = ('parent', 'page' )

    parent = MenuParentTitleChoiceField(queryset=Menu.objects.all(), required=False)
    page =  MenuPageTitleChoiceField(queryset=Page.objects.all(), required=True)

class MenuAdmin(MPTTModelAdmin, SortableModelAdmin, AdminStatics):
    list_display = ('prnt', 'pg', )

    mptt_level_indent = 30
    mptt_indent_field = 'pg'
    form = MenuAdminForm

    sortable = 'order'

    def prnt(self, obj):
        if( obj.parent ):
            return obj.parent.page.title
        else:
            return "None"
    prnt.short_description = "Parent Menu"

    def pg(self, obj):
        return obj.page.title
    pg.short_description = "Page"


admin.site.register(CarouselImage, CarouselImageAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(Menu, MenuAdmin)
