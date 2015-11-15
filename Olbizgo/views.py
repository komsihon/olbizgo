from django.shortcuts import render
from django.views.generic.base import TemplateView


class Theme(TemplateView):
    template_name = 'theme.html'
