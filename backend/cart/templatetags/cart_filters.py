import sys
from pathlib import Path
from django import template

ROOT_DIR = Path(__file__).parent.parent.parent
sys.path.append(str(ROOT_DIR))

from cart.cart import Cart

register = template.Library()


@register.filter
def cart_count_of(cart: Cart, unit_id: int | str = None):
    return cart.count_of(unit_id)
