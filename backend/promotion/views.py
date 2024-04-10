import sys
from pathlib import Path
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.core.cache import cache

ROOT_DIR = Path(__file__).parent.parent
sys.path.append(str(ROOT_DIR))

from promotion.models import PromotionCategory, ProductPromotion, PromoAction
from cart.forms import SimpleCartAddProductForm, SimpleCartRemoveProductForm
from caching import PROMOTION_KEY, PROMOTION_CATEGORY_KEY, DEFAULT_CACHE_TIME


def promotion_list(request: HttpRequest) -> HttpResponse:
    ## using promotion context
    return render(
        request,
        "promotion/promotion_list.html",
    )


def get_promotion_category(
    request: HttpRequest,
    slug: str,
) -> HttpResponse:
    promotion_category_key = f"{PROMOTION_CATEGORY_KEY}::{slug}"

    promotion_category = cache.get(promotion_category_key)
    if not promotion_category:
        promotion_category = PromotionCategory.objects.prefetch_related(
            "promotion_category__product__units__characteristics__measure",
            "promotion_category__product__product_tags__tag",
        ).get(slug=slug)
        cache.set(promotion_category_key, promotion_category, DEFAULT_CACHE_TIME)

    products_promotions: ProductPromotion = promotion_category.promotion_category.all()
    products = [pp.product for pp in products_promotions]

    return render(
        request,
        "promotion/promotion_category.html",
        context={
            "category": promotion_category,
            "products": products,
            "cart_add_product_form": SimpleCartAddProductForm(),
            "cart_remove_product_form": SimpleCartRemoveProductForm(),
        },
    )


def get_promo_action(
    request: HttpRequest,
    slug: str,
) -> HttpResponse:
    promotion_key = f"{PROMOTION_KEY}::{slug}"

    promo_action = cache.get(promotion_key)
    if not promo_action:
        promo_action = PromoAction.objects.get(slug=slug)
        cache.set(promotion_key, promo_action, DEFAULT_CACHE_TIME)

    return render(
        request,
        "promotion/promotion_action.html",
        context={
            "promo_action": promo_action,
        },
    )
