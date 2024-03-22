import sys
from pathlib import Path
from django.db import models


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
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
