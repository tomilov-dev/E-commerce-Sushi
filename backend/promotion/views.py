from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

from .models import PromotionCategory, ProductPromotion, PromoAction
from cart.forms import SimpleCartAddProductForm


def promotion_list(request: HttpRequest) -> HttpResponse:
    promo_actions = PromoAction.objects.all()
    return render(
        request,
        "promotion/promotion_list.html",
        context={"promo_actions": promo_actions},
    )


def get_promotion_category(
    request: HttpRequest,
    slug: str,
) -> HttpResponse:
    promotion_category = PromotionCategory.objects.get(slug=slug)
    products_promotions: ProductPromotion = promotion_category.product_promotions.all()
    products = [pp.product for pp in products_promotions]

    return render(
        request,
        "promotion/promotion_category.html",
        context={
            "category": promotion_category,
            "products": products,
            "current_category": promotion_category.name,
            "cart_add_product_form": SimpleCartAddProductForm(),
        },
    )


def get_promo_action(
    request: HttpRequest,
    slug: str,
) -> HttpResponse:
    promo_action = PromoAction.objects.get(slug=slug)
    return render(
        request,
        "promotion/promotion_action.html",
        context={
            "promo_action": promo_action,
        },
    )
