from django.contrib import admin

from .models import ProductPromotion, PromotionCategory, PromoAction


@admin.register(ProductPromotion)
class ProductPromotionAdmin(admin.ModelAdmin):
    pass


@admin.register(PromotionCategory)
class PromotionCategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(PromoAction)
class PromoActionAdmin(admin.ModelAdmin):
    pass
