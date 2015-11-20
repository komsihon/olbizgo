# -*- coding: utf-8 -*-
import json
from django.conf import settings
import cms.models
from django.core.management import call_command
from django.core.urlresolvers import reverse
from django.test.client import Client
from django.test.utils import override_settings
from django.utils import unittest


class CMSTestCase(unittest.TestCase):
    fixtures = ['flat_pages.yaml']

    def setUp(self):
        self.client = Client()
        for fixture in self.fixtures:
            call_command('loaddata', fixture)

    def tearDown(self):
        for name in ('FlatPage', 'Config'):
            model = getattr(cms.models, name)
            for model in model.objects.all():
                model.delete()

    def test_FlatPageView_with_valid_page(self):
        response = self.client.get(reverse('flat_page', args=('mentions-legales',)))
        self.assertEqual(response.status_code, 200)

    def test_FlatPageView_with_unexisting_page(self):
        response = self.client.get(reverse('flat_page', args=('unexisting',)))
        self.assertEqual(response.status_code, 404)
