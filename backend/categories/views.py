from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

from .models import Category
from cart.forms import SimpleCartAddProductForm


def get_category(
    request: HttpRequest,
    slug: str,
) -> HttpResponse:
    category = Category.objects.get(slug=slug)
    products = category.products.all()

    return render(
        request,
        "categories/category.html",
        context={
            "category": category,
            "products": products,
            "current_category": category.name,
            "cart_add_product_form": SimpleCartAddProductForm(),
        },
    )
