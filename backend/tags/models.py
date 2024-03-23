import sys
from pathlib import Path
from django.db import models


ROOT_DIR = Path(__file__).parent.parent
sys.path.append(str(ROOT_DIR))

from mixins import BaseMixin, AvailableMixin
from products.models import Product


class Tag(
    BaseMixin,
    AvailableMixin,
    models.Model,
):
    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"


class ProductTag(models.Model):
    ## FK
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        verbose_name="Тег",
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name="Товар",
    )

    class Meta:
        verbose_name = "Тег товара"
        verbose_name_plural = "Теги товара"

    def __str__(self) -> str:
        return f"{self.product.name} :: {self.tag.name}"
