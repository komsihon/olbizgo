# -*- coding: utf-8 -*-
from amazon.models import Subscriber

__author__ = 'Kom Sihon'

from django import forms


class SubscriberForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ['email']
