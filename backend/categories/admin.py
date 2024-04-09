from django.contrib import admin

from .models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    fields = [
        "name",
        "slug",
        "priority",
        "description",
        "available",
        "show_navbar",
        "image",
        "icon",
    ]
    list_display = ["name", "show_navbar", "priority", "available"]
    list_editable = ["show_navbar", "priority", "available"]

    prepopulated_fields = {"slug": ("name",)}
