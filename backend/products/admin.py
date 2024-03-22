from django.contrib import admin

from .models import Product, Unit, Measure, Characteristics


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    pass


@admin.register(Measure)
class MeasureAdmin(admin.ModelAdmin):
    pass


@admin.register(Characteristics)
class CharacteristicsAdmin(admin.ModelAdmin):
    pass
