import sys
from pathlib import Path
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

ROOT_DIR = Path(__file__).parent.parent
sys.path.append(str(ROOT_DIR))
from categories.models import Category


def home(request: HttpRequest) -> HttpRequest:
    categories = Category.objects.all()

    return render(
        request,
        "pages/home.html",
        context={"items": categories},
    )
