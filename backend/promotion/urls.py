from django.urls import path

from .views import get_promotion_category, get_promo_action

app_name = "promotion"

urlpatterns = [
    path(
        "category/<slug:slug>/",
        get_promotion_category,
        name="get_promotion_category",
    ),
    path("<slug:slug>/", get_promo_action, name="get_promo_action"),
]
