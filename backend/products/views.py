from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

from .models import Product


def get_product(
    request: HttpRequest,
    slug: str,
) -> HttpResponse:
    product = Product.objects.get(slug=slug)
    return render(
        request,
        "products/product.html",
        context={"product": product},
    )
