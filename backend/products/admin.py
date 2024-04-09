import sys
from pathlib import Path
from django.contrib import admin


ROOT_DIR = Path(__file__).parent.parent
sys.path.append(str(ROOT_DIR))

from products.models import Product, Unit, Measure, Characteristics
from tags.models import ProductTag
from promotion.models import ProductPromotion, PromoAction


class UnitCharcsInline(admin.TabularInline):
    model = Characteristics
    extra = 0
    show_change_link = True
    fields = [
        "unit",
        "quantity",
        "measure",
        "measure_count",
        "proteins",
        "fats",
        "carbohydrates",
        "kilocalories",
    ]


class ProductUnitInline(admin.TabularInline):
    model = Unit
    extra = 0
    show_change_link = True


class ProductTagInline(admin.TabularInline):
    model = ProductTag
    extra = 0


class ProductPromotionInline(admin.TabularInline):
    model = ProductPromotion
    extra = 0


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [
        ProductUnitInline,
        ProductTagInline,
        ProductPromotionInline,
    ]

    fields = ["name", "slug", "category", "priority", "description", "image"]
    list_display = ["name", "priority"]
    list_editable = ["priority"]
    search_fields = ["name"]
    list_filter = ["category"]

    prepopulated_fields = {"slug": ("name",)}


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    inlines = [UnitCharcsInline]

    fields = ["name", "price", "discount_price", "product", "available"]
    list_display = ["__str__", "available"]
    list_editable = ["available"]

    list_filter = ["product__category"]
    search_fields = ["product__name"]


@admin.register(Measure)
class MeasureAdmin(admin.ModelAdmin):
    fields = ["name", "symbol", "display_name"]
    list_display = ["name", "symbol", "display_name"]


@admin.register(Characteristics)
class CharacteristicsAdmin(admin.ModelAdmin):
    fields = [
        "unit",
        "quantity",
        "measure",
        "measure_count",
        "proteins",
        "fats",
        "carbohydrates",
        "kilocalories",
    ]
