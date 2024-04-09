import sys
from pathlib import Path
from django.contrib import admin

ROOT_DIR = Path(__file__).parent.parent
sys.path.append(str(ROOT_DIR))

from promotion.models import ProductPromotion, PromotionCategory, PromoAction
from products.models import Product
from categories.models import Category


@admin.register(PromoAction)
class PromoActionAdmin(admin.ModelAdmin):
    fields = [
        "name",
        "slug",
        "priority",
        "available",
        "straight_redirect",
        "description",
        "image",
        "product",
        "category",
        "promotion_category",
    ]
    list_display = ["name", "priority", "available"]
    list_editable = ["priority", "available"]

    autocomplete_fields = ["product"]
    prepopulated_fields = {"slug": ("name",)}

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "product":
            kwargs["queryset"] = Product.objects.order_by("name")
        elif db_field.name == "category":
            kwargs["queryset"] = Category.objects.order_by("name")
        elif db_field.name == "promotion_category":
            kwargs["queryset"] = PromotionCategory.objects.order_by("name")

        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class ProductPromotionInline(admin.TabularInline):
    model = ProductPromotion
    extra = 1


@admin.register(PromotionCategory)
class PromotionCategoryAdmin(admin.ModelAdmin):
    inlines = [ProductPromotionInline]

    fields = [
        "name",
        "slug",
        "priority",
        "available",
        "show_navbar",
        "description",
        "image",
        "icon",
    ]
    list_display = ["name", "show_navbar", "priority", "available"]
    list_editable = ["show_navbar", "priority", "available"]


@admin.register(ProductPromotion)
class ProductPromotionAdmin(admin.ModelAdmin):
    fields = [
        "product",
        "promotion_category",
    ]
