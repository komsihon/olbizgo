# -*- coding: utf-8 -*-
from django.db import models
from django.utils import translation
from django.utils.translation import gettext as _
from ikwen.utils import to_dict


class MultiLingualTitle():
    """
    Title fields are not defined here because the may have different properties
    in the sub-models, so only the methods are defined
    """
    def _get_title(self):
        lang = translation.get_language()
        if lang.lower().find('en') == 0 and self.title_en:
            return self.title_en
        if lang.lower().find('de') == 0 and self.title_de:
            return self.title_de
        else:
            return self.title_fr
    title = property(_get_title)


class Dimension(models.Model):
    width = models.PositiveSmallIntegerField(help_text=_(u"Largeur en pixels"))
    height = models.PositiveSmallIntegerField(help_text=_(u"Hauteur en pixels"))

    class Meta:
        verbose_name_plural = _(u"Différentes dimensions fournies par Amazon")


class Category(models.Model, MultiLingualTitle):
    title_fr = models.CharField(max_length=100,
                                help_text=_(u"Titre en français de la catégorie"))
    title_en = models.CharField(max_length=100, blank=True,
                                help_text=_(u"Titre en anglais de la catégorie"))
    title_de = models.CharField(max_length=100, blank=True,
                                help_text=_(u"Titre en allemand de la catégorie"))
    icon = models.ImageField(blank=True, width_field=27, height_field=27,
                             help_text=_(u"Icône d'illustration: 27px X 27px"))
    slug = models.SlugField(max_length=100, unique=True, blank=True,
                            help_text=_(u"Donnée remplie automatiquement"))
    description = models.CharField(max_length=100, blank=True,
                                   help_text=_(u"Petite description de la catégorie"))
    items_count = models.PositiveIntegerField(default=0,
                                              help_text=_(u"Nombre d'éléments dans cette catégorie"))
    appear_in_main = models.BooleanField(default=False,
                                         help_text=_(u"Cocher pour mettre en évidence dans la liste des catégories"))
    order_of_appearance = models.SmallIntegerField(default=1000,
                                                   help_text=_(u"Ordre d'apparition dans la liste des catégories"))
    visible = models.BooleanField(default=True, blank=True,
                                  help_text=_(u"Cocher/Décocher pour rendre visible/invisible sur le site"))
    items_dimension = models.ForeignKey(Dimension, blank=True, null=True, editable=False,
                                        help_text=_(u"Dimensions à utiliser lors de l'affichage des produits de cette catégorie"))

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
        verbose_name_plural = _(u"Catégories")


class Item(models.Model, MultiLingualTitle):
    title_fr = models.CharField(max_length=100,
                                help_text=_(u"Intitulé en français du produit"))
    title_en = models.CharField(max_length=100, blank=True,
                                help_text=_(u"Intitulé en anglais du produit"))
    title_de = models.CharField(max_length=100, blank=True,
                                help_text=_(u"Intitulé en allemand du produit"))
    slug = models.SlugField(max_length=100, blank=True,
                            help_text=_(u"Donnée remplie automatiquement"))
    category = models.ForeignKey(Category, help_text=_(u"Catégorie à laquelle appartient ce produit"))
    embed_code = models.TextField(help_text=_(u"Code d'intégration fourni par Amazon"))
    appear_in_slideshow = models.BooleanField(default=False,
                                              help_text=_(u"Cocher/Décocher pour insérer/retirer dans le Slideshow de la page d'accueil"))

    class Meta:
        verbose_name_plural = _(u"Produits Amazon")

