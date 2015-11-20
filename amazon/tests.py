# -*- coding: utf-8 -*-
import json
from django.conf import settings
import amazon.models
from django.core.management import call_command
from django.core.urlresolvers import reverse
from django.test.client import Client
from django.test.utils import override_settings
from django.utils import unittest
import MySQLdb
from amazon.models import *


class AmazonTestCase(unittest.TestCase):
    fixtures = ['categories.yaml', 'items.yaml']

    def setUp(self):
        self.client = Client()
        for fixture in self.fixtures:
            call_command('loaddata', fixture)

    def tearDown(self):
        for name in ('Item', 'Category', 'Subscriber'):
            model = getattr(amazon.models, name)
            for model in model.objects.all():
                model.delete()

    def test_Home(self):
        response = self.client.get(reverse('amazon:home'))
        self.assertEqual(response.status_code, 200)

    def test_ListItem(self):
        response = self.client.get(reverse('amazon:item_list', args=('jeux-videos', )))
        self.assertEqual(response.status_code, 200)
        self.assertIn('text/html', response['Content-Type'])

    @override_settings(POMMO_DATABASE=('localhost', 'root', '', 'test_Olbizgo_poMMo'))
    def test_add_subscriber_with_valid_email(self):
        """
        add_subscriber should add one more subscriber to list and copy it to the poMMo MySQL database
        """
        db = getattr(settings, 'POMMO_DATABASE')
        with MySQLdb.connect(db[0], db[1], db[2], 'mysql') as cursor:
            # cursor = cnx.cursor()
            cursor.execute("DROP DATABASE IF EXISTS test_Olbizgo_poMMo")
            cursor.execute("CREATE DATABASE test_Olbizgo_poMMo")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS test_Olbizgo_poMMo.`subscribers` (
                  `subscriber_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
                  `email` char(60) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
                  `time_touched` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                  `time_registered` datetime NOT NULL,
                  `flag` tinyint(1) NOT NULL DEFAULT '0' COMMENT '0: NULL, 1-8: REMOVE, 9: UPDATE',
                  `ip` int(10) unsigned DEFAULT NULL COMMENT 'Stored with INET_ATON(), Fetched with INET_NTOA()',
                  `status` tinyint(1) NOT NULL DEFAULT '2' COMMENT '0: Inactive, 1: Active, 2: Pending',
                  PRIMARY KEY (`subscriber_id`),
                  KEY `status` (`status`,`subscriber_id`),
                  KEY `status_2` (`status`,`email`),
                  KEY `status_3` (`status`,`time_touched`),
                  KEY `status_4` (`status`,`time_registered`),
                  KEY `status_5` (`status`,`ip`),
                  KEY `flag` (`flag`)
                ) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
            """)
            email = 'subscriber@newsletter.com'
            response = self.client.get(reverse('amazon:add_subscriber'), {'email': email})

            cursor.execute("SELECT * FROM test_Olbizgo_poMMo.subscribers LIMIT 1")
            result_set = cursor.fetchall()
            row = result_set[0]
            self.assertEqual(row[1], email)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.content, json.dumps({'success': True}))
            cursor.execute("DROP DATABASE test_Olbizgo_poMMo")

    def test_add_subscriber_with_invalid_email(self):
        """
        add_subscriber with invalid email should return JSON {'error': 'Invalid e-mail'}
        """
        email = 'invalid@email'
        response = self.client.get(reverse('amazon:add_subscriber'), {'email': email})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, json.dumps({'error': 'E-mail invalide.'}))

    def test_Item_get_href(self):
        """
        Item.get_href must return only the href from the Item.embed_code
        """
        item = Item(embed_code='<a rel="nofollow" href="http://www.amazon.fr/gp/product/B00WMEJX0A/ref=as_li_tl?ie=UTF8&camp=1642&creative=6746&creativeASIN=B00WMEJX0A&linkCode=as2&tag=olbizgocom090-21"><img border="0" src="http://ws-eu.amazon-adsystem.com/widgets/q?_encoding=UTF8&ASIN=B00WMEJX0A&Format=_SL160_&ID=AsinImage&MarketPlace=FR&ServiceVersion=20070822&WS=1&tag=olbizgocom090-21" ></a><img src="http://ir-fr.amazon-adsystem.com/e/ir?t=olbizgocom090-21&l=as2&o=8&a=B00WMEJX0A" width="1" height="1" border="0" alt="" style="border:none !important; margin:0px !important;" />')
        self.assertEqual(item.get_href(), 'http://www.amazon.fr/gp/product/B00WMEJX0A/ref=as_li_tl?ie=UTF8&camp=1642&creative=6746&creativeASIN=B00WMEJX0A&linkCode=as2&tag=olbizgocom090-21')

    def test_Item_get_embed_code(self):
        """
        Item.get_embed_code must correctly replace the image dimensions inside the embed_code return only the href from the Item.embed_code
        """
        item = Item(embed_code='<a rel="nofollow" href="http://www.amazon.fr/gp/product/B00WMEJX0A/ref=as_li_tl?ie=UTF8&camp=1642&creative=6746&creativeASIN=B00WMEJX0A&linkCode=as2&tag=olbizgocom090-21"><img border="0" src="http://ws-eu.amazon-adsystem.com/widgets/q?_encoding=UTF8&ASIN=B00WMEJX0A&Format=_SL160_&ID=AsinImage&MarketPlace=FR&ServiceVersion=20070822&WS=1&tag=olbizgocom090-21" ></a><img src="http://ir-fr.amazon-adsystem.com/e/ir?t=olbizgocom090-21&l=as2&o=8&a=B00WMEJX0A" width="1" height="1" border="0" alt="" style="border:none !important; margin:0px !important;" />')
        self.assertEqual(item.get_embed_code(Item.SMALL),
                         '<a rel="nofollow" href="http://www.amazon.fr/gp/product/B00WMEJX0A/ref=as_li_tl?ie=UTF8&camp=1642&creative=6746&creativeASIN=B00WMEJX0A&linkCode=as2&tag=olbizgocom090-21"><img border="0" src="http://ws-eu.amazon-adsystem.com/widgets/q?_encoding=UTF8&ASIN=B00WMEJX0A&Format=_SL110_&ID=AsinImage&MarketPlace=FR&ServiceVersion=20070822&WS=1&tag=olbizgocom090-21" ></a><img src="http://ir-fr.amazon-adsystem.com/e/ir?t=olbizgocom090-21&l=as2&o=8&a=B00WMEJX0A" width="1" height="1" border="0" alt="" style="border:none !important; margin:0px !important;" />')
        self.assertEqual(item.get_embed_code(Item.MEDIUM),
                         '<a rel="nofollow" href="http://www.amazon.fr/gp/product/B00WMEJX0A/ref=as_li_tl?ie=UTF8&camp=1642&creative=6746&creativeASIN=B00WMEJX0A&linkCode=as2&tag=olbizgocom090-21"><img border="0" src="http://ws-eu.amazon-adsystem.com/widgets/q?_encoding=UTF8&ASIN=B00WMEJX0A&Format=_SL160_&ID=AsinImage&MarketPlace=FR&ServiceVersion=20070822&WS=1&tag=olbizgocom090-21" ></a><img src="http://ir-fr.amazon-adsystem.com/e/ir?t=olbizgocom090-21&l=as2&o=8&a=B00WMEJX0A" width="1" height="1" border="0" alt="" style="border:none !important; margin:0px !important;" />')
        self.assertEqual(item.get_embed_code(Item.BIG),
                         '<a rel="nofollow" href="http://www.amazon.fr/gp/product/B00WMEJX0A/ref=as_li_tl?ie=UTF8&camp=1642&creative=6746&creativeASIN=B00WMEJX0A&linkCode=as2&tag=olbizgocom090-21"><img border="0" src="http://ws-eu.amazon-adsystem.com/widgets/q?_encoding=UTF8&ASIN=B00WMEJX0A&Format=_SL250_&ID=AsinImage&MarketPlace=FR&ServiceVersion=20070822&WS=1&tag=olbizgocom090-21" ></a><img src="http://ir-fr.amazon-adsystem.com/e/ir?t=olbizgocom090-21&l=as2&o=8&a=B00WMEJX0A" width="1" height="1" border="0" alt="" style="border:none !important; margin:0px !important;" />')

    def test_ItemList_with_json(self):
        """
        ItemList must return a list of Item in JSON format when queried with the format=json GET parameter
        """
        response = self.client.get(reverse('amazon:item_list'), {'category_id': '55fd77feb37b330f4fc7a6b4', 'start': 0, 'length': 10, 'format': 'json'})
        self.assertEqual(response.status_code, 200)
        json_content = json.loads(response.content)
        self.assertEqual(len(json_content), 2)
