# -*- coding: utf-8 -*-
from amazon.models import Category, Item, Dimension
from django.contrib import admin


class DimensionAdmin(admin.ModelAdmin):
    list_display = ('width', 'height', )
    ordering = ('width', 'height', )


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


# admin.site.register(Dimension, DimensionAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Item, ItemAdmin)