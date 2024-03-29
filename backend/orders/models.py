import uuid
from django.db import models
from django.urls import reverse
from django.core.validators import RegexValidator


from products.models import Unit
from accounts.models import CustomUser


class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = "PD", "Заказ ожидает подтверждения."
        IN_PROGRESS = "PR", "Заказ готовится."
        READY = "RD", "Заказ готов. Ожидает доставки."
        ON_WAY = "OW", "Заказ в пути."
        DONE = "DN", "Заказ полностью выполнен."
        DECLINED = "DC", "Заказ отклонен."

    class Payment(models.TextChoices):
        CASH = "CH", "Оплата наличными"
        CARD = "CD", "Оплата картой"

    class Delivery(models.TextChoices):
        PICKUP = "PK", "Самовывоз"
        DELIVERY = "DL", "Доставка"

    account = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="orders",
        verbose_name="Аккаунт заказчика",
        editable=False,
    )

    uuid = models.UUIDField(
        default=uuid.uuid4,
        blank=True,
        unique=True,
        verbose_name="Уникальный идентификатор заказа",
        editable=False,
    )

    phone = models.CharField(
        max_length=12,
        verbose_name="Номер телефона",
        validators=[RegexValidator(r"\+?[78]\d{10}")],
    )
    first_name = models.CharField(
        max_length=50,
        verbose_name="Имя",
    )
    last_name = models.CharField(
        null=True,
        blank=True,
        max_length=50,
        verbose_name="Фамилия (необязательно)",
    )

    address = models.CharField(
        default="Самовывоз",
        verbose_name="Адрес",
    )
    delivery = models.CharField(
        max_length=2,
        choices=Delivery.choices,
        verbose_name="Метод доставки",
    )
    payment = models.CharField(
        max_length=2,
        choices=Payment.choices,
        verbose_name="Способ оплаты",
    )

    client_comment = models.TextField(
        verbose_name="Комментарий клиента (необязательно)",
        blank=True,
        null=True,
    )

    ## editable
    business_comment = models.TextField(
        verbose_name="Комментарий компании",
        blank=True,
        null=True,
    )
    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name="Статус",
    )

    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Время создания",
    )
    updated = models.DateTimeField(
        auto_now=True,
        verbose_name="Время последнего обновления",
    )

    class Meta:
        ordering = ["-created"]
        indexes = [
            models.Index(fields=["-created"]),
        ]
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def get_absolute_url(self) -> str:
        return reverse("orders:order_detail", args=[self.uuid])

    @property
    def done(self) -> bool:
        if self.status == self.Status.DONE or self.status == self.Status.DECLINED:
            return True

        else:
            return False

    @property
    def total_cost(self) -> int:
        return self.get_total_cost()

    def get_total_cost(self) -> int:
        return sum(item.get_cost() for item in self.items.all())

    def __str__(self) -> str:
        return str(self.id)


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        related_name="items",
        on_delete=models.CASCADE,
        verbose_name="Заказ",
        editable=False,
    )

    unit = models.ForeignKey(
        Unit,
        on_delete=models.CASCADE,
        verbose_name="Товарная единица",
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Цена",
    )

    quantity = models.PositiveIntegerField(
        default=1,
        verbose_name="Количество",
    )

    def get_cost(self) -> int:
        return self.price * self.quantity

    @property
    def total_cost(self) -> int:
        return self.get_cost()

    @property
    def total_cost(self) -> int:
        return self.get_cost()

    def __str__(self) -> str:
        return str(self.id)
