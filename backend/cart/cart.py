from decimal import Decimal
from typing import Generator, Any
from django.conf import settings
from django.http import HttpRequest
from django.shortcuts import get_object_or_404

from products.models import Unit


CART_SESSION_ID = settings.CART_SESSION_ID


class CartItem(object):
    def __init__(
        self,
        name: str,
        price: int,
        quantity: int,
    ) -> None:
        self.name = name
        self.price = price
        self.quantity = quantity
        self.total_price = price * quantity


class Cart(object):
    def __init__(
        self,
        request: HttpRequest,
    ) -> None:
        self.session = request.session
        cart = self.session.get(CART_SESSION_ID)

        if not cart:
            cart = self.session[CART_SESSION_ID] = {}

        self.cart = cart

    def save(self) -> None:
        self.session.modified = True

    def add(
        self,
        unit: Unit,
        quantity: int = 1,
        override_quantity: bool = False,
    ) -> None:
        unit_id = str(unit.id)
        if unit_id not in self.cart:
            self.cart[unit_id] = 0

        if override_quantity:
            self.cart[unit_id] = quantity
        else:
            self.cart[unit_id] += quantity

        self.save()

    def remove(self, unit: Unit) -> None:
        unit_id = str(unit.id)
        if unit_id in self.cart:
            del self.cart[unit_id]
            self.save()

    def clear(self) -> None:
        del self.session[CART_SESSION_ID]
        self.save()

    @property
    def empty(self) -> bool:
        return self.__len__() == 0

    @property
    def units_count(self) -> int:
        count = 0
        for unit_id in self.cart:
            count += self.cart[unit_id]
        return count

    def __iter__(self) -> Generator[CartItem, Any, Any]:
        units_ids = self.cart.keys()

        for unit_id in units_ids:
            quantity = self.cart[unit_id]
            unit = get_object_or_404(Unit, id=unit_id)

            yield CartItem(
                unit.full_name,
                Decimal(unit.price),
                Decimal(quantity),
            )

        # cart = self.cart.copy()
        # for unit in units:
        #     cart[str(unit.id)]["unit"] = unit

        # for item in cart.values():
        #     item["price"] = Decimal(item["price"])
        #     item["total_price"] = item["price"] * item["quantity"]
        #     yield item

    def __len__(self) -> int:
        return self.units_count
