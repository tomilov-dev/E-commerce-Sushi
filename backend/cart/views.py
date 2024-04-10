from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from django.http import HttpRequest, HttpResponse, Http404, JsonResponse
from django.urls import reverse

from products.models import Unit
from .cart import Cart, TotalPrices
from .forms import (
    SimpleCartAddProductForm,
    CartAddProductForm,
    SimpleCartRemoveProductForm,
    SimpleCartDeleteProductForm,
)


def cart_details(request: HttpRequest) -> HttpResponse:
    cart = Cart(request)

    return render(
        request,
        "cart/details.html",
        {
            "cart": cart,
            "cart_add_product_form": SimpleCartAddProductForm(),
            "cart_remove_product_form": SimpleCartRemoveProductForm(),
            "cart_delete_product_form": SimpleCartDeleteProductForm(),
        },
    )


@require_POST
def cart_add(
    request: HttpRequest,
    unit_id: int,
) -> HttpResponse:
    cart = Cart(request)
    unit = get_object_or_404(Unit, id=unit_id)

    form = SimpleCartAddProductForm(request.POST)
    if form.is_valid():
        cleaned = form.cleaned_data
        unit_total_price = cart.add(
            unit=unit,
            quantity=cleaned["quantity"],
            override_quantity=cleaned["override"],
        )
    else:
        raise Http404()

    total_prices: TotalPrices = cart.total_price
    return JsonResponse(
        {
            "added_item": unit.full_name,
            "units_count": cart.units_count,
            "units_count_text": cart.units_count_text,
            "items_price": total_prices.items_price,
            "delivery_price": total_prices.delivery_price,
            "cart_price": total_prices.cart_price,
            "unit_total_price": unit_total_price,
        }
    )


@require_POST
def cart_remove(
    request: HttpRequest,
    unit_id: int,
) -> HttpResponse:
    cart = Cart(request)
    unit = get_object_or_404(Unit, id=unit_id)

    form = SimpleCartRemoveProductForm(request.POST)
    if form.is_valid():
        cleaned = form.cleaned_data
        unit_total_price = cart.remove(unit, cleaned["quantity"])
    else:
        raise Http404()

    total_prices: TotalPrices = cart.total_price
    return JsonResponse(
        {
            "removed_item": unit.full_name,
            "units_count": cart.units_count,
            "units_count_text": cart.units_count_text,
            "items_price": total_prices.items_price,
            "delivery_price": total_prices.delivery_price,
            "cart_price": total_prices.cart_price,
            "unit_total_price": unit_total_price,
        }
    )


@require_POST
def cart_delete(
    request: HttpRequest,
    unit_id: int | str,
) -> HttpResponse:
    cart = Cart(request)
    unit = get_object_or_404(Unit, id=unit_id)

    form = SimpleCartDeleteProductForm(request.POST)
    if form.is_valid():
        cart.delete(unit)
    else:
        raise Http404()

    total_prices: TotalPrices = cart.total_price
    return JsonResponse(
        {
            "deleted_item": unit.full_name,
            "units_count": cart.units_count,
            "units_count_text": cart.units_count_text,
            "items_price": total_prices.items_price,
            "delivery_price": total_prices.delivery_price,
            "cart_price": total_prices.cart_price,
        }
    )
