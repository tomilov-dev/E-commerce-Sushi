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

    @property
    def link(self) -> str:
        return reverse("promotion:get_promotion_category", args=[self.slug])

    class Meta:
        verbose_name = "Промо-категория"
        verbose_name_plural = "Промо-категории"

    def __repr__(self) -> str:
        return self.link


class ProductPromotion(models.Model):
    ## FK
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name="Товар",
        related_name="product_promotions",
    )
    promotion_category = models.ForeignKey(
        PromotionCategory,
        on_delete=models.CASCADE,
        verbose_name="Промо-категория",
        related_name="product_promotions",
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

    @property
    def get_redir_link(self) -> str | None:
        if self.product:
            return self.product.link
        elif self.category:
            return self.category.link
        elif self.promotion_category:
            return self.promotion_category.link
        else:
            return None

    @property
    def link(self) -> str | None:
        if self.straight_redirect:
            if self.product:
                return self.product.link
            elif self.category:
                return self.category.link
            elif self.promotion_category:
                return self.promotion_category.link
            else:
                return "#"

        else:
            return reverse("promotion:get_promo_action", args=[self.slug])

    class Meta:
        verbose_name = "Промо-акция"
        verbose_name_plural = "Промо-акции"
