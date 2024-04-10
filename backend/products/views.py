from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.core.cache import cache

from .models import Product
from cart.forms import SimpleCartAddProductForm, SimpleCartRemoveProductForm
from caching import PRODUCT_KEY, DEFAULT_CACHE_TIME


def get_product(
    request: HttpRequest,
    slug: str,
) -> HttpResponse:
    product_key = f"{PRODUCT_KEY}::{slug}"

    product = cache.get(product_key)
    if not product:
        product = Product.objects.prefetch_related(
            "product_tags__tag",
            "units__characteristics",
            "units__characteristics__measure",
        ).get(slug=slug)
        cache.set(product_key, product, DEFAULT_CACHE_TIME)

    return render(
        request,
        "products/product.html",
        context={
            "product": product,
            "cart_add_product_form": SimpleCartAddProductForm(),
            "cart_remove_product_form": SimpleCartRemoveProductForm(),
        },
    )
