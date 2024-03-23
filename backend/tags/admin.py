from django.contrib import admin

from .models import Tag, ProductTag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    fields = ["name", "description", "available", "image"]
    list_display = ["name", "available"]
    list_editable = ["available"]


@admin.register(ProductTag)
class ProductTagAdmin(admin.ModelAdmin):
    fields = ["tag", "product"]
    list_display = ["tag", "product"]

    search_fields = ["product__name", "tag__name"]
