from django.urls import path

from .views import cart_details, cart_add, cart_remove, cart_delete


app_name = "cart"


urlpatterns = [
    path("", cart_details, name="cart_details"),
    path("add/<int:unit_id>/", cart_add, name="cart_add"),
    path("remove/<int:unit_id>/", cart_remove, name="cart_remove"),
    path("delete/<int:unit_id>/", cart_delete, name="cart_delete"),
    # path("update/<int:unit_id>/", cart_update, name="cart_update"),
    # path("remove/<int:unit_id>/", cart_remove, name="cart_remove"),
]
