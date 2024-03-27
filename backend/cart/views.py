import re

from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from django.http import HttpRequest, HttpResponse, Http404, JsonResponse
from django.urls import reverse

from products.models import Unit
from .cart import Cart, CartItem
from .forms import SimpleCartAddProductForm, CartAddProductForm

REFERER_URL = re.compile(pattern=r"https?://.*?/(.*)", flags=re.IGNORECASE)


def get_redirect_url(request: HttpRequest, product: Unit) -> str:
    ct_url = reverse("products:category", args=[product.category.slug])
    sp_url = ""
    if product.special_category:
        sp_url = reverse("products:special", args=[product.special_category.slug])

    redirect_to = ""
    referer = request.META.get("HTTP_REFERER", None)
    if referer:
        referer = "/" + REFERER_URL.findall(referer)[0]

        if sp_url == referer:
            redirect_to = sp_url
        else:
            redirect_to = ct_url

    else:
        redirect_to = ct_url

    return redirect_to


def cart_details(request: HttpRequest) -> HttpResponse:
    cart = Cart(request)
    return render(
        request,
        "cart/details.html",
        {"cart": cart},
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
        cart.add(
            unit=unit,
            quantity=cleaned["quantity"],
            override_quantity=cleaned["override"],
        )
    else:
        raise Http404()

    return JsonResponse(
        {
            "added_item": unit.full_name,
            "cart_items": cart.units_count,
        }
    )


@require_POST
def cart_update(
    request: HttpRequest,
    unit_id: int,
) -> HttpResponse:
    cart = Cart(request)
    unit = get_object_or_404(Unit, id=unit_id)

    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cleaned = form.cleaned_data
        cart.add(
            unit=unit,
            quantity=cleaned["quantity"],
            override_quantity=cleaned["override"],
        )

    # return redirect("cart:cart_details")
    return HttpResponse("Updated")


@require_POST
def cart_remove(
    request: HttpRequest,
    unit_id: int,
) -> HttpResponse:
    cart = Cart(request)
    unit = get_object_or_404(Unit, id=unit_id)

    cart.remove(unit)
    # return redirect("cart:cart_details")
    return HttpResponse("Removed")
