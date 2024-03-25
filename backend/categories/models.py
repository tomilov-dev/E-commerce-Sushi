import sys
from pathlib import Path
from django.db import models
from django.urls import reverse

ROOT_DIR = Path(__file__).parent.parent
sys.path.append(str(ROOT_DIR))


from mixins import (
    BaseMixin,
    WebMixin,
    AvailableMixin,
    PriorityMixin,
    IconMixin,
    ShowNavbarMixin,
)


class Category(
    BaseMixin,
    WebMixin,
    AvailableMixin,
    PriorityMixin,
    IconMixin,
    ShowNavbarMixin,
    models.Model,
):
    @property
    def link(self) -> str:
        return reverse("categories:get_category", args=[self.slug])

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __repr__(self) -> str:
        return self.link
