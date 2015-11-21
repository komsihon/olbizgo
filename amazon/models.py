# -*- coding: utf-8 -*-
import MySQLdb
from cms.models import MultiLingualTitle
from django.conf import settings
from django.utils import timezone
from django.db import models
from django.utils import translation
from ikwen.utils import to_dict


class AmazonConfig(models.Model):
    NONE = 'none'
    BLACK = 'dark'
    SLIDESHOW_BACKGROUND_CHOICES = (
        (NONE, "Aucun"),
        (BLACK, "Noir"),
    )
    item_border = models.BooleanField(default=True, help_text=u"Cocher/Décocher pour mettre/retirer une bordure sur les produits.")
    slideshow_visible = models.BooleanField(default=True,
                                            help_text=u"Cocher/Décocher pour rendre le slideshow visible/invisible."
                                                        u" NB: Il n'apparaîtra que s'il contient au moins 5 éléments.")
    slideshow_background = models.CharField(max_length=30, default=BLACK, choices=SLIDESHOW_BACKGROUND_CHOICES,
                                            help_text=u"Couleur d'arrière plan du slideshow de la page d'accueil.")
    newsletter_text_fr = models.CharField(max_length=255,
                                          help_text=u"Text en français de demande d'inscription à la newsletter (255 caractères max).")
    newsletter_text_en = models.CharField(max_length=255, blank=True,
                                          help_text=u"Text en anglais de demande d'inscription à la newsletter (255 caractères max).")
    newsletter_text_de = models.CharField(max_length=255, blank=True,
                                          help_text=u"Text en allemand de demande d'inscription à la newsletter (255 caractères max).")
    adsense_slideshow = models.TextField(blank=True,
                                         help_text=u"Code du Adsense qui apparaît en dessous du Slideshow"
                                                   u" à la page d'accueil. (728 x 90px)")
    adsense_categories = models.TextField(blank=True,
                                          help_text=u"Code du Adsense qui apparaît en dessous des catégories"
                                                    u" à la page d'accueil. (225 x 320px)")
    adsense_item_list = models.TextField(blank=True,
                                         help_text=u"Code du Adsense qui apparaît sur la page de listing des produits"
                                                   u"d'une catégorie. (120 x 320px)")

    def __unicode__(self):
        return u"Configuration de la boutique"

    class Meta:
        verbose_name_plural = u"Configurations de la boutique"

    def _get_newsletter_text(self):
        lang = translation.get_language()
        if lang.lower().find('en') == 0 and self.newsletter_text_en:
            return self.newsletter_text_en
        if lang.lower().find('de') == 0 and self.newsletter_text_de:
            return self.newsletter_text_de
        else:
            return self.newsletter_text_fr
    newsletter_text = property(_get_newsletter_text)


class Item(models.Model, MultiLingualTitle):
    SMALL = 'small'
    MEDIUM = 'medium'
    BIG = 'big'

    BUTTON_DEFAULT = 'default'
    BUTTON_CONFIRM = 'confirm'
    BUTTON_SPECIAL = 'special'
    BUTTON_STYLE_CHOICES = (
        (BUTTON_DEFAULT, u"Bouton par défaut"),
        (BUTTON_CONFIRM, u"Bouton de confirmation"),
        (BUTTON_SPECIAL, u"Bouton spécial"),
    )

    title_fr = models.CharField(max_length=100,
                                help_text=u"Intitulé en français du produit.")
    title_en = models.CharField(max_length=100, blank=True,
                                help_text=u"Intitulé en anglais du produit.")
    title_de = models.CharField(max_length=100, blank=True,
                                help_text=u"Intitulé en allemand du produit.")
    slug = models.SlugField(help_text=u"Donnée remplie automatiquement.")
    button_text_fr = models.CharField(max_length=30, default="Acheter",
                                      help_text=u"Texte du bouton en français.")
    button_text_en = models.CharField(max_length=30, default="Buy now",
                                      help_text=u"Texte du bouton en anglais.")
    button_text_de = models.CharField(max_length=30, blank=True, default="Kaufen",
                                      help_text=u"Texte du bouton en allemand.")
    button_style = models.CharField(max_length=30, default=BUTTON_CONFIRM, choices=BUTTON_STYLE_CHOICES,
                                    help_text=u"Apparence du bouton. Regarder l'aperçu sur http://olbizgo.com/theme")
    category = models.ForeignKey('Category', help_text=u"Catégorie à laquelle appartient ce produit.")
    embed_code = models.TextField(unique=True,
                                  help_text=u"Code d'intégration fourni par Amazon.")
    appear_in_slideshow = models.BooleanField(default=False,
                                              help_text=u"Cocher/Décocher pour insérer/retirer dans le Slideshow de la page d'accueil.")

    class Meta:
        verbose_name_plural = u"Produits Amazon"

    def save(self, *args, **kwargs):
        self.embed_code = self.embed_code.strip()
        super(Item, self).save(*args, **kwargs)
        self.category.items_count += 1
        self.category.save()

    def _get_button_text(self):
        lang = translation.get_language()
        if lang.lower().find('en') == 0 and self.button_text_en:
            return self.button_text_en
        if lang.lower().find('de') == 0 and self.button_text_de:
            return self.button_text_de
        else:
            return self.button_text_fr
    button_text = property(_get_button_text)

    def get_embed_code(self, format):
        """
        Get the embed code with the specified image format (BIG, MEDIUM or SMALL)
        :param format:
        :return:
        """
        if format == Item.BIG:
            return self.embed_code.replace('_SL160_', '_SL250_').replace('_SL110_', '_SL250_')
        if format == Item.MEDIUM:
            return self.embed_code.replace('_SL250_', '_SL160_').replace('_SL110_', '_SL160_')
        if format == Item.SMALL:
            return self.embed_code.replace('_SL250_', '_SL110_').replace('_SL160_', '_SL110_')
        raise ValueError("Invalid embed code. Must be either %s, %s or %s" % (Item.BIG, Item.MEDIUM, Item.SMALL))

    def get_href(self):
        """
        Get the Amazon target from the embed code
        :return:
        """
        self.embed_code = self.embed_code.strip()
        e = self.embed_code.find('>', 1) - 1
        s = self.embed_code.rfind('"', 1, e) + 1
        return self.embed_code[s:e]

    def to_dict(self):
        embed_code = self.get_embed_code(self.category.items_size)
        var = to_dict(self)
        var['embed_code'] = embed_code
        var['button_text'] = self.button_text
        var['href'] = self.get_href()
        var['title'] = self.title
        return var


class Category(models.Model, MultiLingualTitle):
    SIZE_CHOICES = (
        (Item.SMALL, "Petite (110 x 110px)"),
        (Item.MEDIUM, "Moyenne (160 x 160px)"),
        (Item.BIG, "Grande (250 x 250px)")
    )
    title_fr = models.CharField(max_length=100,
                                help_text=u"Titre en français de la catégorie.")
    title_en = models.CharField(max_length=100, blank=True,
                                help_text=u"Titre en anglais de la catégorie.")
    title_de = models.CharField(max_length=100, blank=True,
                                help_text=u"Titre en allemand de la catégorie.")
    icon = models.ImageField(blank=True, null=True, upload_to='categories_icons',
                             help_text=u"Icône d'illustration: 24px X 24px")
    slug = models.SlugField(unique=True,
                            help_text=u"Donnée remplie automatiquement.")
    home_previews_count = models.PositiveSmallIntegerField(default=8,
                                   help_text=u"Nombre d'éléments de cette catégorie qui apparaissent dans l'aperçu à l'accueil.")
    description = models.CharField(max_length=100, blank=True,
                                   help_text=u"Petite description de la catégorie.")
    items_count = models.PositiveIntegerField(default=0,
                                              help_text=u"Nombre d'éléments dans cette catégorie.")
    appear_in_main = models.BooleanField(default=False,
                                         help_text=u"Cocher pour mettre en évidence dans la liste des catégories.")
    order_of_appearance = models.SmallIntegerField(default=1000,
                                                   help_text=u"Ordre d'apparition dans la liste des catégories.")
    visible = models.BooleanField(default=True,
                                  help_text=u"Cocher/Décocher pour rendre visible/invisible sur le site.")
    items_size = models.CharField(max_length=30, default=Item.MEDIUM, choices=SIZE_CHOICES,
                                  help_text=u"Dimensions à utiliser lors de l'affichage des produits de cette catégorie.")

    def to_dict(self):
        var = to_dict(self)
        var['title'] = self.title
        del(var['title_fr'])
        del(var['title_en'])
        del(var['title_de'])
        del(var['description'])
        return var

    def __unicode__(self):
        return self.title_fr

    class Meta:
        ordering = ('order_of_appearance', 'title_fr', )
        verbose_name_plural = u"Catégories"


class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    date_joined = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = u"Abonnés Newsletter"

    def save(self, *args, **kwargs):
        super(Subscriber, self).save(*args, **kwargs)
        try:
            db = getattr(settings, 'POMMO_DATABASE')
            with MySQLdb.connect(db[0], db[1], db[2], db[3]) as cnx:
                cnx.execute("INSERT INTO %s.subscribers(email, time_registered) VALUES('%s', NOW())" % (db[3], self.email))
        except:
            pass