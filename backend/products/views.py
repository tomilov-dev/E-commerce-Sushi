from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

from .models import Product
from cart.forms import SimpleCartAddProductForm


def get_product(
    request: HttpRequest,
    slug: str,
) -> HttpResponse:
    product = Product.objects.get(slug=slug)

    print(product.tags)

    return render(
        request,
        "products/product.html",
        context={
            "product": product,
            "cart_add_product_form": SimpleCartAddProductForm(),
        },
    )
