from decimal import Decimal
from typing import Generator, Any
from django.conf import settings
from django.http import HttpRequest
from django.shortcuts import get_object_or_404

from products.models import Unit


CART_SESSION_ID = settings.CART_SESSION_ID
DELIVERY_PRICES: dict = settings.DELIVERY_PRICES


class CartItem(object):
    def __init__(
        self,
        name: str,
        price: int,
        quantity: int,
        unit: Unit,
    ) -> None:
        self.name = name
        self.price = price
        self.quantity = quantity
        self.unit = unit
        self.total_price = price * quantity


class TotalPrices(object):
    def __init__(
        self,
        items_price: int,
        delivery_price: int,
        cart_price: int,
    ) -> None:
        self.items_price = int(items_price)
        self.delivery_price = int(delivery_price)
        self.cart_price = int(cart_price)


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

    def unit_total_price(self, unit: Unit) -> int | None:
        unit_id = str(unit.id)
        if self.cart.get(unit_id, None):
            total_unit_price = unit.get_price() * self.cart[unit_id]
            return int(total_unit_price)
        else:
            return None

    def add(
        self,
        unit: Unit,
        quantity: int = 1,
        override_quantity: bool = False,
    ) -> int:
        unit_id = str(unit.id)
        if unit_id not in self.cart:
            self.cart[unit_id] = 0

        if override_quantity:
            self.cart[unit_id] = quantity
        else:
            self.cart[unit_id] += quantity

        self.save()
        return self.unit_total_price(unit)

    def remove(
        self,
        unit: Unit,
        quantity: int = 1,
    ) -> None:
        unit_id = str(unit.id)
        if unit_id in self.cart:
            qic = self.cart[unit_id]
            if qic <= quantity:
                del self.cart[unit_id]
            else:
                self.cart[unit_id] -= quantity

        self.save()
        return self.unit_total_price(unit)

    def delete(self, unit: Unit) -> None:
        unit_id = str(unit.id)
        if unit_id in self.cart:
            del self.cart[unit_id]
        self.save()

    def clear(self) -> None:
        del self.session[CART_SESSION_ID]
        self.save()

    def contains(self, unit_id: str | int) -> bool:
        unit_id = str(unit_id)
        if unit_id in self.cart.keys():
            return True
        return False

    def count_of(self, unit_id: str | int) -> int:
        if unit_id is None:
            return self.delivery_price
        else:
            return self.cart.get(str(unit_id), 0)

    @property
    def empty(self) -> bool:
        return self.__len__() == 0

    @property
    def units_count(self) -> int:
        count = 0
        for unit_id in self.cart:
            count += self.cart[unit_id]
        return count

    @property
    def units_count_text(self) -> str:
        count = self.units_count
        if count > 9:
            text = "9+"
        else:
            text = str(count)
        return text

    def count_total_items_price(self) -> int:
        total_items_price = 0
        units_ids = self.cart.keys()
        for unit_id in units_ids:
            quantity = self.cart[unit_id]
            unit = get_object_or_404(Unit, id=unit_id)
            total_items_price += quantity * unit.get_price()
        return total_items_price

    def count_delivery_price(
        self,
        total_items_price: int,
    ) -> int:
        delivery_price = DELIVERY_PRICES[0]
        current_rng = 0
        for rng, prc in DELIVERY_PRICES.items():
            if current_rng < rng and total_items_price >= rng:
                current_rng = rng
                delivery_price = prc
        return delivery_price

    @property
    def delivery_price(self) -> int:
        return self.count_delivery_price(self.count_total_items_price())

    @property
    def total_price(self) -> tuple[int, int]:
        total_items_price = self.count_total_items_price()
        delivery_price = self.count_delivery_price(total_items_price)
        return TotalPrices(
            total_items_price,
            delivery_price,
            delivery_price + total_items_price,
        )

    def __contains__(self, unit_id: int | str):
        return self.contains(unit_id)

    def __iter__(self) -> Generator[CartItem, Any, Any]:
        units_ids = self.cart.keys()

        for unit_id in units_ids:
            quantity = self.cart[unit_id]
            unit = get_object_or_404(Unit, id=unit_id)
            price = unit.price
            if unit.discount_price:
                price = unit.discount_price

            yield CartItem(
                unit.full_name,
                Decimal(price),
                Decimal(quantity),
                unit=unit,
            )

    def __len__(self) -> int:
        return self.units_count
