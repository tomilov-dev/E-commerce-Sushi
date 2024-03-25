from django.urls import path

from .views import get_category

app_name = "categories"

urlpatterns = [
    path("<slug:slug>/", get_category, name="get_category"),
]
