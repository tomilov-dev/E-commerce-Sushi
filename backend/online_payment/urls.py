from django.urls import path
from .views import order_payed

app_name = "payment"

urlpatterns = [
    path("callback/", order_payed, name="order_payed"),
]
