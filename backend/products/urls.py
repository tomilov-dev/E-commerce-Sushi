from django.urls import path

from .views import get_product

app_name = "products"

urlpatterns = [
    path("<slug:slug>/", get_product, name="get_product"),
]
