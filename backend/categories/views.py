import sys
from pathlib import Path
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.core.cache import cache

ROOT_DIR = Path(__file__).parent.parent
print(ROOT_DIR)
sys.path.append(str(ROOT_DIR))

from categories.models import Category
from cart.forms import SimpleCartAddProductForm, SimpleCartRemoveProductForm
from caching import CATEGORY_KEY, DEFAULT_CACHE_TIME


def get_category(
    request: HttpRequest,
    slug: str,
) -> HttpResponse:
    category_key = f"{CATEGORY_KEY}::{slug}"

    category = cache.get(category_key)
    if not category:
        category = Category.objects.prefetch_related(
            "products",
            "products__units__characteristics__measure",
            "products__product_tags__tag",
        ).get(slug=slug)
        cache.set(category_key, category, DEFAULT_CACHE_TIME)

    return render(
        request,
        "categories/category.html",
        context={
            "category": category,
            "cart_add_product_form": SimpleCartAddProductForm(),
            "cart_remove_product_form": SimpleCartRemoveProductForm(),
        },
    )
