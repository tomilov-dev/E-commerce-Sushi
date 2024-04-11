import sys
from pathlib import Path
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

ROOT_DIR = Path(__file__).parent.parent
sys.path.append(str(ROOT_DIR))
from categories.models import Category


def home(request: HttpRequest) -> HttpRequest:
    return render(
        request,
        "pages/home.html",
    )


def info(request: HttpRequest) -> HttpResponse:
    return render(request, "pages/info.html")


def delivery(request: HttpRequest) -> HttpResponse:
    return render(request, "pages/delivery.html")


def payment(request: HttpRequest) -> HttpResponse:
    return render(request, "pages/payment.html")


def news(request: HttpRequest) -> HttpResponse:
    return render(request, "pages/news.html")


def about(request: HttpRequest) -> HttpResponse:
    return render(request, "pages/about.html")


def requisites(request: HttpRequest) -> HttpResponse:
    return render(request, "pages/requisites.html")


def commercial(request: HttpRequest) -> HttpResponse:
    return render(request, "pages/commercial.html")


def confidential(request: HttpRequest) -> HttpResponse:
    return render(request, "pages/confidential.html")


def terms(request: HttpRequest) -> HttpResponse:
    return render(request, "pages/terms.html")


def rules(request: HttpRequest) -> HttpResponse:
    return render(request, "pages/rules.html")


def important(request: HttpRequest) -> HttpResponse:
    return render(request, "pages/important.html")
