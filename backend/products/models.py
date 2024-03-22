import sys
from pathlib import Path
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


ROOT_DIR = Path(__file__).parent.parent
sys.path.append(str(ROOT_DIR))

from mixins import BaseMixin, WebMixin, AvailableMixin, PriorityMixin, NameMixin
from categories.models import Category


class Product(
    BaseMixin,
    WebMixin,
    PriorityMixin,
    models.Model,
):
    ## FK
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,  ## in case of accidental deletion
        verbose_name="Категория",
        null=True,  ## in case of accidental deletion
    )

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"


class Unit(
    AvailableMixin,
    models.Model,
):
    name = models.CharField(
        verbose_name="Название",
        blank=True,
        null=True,  ## use Product.name
    )
    price = models.DecimalField(
        verbose_name="Цена товарной единицы",
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(1, "Цена должна быть >= 1")],
    )

    discount_price = models.DecimalField(
        null=True,
        blank=True,
        verbose_name="Цена товарной единицы со скидкой",
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(1, "Цена должна быть >= 1")],
    )

    # FK
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name="Товар",
    )

    class Meta:
        verbose_name = "Товарная единица"
        verbose_name_plural = "Товарные единицы"


class Measure(
    NameMixin,
    models.Model,
):
    symbol = models.CharField()

    class Meta:
        verbose_name = "Единица измерения"
        verbose_name_plural = "Единицы измерения"


class Characteristics(models.Model):
    measure_count = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="Количество в заданных единицах измерения",
    )
    quantity = models.IntegerField(
        default=1,
        verbose_name="Количества товара в упаковке, шт",
    )

    proteins = models.IntegerField(
        verbose_name="Белки",
        blank=True,
        null=True,
    )
    fats = models.IntegerField(
        verbose_name="Жиры",
        blank=True,
        null=True,
    )
    carbohydrates = models.IntegerField(
        verbose_name="Углеводы",
        blank=True,
        null=True,
    )
    kilocalories = models.IntegerField(
        verbose_name="Килокалории",
        blank=True,
        null=True,
    )

    ## FK
    unit = models.ForeignKey(
        Unit,
        on_delete=models.CASCADE,
        verbose_name="Товарная единица",
    )
    measure = models.ForeignKey(
        Measure,
        on_delete=models.SET_NULL,
        verbose_name="Единица измерения",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Характеристика товарной единицы"
        verbose_name_plural = "Характеристики товарных единиц"
