from django.urls import path

from .views import home, on_map, about

app_name = "pages"

urlpatterns = [
    path("", home, name="home"),
    path("map/", on_map, name="map"),
    path("about/", about, name="about"),
]
