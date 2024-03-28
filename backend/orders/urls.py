from django.urls import path

from .views import order_detail, order_list, order_confirm

app_name = "orders"

urlpatterns = [
    path("list/", order_list, name="order_list"),
    path("confirm/", order_confirm, name="order_confirm"),
    path("details/<str:uuid>/", order_detail, name="order_detail"),
]
