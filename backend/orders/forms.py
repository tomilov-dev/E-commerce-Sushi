import re
from django import forms
from django.core.exceptions import ValidationError

from .models import Order


PHONE_RX = re.compile(r"^\+?[78]\d{10}$")
NAME_RX = re.compile(r"^[а-я]+$", re.IGNORECASE)


def validate_phone_number(value):
    if not PHONE_RX.match(value):
        raise ValidationError("Неверный формат номера телефона")


def validate_name(value):
    if not NAME_RX.match(value):
        raise ValidationError("Ошибки в имени или фамилии")


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            "phone",
            "first_name",
            "last_name",
            "delivery",
            "address",
            "payment",
            "client_comment",
        ]

        widgets = {
            "phone": forms.TextInput(attrs={"class": "order-form text-field"}),
            "first_name": forms.TextInput(attrs={"class": "order-form text-field"}),
            "last_name": forms.TextInput(attrs={"class": "order-form text-field"}),
            "delivery": forms.Select(
                attrs={"class": "order-form select-field form-select"}
            ),
            "payment": forms.Select(
                attrs={"class": "order-form select-field form-select"}
            ),
            "address": forms.TextInput(attrs={"class": "order-form text-field"}),
            "client_comment": forms.Textarea(
                attrs={"class": "order-form message-field", "cols": 20, "rows": 10}
            ),
        }

    def clean(self):
        cleaned_data = super().clean()

        validate_phone_number(cleaned_data.get("phone"))
        validate_name(cleaned_data.get("first_name"))

        return cleaned_data
