import sys
from pathlib import Path
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpRequest, HttpResponse
from django.contrib import messages

ROOT_DIR = Path(__file__).parent.parent
sys.path.append(str(ROOT_DIR))

from orders.forms import OrderCreateForm
from orders.models import Order, OrderItem
from accounts.models import CustomUser
from accounts.messages import LOGIN_LEVEL
from cart.cart import Cart


def order_confirm(request: HttpRequest) -> HttpResponse:
    user: CustomUser = request.user
    cart = Cart(request)

    if not user.is_authenticated:
        messages.add_message(
            request,
            LOGIN_LEVEL,
            "Для оформления заказа требуется авторизация",
        )
        return redirect("accounts:account_login")

    if request.method == "POST":
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            cleaned = form.cleaned_data

            order = Order.objects.create(
                account=user,
                phone=cleaned["phone"],
                first_name=cleaned["first_name"],
                last_name=cleaned["last_name"],
                address=cleaned["address"],
                delivery=cleaned["delivery"],
                payment=cleaned["payment"],
                client_comment=cleaned["client_comment"],
            )

            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    unit=item.unit,
                    price=item.unit.get_price(),
                    quantity=item.quantity,
                )

            cart.clear()
            return redirect("orders:order_list")

        else:
            return HttpResponse("Форма не валидна")

    if cart.empty:
        return redirect("cart:cart_details")

    order_form = OrderCreateForm(
        initial={
            "phone": user.phone,
            "first_name": user.first_name,
            "last_name": user.last_name,
        }
    )

    return render(
        request,
        "orders/order_confirm.html",
        context={
            "cart": cart,
            "order_form": order_form,
        },
    )


def order_list(request: HttpRequest) -> HttpResponse:
    user: CustomUser = request.user
    if not user.is_authenticated:
        messages.add_message(
            request,
            LOGIN_LEVEL,
            "Для просмотра заказов требуется авторизация",
        )
        return redirect("accounts:account_login")

    orders = user.orders.all()
    return render(
        request,
        "orders/order_list.html",
        context={"orders": orders},
    )


def order_detail(request: HttpRequest, uuid: str) -> HttpResponse:
    order = get_object_or_404(Order, uuid=uuid)
    items = order.items.all()

    return render(
        request,
        "orders/order_detail.html",
        context={
            "order": order,
            "items": items,
        },
    )
