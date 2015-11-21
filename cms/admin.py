from cms.models import FlatPage, Config
from django.contrib import admin


class FlatPageAdmin(admin.ModelAdmin):
    list_display = ('title_fr', )
    prepopulated_fields = {"slug": ("title_fr",)}

admin.site.register(Config)
admin.site.register(FlatPage, FlatPageAdmin)
