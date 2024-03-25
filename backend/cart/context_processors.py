from django.http import HttpRequest

from .cart import Cart


def cart_context(request: HttpRequest):
    return {
        "cart": Cart(request),
    }
