import sys
from pathlib import Path
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator

ROOT_DIR = Path(__file__).parent
sys.path.append(str(ROOT_DIR))

from utils import image_filename


class AvailableMixin(models.Model):
    available = models.BooleanField(
        verbose_name="Доступно",
        default=True,
    )

    class Meta:
        abstract = True


class PriorityMixin(models.Model):
    priority = models.IntegerField(
        default=0,
        verbose_name="Приоритет",
        help_text="По умолчанию 0. Максимальный приоритет 100.",
        validators=[
            MinValueValidator(0, "Приоритет не может быть меньше нуля!"),
            MaxValueValidator(100, "Приоритет не может быть больше 100!"),
        ],
    )

    class Meta:
        abstract = True


class IconMixin(models.Model):
    icon = models.ImageField(
        verbose_name="Иконка",
        upload_to=image_filename,
        null=True,
        blank=True,
    )

    class Meta:
        abstract = True


class WebMixin(models.Model):
    slug = models.SlugField(
        max_length=200,
        verbose_name="Человекочитаемый URL",
        unique=True,
        help_text="Должен быть на английском!",
        validators=[RegexValidator(r"^[a-z0-9-_%]+$", "Должен быть на английском!")],
    )

    class Meta:
        abstract = True


class ShowNavbarMixin(models.Model):
    show_navbar = models.BooleanField(
        verbose_name="Отображать в навигационной панели",
        default=True,
    )

    class Meta:
        abstract = True


class NameMixin(models.Model):
    name = models.CharField(
        verbose_name="Название",
        unique=True,
    )

    class Meta:
        abstract = True


class BaseMixin(NameMixin, models.Model):
    description = models.TextField(
        verbose_name="Описание",
        null=True,
        blank=True,
    )

    image = models.ImageField(
        verbose_name="Изображение",
        upload_to=image_filename,
        null=True,
        blank=True,
    )

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return self.name
