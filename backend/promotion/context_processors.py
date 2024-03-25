from django.http import HttpRequest
from .models import PromoAction


def promotion_context(request: HttpRequest) -> dict:
    promos = PromoAction.objects.all().order_by("-priority")
    return {"promotion_context": promos}
