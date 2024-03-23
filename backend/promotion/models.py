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
from products.models import Product
from categories.models import Category


class PromotionCategory(
    BaseMixin,
    WebMixin,
    AvailableMixin,
    PriorityMixin,
    IconMixin,
    ShowNavbarMixin,
    models.Model,
):
    """
    Promo category.
    Combines products that relies to specific promo action.
    """

    class Meta:
        verbose_name = "Промо-категория"
        verbose_name_plural = "Промо-категории"


class ProductPromotion(models.Model):
    ## FK
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name="Товар",
    )
    promotion_category = models.ForeignKey(
        PromotionCategory,
        on_delete=models.CASCADE,
        verbose_name="Промо-категория",
    )

    class Meta:
        verbose_name = "Промо-категория товара"
        verbose_name_plural = "Промо-категории товара"

    def __str__(self) -> str:
        return f"{self.product.name} :: {self.promotion_category.name}"


class PromoAction(
    BaseMixin,
    WebMixin,
    AvailableMixin,
    PriorityMixin,
    models.Model,
):
    straight_redirect = models.BooleanField(
        default=False,
        verbose_name="Прямой переход на акционный товар или категорию",
    )

    ## FK
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name="Товар",
        blank=True,
        null=True,
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name="Категория",
        blank=True,
        null=True,
    )
    promotion_category = models.ForeignKey(
        PromotionCategory,
        on_delete=models.CASCADE,
        verbose_name="Промо-категория",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Промо-акция"
        verbose_name_plural = "Промо-акции"
