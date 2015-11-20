# -*- coding: utf-8 -*-
from amazon.models import Category, Item, Subscriber, AmazonConfig
from django.contrib import admin
from import_export.admin import ImportExportMixin


class AmazonConfigAdmin(admin.ModelAdmin):
    list_display = ('slideshow_visible', 'slideshow_background', 'item_border', )


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title_fr', 'order_of_appearance', 'items_count', 'appear_in_main', 'visible', )
    ordering = ('order_of_appearance', 'title_fr', )
    search_fields = ('title_fr', )
    prepopulated_fields = {"slug": ("title_fr",)}
    readonly_fields = ('items_count', )


class ItemAdmin(admin.ModelAdmin):
    list_display = ('title_fr', 'category', 'appear_in_slideshow', )
    ordering = ('title_fr', )
    search_fields = ('title_fr', )
    prepopulated_fields = {"slug": ("title_fr",)}
    list_filter = ('category', 'appear_in_slideshow', )


class SubscriberAdmin(admin.ModelAdmin, ImportExportMixin):
    list_display = ('email', 'date_joined', )
    list_filter = ('date_joined', )


admin.site.register(AmazonConfig, AmazonConfigAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Subscriber, SubscriberAdmin)