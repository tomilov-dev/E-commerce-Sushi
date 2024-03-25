import sys
from pathlib import Path
from django.http import HttpRequest

ROOT_DIR = Path(__file__).parent.parent
sys.path.append(str(ROOT_DIR))

from categories.models import Category
from promotion.models import PromotionCategory


def categories_context(
    request: HttpRequest,
) -> dict:
    default_categories = Category.objects.all().order_by("-priority")
    promotion_categories = PromotionCategory.objects.all().order_by("-priority")

    categories = []
    for category in promotion_categories:
        categories.append(category)
    for category in default_categories:
        categories.append(category)

    return {"categories_context": categories}
