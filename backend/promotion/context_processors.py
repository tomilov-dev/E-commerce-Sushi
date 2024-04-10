from django.core.cache import cache
from django.http import HttpRequest

from .models import PromoAction
from caching import PROMO_ACTIONS_KEY, DEFAULT_CACHE_TIME


def promotion_context(request: HttpRequest) -> dict:
    promos = cache.get(PROMO_ACTIONS_KEY)
    if not promos:
        promos = (
            PromoAction.objects.all()
            .select_related(
                "product",
                "category",
                "promotion_category",
            )
            .order_by("-priority")
        )
        cache.set(PROMO_ACTIONS_KEY, promos, DEFAULT_CACHE_TIME)

    return {"promotion_context": promos}
