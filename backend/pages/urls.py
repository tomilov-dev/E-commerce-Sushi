from django.urls import path

from .views import (
    home,
    about,
    requisites,
    info,
    delivery,
    payment,
    news,
    commercial,
    confidential,
    terms,
    important,
    rules,
    menu,
)

app_name = "pages"

urlpatterns = [
    path("", home, name="home"),
    path("menu/", menu, name="menu"),
    path("delivery/", delivery, name="delivery"),
    path("payment/", payment, name="payment"),
    path("news/", news, name="news"),
    path("about/", about, name="about"),
    path("requisites/", requisites, name="requisites"),
    path("commercial/", commercial, name="commercial"),
    path("confidential/", confidential, name="confidential"),
    path("terms/", terms, name="terms"),
    path("important/", important, name="important"),
    path("rules/", rules, name="rules"),
]
