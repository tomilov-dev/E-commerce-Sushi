from django.contrib import admin

from .models import Tag, ProductTag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(ProductTag)
class ProductTagAdmin(admin.ModelAdmin):
    pass
