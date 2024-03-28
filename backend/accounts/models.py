from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    username = None
    phone = models.CharField(
        max_length=12,
        unique=True,
        verbose_name="Номер телефона",
        validators=[RegexValidator(r"\+?[78]\d{10}")],
    )

    USERNAME_FIELD = "phone"

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class PhoneConfirmation(models.Model):
    phone = models.CharField(max_length=20, unique=True, verbose_name="Номер телефона")
    code = models.CharField(max_length=6)
    phone_hash = models.CharField(max_length=70, unique=True)
    password = models.CharField()
    sent_time = models.IntegerField()

    class Meta:
        verbose_name = "Подтверждение номера телефона"
        verbose_name_plural = "Подтверждения номеров телефонов"
