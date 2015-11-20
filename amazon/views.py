# -*- coding: utf-8 -*-
import json
from amazon.models import Item, Category, Subscriber
from cms.views import BaseView
from amazon.forms import SubscriberForm
from django.http.response import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic.base import TemplateView
from django.utils.translation import gettext as _


class Home(BaseView):
    template_name = 'amazon/home.html'

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        slides = Item.objects.filter(appear_in_slideshow=True)
        MIN_SLIDESHOW_ITEMS = 5
        if len(slides) >= MIN_SLIDESHOW_ITEMS:
            for item in slides:
                item.embed_code_big_image = item.get_embed_code(Item.BIG)
        context['slides'] = slides
        context['MIN_SLIDESHOW_ITEMS'] = MIN_SLIDESHOW_ITEMS
        return context


class ItemList(BaseView):
    template_name = 'amazon/item_list.html'

    def get_context_data(self, **kwargs):
        context = super(ItemList, self).get_context_data(**kwargs)
        category_slug = kwargs.get('category_slug')
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            default_length = 16
            if category.items_size == Item.BIG:
                default_length = 12
            elif category.items_size == Item.SMALL:
                default_length = 24
            context['category'] = category
            context['default_length'] = default_length
        return context

    def get(self, request, *args, **kwargs):
        if request.GET.get('format') == 'json':
            category_id = request.GET.get('category_id')
            start = request.GET.get('start')
            length = request.GET.get('length')
            items = []
            if category_id and start is not None and length:
                category = Category.objects.get(pk=category_id)
                items = [item.to_dict() for item in Item.objects.filter(category=category)[start:length]]
            return HttpResponse(json.dumps(items), content_type='application/json')
        return super(ItemList, self).get(request, *args, **kwargs)


class Links(TemplateView):
    template_name = 'amazon/links.html'


def add_subscriber(request, *args, **kwargs):
    form = SubscriberForm(request.GET)
    if form.is_valid():
        email = form.cleaned_data['email']
        try:
            Subscriber.objects.get(email=email)
            response = {'error': _(u"Vous êtes déjà enregistré.")}
        except Subscriber.DoesNotExist:
            form.save()
            response = {'success': True}
    else:
        response = {'error': _("E-mail invalide.")}
    return HttpResponse(json.dumps(response), content_type='application/json')