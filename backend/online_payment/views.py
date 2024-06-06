import json
from decimal import Decimal
from django.http import HttpRequest, HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from orders.models import Order


@csrf_exempt
@require_POST
def order_payed(request: HttpRequest) -> HttpResponse:
    data: dict = json.loads(request.body)
    data = data.get("object", None)
    print(data)

    if data:
        paid = data.get("paid")
        paid_amount: dict = data.get("amount")
        paid_amount_value = paid_amount.get("value") if paid_amount else 0

        metadata: dict = data.get("metadata")
        order_uuid = metadata.get("order_uuid") if metadata else None
        if order_uuid is None:
            raise ValueError("Order uuid not found")

        status = data.get("status")

        print("paid", paid)
        print("paid_amout", paid_amount)
        print("metadata", metadata)
        print("status", status)

        if status == "succeeded":
            order = Order.objects.get(uuid=order_uuid)
            order.paid_online = True
            order.paid_online_amount = Decimal(paid_amount_value)
            order.save()

            print("Заказ успешно оплачен онлайн")
