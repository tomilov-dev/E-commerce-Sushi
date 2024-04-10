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


def on_map(request: HttpRequest) -> HttpResponse:
    return render(request, "pages/on_map.html")


def about(request: HttpRequest) -> HttpResponse:
    return render(request, "pages/about.html")


def blog(request: HttpRequest) -> HttpResponse:
    return render(request, "pages/blog.html")


def license(request: HttpRequest) -> HttpResponse:
    return render(request, "pages/license.html")


def terms(request: HttpRequest) -> HttpResponse:
    return render(request, "pages/terms.html")


def contact(request: HttpRequest) -> HttpResponse:
    return render(request, "pages/contact.html")


def requisites(request: HttpRequest) -> HttpResponse:
    return render(request, "pages/requisites.html")
