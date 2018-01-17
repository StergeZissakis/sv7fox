from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import render
from django.utils.text import *
from SV7FOX.models import (Page, CarouselImage, Menu)
from django.core.mail import send_mail
from django import forms
from SV7FOX import settings
from django.utils import html
import re

def broker(request, path):
    pages = Page.objects.all().order_by('title')
    menu = Menu.objects.all().order_by('order')
    top_menu = [m for m in menu if m.isTopMenuItem() == True ]
    front_pages = [ p for p in pages if p.front_page == True]
    carouselImages = CarouselImage.objects.order_by('alt')
    promos = [ p for p in pages if p.promote == True]

    page = [p for p in pages if p.slug() == path] if pages and path else False
    page = page[0] if page and len(page) else False


    page_menu = [m for m in menu if m.page == page ] if page else False
    current_page_parents = []
    if( page_menu and len(page_menu) ):
        page_menu = page_menu[0]
        current_page_parent_menus = page_menu.get_ancestors()
        current_page_parents = [m.page for m in current_page_parent_menus ]
    else:
        page = False
        page_menu = False

    template = 'page-'

    head_title = ' Αρχική'
    head_keywords = 'Ραδιοερασιτέχνης, SV7FOX, sv7fox.com, '
    head_description = 'Ο Ραδιοερασιτέχνης SV7FOX'

    if page:
        head_title = page.title
        head_description += html.strip_tags(page.summary).strip() + " " + html.strip_tags(page.content).strip();
        head_description = re.sub(" +", " ", head_description).strip('\n\r')
        keywords = set(head_description.split())
        head_keywords += ",".join([kw for kw in keywords if len(kw) > 4])

        if page.promote:
            template += 'promo'
        else:
            template += 'ordinary'
    else:
        template += 'front'

    template += '.html'

    return render(request, template,
                   {'pages': pages,
                    'front_pages': front_pages,
                    'top_menu': top_menu,
                    'carouselImages': carouselImages,
                    'promos': promos,
                    'current_page': page,
                    'current_page_parents' : current_page_parents,
                    'social_icons': ( { 'icon': 'facebook', 'link': '//www.facebook.com/pages/%CE%A1%CE%B1%CE%B4%CE%B9%CE%BF%CE%B5%CF%81%CE%B1%CF%83%CE%B9%CF%84%CE%B5%CF%87%CE%BD%CE%B9%CE%BA%CE%AC-%CE%91%CE%BE%CE%B5%CF%83%CE%BF%CF%85%CE%AC%CF%81/809493385751224', 'code': '' },
                                      # { 'icon': 'google-plus', 'link': '', 'code': '' }
                                      { 'icon': 'skype', 'link': 'skype:sv7fox-htc?call', 'code': '' },
                                      { 'icon': 'twitter', 'link': '//twitter.com/@Sv7foxPanos', 'code': ''}, ),
                    'seo': {'keywords': head_keywords, 'description': head_description, 'title': head_title },
                    'settings': settings}, )


class ContactForm(forms.Form):
    qrz = forms.CharField(label='qrz', max_length=12)
    email = forms.CharField(label='email', max_length=100)
    qso = forms.CharField(label='qso', max_length=5000)

def qso(request):
	if request.method == 'POST':
		form = ContactForm(request.POST)
		if form.is_valid() :
			from_email = form.cleaned_data['qrz'] + "<" + form.cleaned_data['email'] + '>'
			if( send_mail('QSO from sv7fox.com', form.cleaned_data['qso'], from_email, ['sv7fox@yahoo.gr'], fail_silently=True) != 1 ):
				raise Http404("")
			else:
				return HttpResponse('')
		else:
			raise Http404("")
	else:
		raise Http404("")












