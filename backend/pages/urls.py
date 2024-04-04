from django.urls import path

from .views import home, on_map, about, blog, license, terms, contact, requisites

app_name = "pages"

urlpatterns = [
    path("", home, name="home"),
    path("map/", on_map, name="map"),
    path("about/", about, name="about"),
    path("blog/", blog, name="blog"),
    path("license/", license, name="license"),
    path("terms/", terms, name="terms"),
    path("contact/", contact, name="contact"),
    path("requisites/", requisites, name="requisites"),
]
