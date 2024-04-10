import sys
from pathlib import Path
from django.http import HttpRequest
from django.core.cache import cache

ROOT_DIR = Path(__file__).parent.parent
sys.path.append(str(ROOT_DIR))

from categories.models import Category
from promotion.models import PromotionCategory
from caching import CATEGORIES_KEY, PROMOTION_CATEGORIES_KEY, DEFAULT_CACHE_TIME


def categories_context(
    request: HttpRequest,
) -> dict:
    default_categories = cache.get(CATEGORIES_KEY)
    if not default_categories:
        default_categories = Category.objects.all().order_by("-priority")
        cache.set(CATEGORIES_KEY, default_categories, DEFAULT_CACHE_TIME)

    promotion_categories = cache.get(PROMOTION_CATEGORIES_KEY)
    if not promotion_categories:
        promotion_categories = PromotionCategory.objects.all().order_by("-priority")
        cache.set(PROMOTION_CATEGORIES_KEY, promotion_categories, DEFAULT_CACHE_TIME)

    categories: list | None = list(promotion_categories)
    if categories:
        categories.extend(list(default_categories))
    else:
        categories = list(default_categories)

    return {"categories_context": categories}
