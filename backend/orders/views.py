import sys
from pathlib import Path
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.contrib import messages

ROOT_DIR = Path(__file__).parent.parent
sys.path.append(str(ROOT_DIR))

from orders.forms import OrderCreateForm
from orders.models import Order, OrderItem
from accounts.models import CustomUser
from accounts.messages import LOGIN_LEVEL
from cart.cart import Cart
from online_payment.payment import yookassa_payment


def order_confirm(request: HttpRequest) -> HttpResponse:
    errors = []
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
                total_cost=cart.total_price.cart_price,
            )

            for item, unit in cart.objects:
                OrderItem.objects.create(
                    order=order,
                    unit=unit,
                    price=unit.get_price(),
                    quantity=item.quantity,
                )

            redir_link = "orders:order_list"
            if order.payment == Order.Payment.ONLINE:
                payment = yookassa_payment.online_payment(order)

                confirmation = payment.confirmation
                confirmation_url = confirmation.confirmation_url

                redir_link = confirmation_url

            cart.clear()
            return redirect(redir_link)

        else:
            errors.extend(form.errors.values())

    if cart.empty:
        return redirect("cart:cart_details")

    order_form = OrderCreateForm(
        initial={
            "phone": "8" + user.phone,
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
            "errors": errors,
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

    orders: list[Order] = user.orders.order_by("-created")[:18]
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


def unprocessed_orders_count(request: HttpRequest) -> HttpResponse:
    count = Order.objects.filter(status=Order.Status.PENDING).count()
    return JsonResponse({"count": count})
