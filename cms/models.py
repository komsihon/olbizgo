# -*- coding: utf-8 -*-
from django.db import models
from django.template.defaultfilters import slugify
from django.utils import translation
from django.utils.translation import gettext as _


class MultiLingualTitle():
    """
    Title fields are not defined here because the may have different properties
    in the sub-models, so only the methods are defined.
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


class Config(models.Model):
    facebook_link = models.CharField(max_length=150,
                                     help_text=u"Lien Facebook Olbizgo.")
    twitter_link = models.CharField(max_length=150,
                                    help_text=u"Lien Twitter Olbizgo.")
    google_plus_link = models.CharField(max_length=150,
                                        help_text=u"Lien Google+ Olbizgo.")
    address = models.CharField(max_length=180,
                               help_text=u"Adresse de Olbizgo (Apparaît en bas de page à droite).")
    contact_phone = models.CharField(max_length=18,
                                     help_text=u"Numéro de téléphone de Olbizgo (Apparaît en bas de page à droite).")
    contact_email = models.CharField(max_length=60,
                                     help_text=u"E-mail de contact de Olbizgo (Apparaît en bas de page à droite).")
    about_text_fr = models.TextField(help_text=u"Text en français de demande d'inscription à la about (255 caractères max).")
    about_text_en = models.TextField(blank=True,
                                     help_text=u"Text en anglais de demande d'inscription à la about (255 caractères max).")
    about_text_de = models.TextField(blank=True,
                                     help_text=u"Text en allemand de demande d'inscription à la about (255 caractères max).")
    legal_mentions_page = models.ForeignKey('FlatPage',
                                            help_text=u"La page contenant les mentions légales du site.")

    def __unicode__(self):
        return u"Configurations gérérales du site."

    def get_raw_contact_phone(self):
        return slugify(self.contact_phone).replace('-', '')

    def _get_about_text(self):
        lang = translation.get_language()
        if lang.lower().find('en') == 0 and self.about_text_en:
            return self.about_text_en
        if lang.lower().find('de') == 0 and self.about_text_de:
            return self.about_text_de
        else:
            return self.about_text_fr
    about_text = property(_get_about_text)


class FlatPage(models.Model, MultiLingualTitle):
    title_fr = models.CharField(max_length=100,
                                help_text=u"Titre en français de la page.")
    title_en = models.CharField(max_length=100, blank=True,
                                help_text=u"Titre en anglais de la page.")
    title_de = models.CharField(max_length=100, blank=True,
                                help_text=u"Titre en allemand de la page.")
    slug = models.SlugField(unique=True,
                            help_text=u"Donnée remplie automatiquement.")
    url = models.URLField(blank=True,
                          help_text=u"S'il s'agit d'une page qui mène vers un lien externe, mettez le lien complet ici."
                                    u"Ex: http://www.ikwen.com/blog/")
    content_fr = models.TextField(blank=True,
                                  help_text=u"Contenu en français de la page. Le contenu HTML est autorisé. Utilisez"
                                            u"TinyMCE pour créer votre contenu HTML, puis copiez et collez le code ici.")
    content_en = models.TextField(blank=True,
                                  help_text=u"Contenu en anglais de la page.")
    content_de = models.TextField(blank=True,
                                  help_text=u"Contenu en allemand de la page.")
    # show_banner = models.BooleanField(default=False)
    # banner = models.FileField(upload_to='cms/flat_page_banners', blank=True)
    # show_in_footer = models.BooleanField(default=True)

    def __unicode__(self):
        return self.title

    def _get_content(self):
        lang = translation.get_language()
        if lang.lower().find('en') == 0 and self.content_en:
            return self.content_en
        elif lang.lower().find('de') == 0 and self.content_de:
            return self.content_de
        else:
            return self.content_fr
    content = property(_get_content)