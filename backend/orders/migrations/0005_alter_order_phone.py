# Generated by Django 5.0.3 on 2024-04-10 14:00

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("orders", "0004_order_order_done"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="phone",
            field=models.CharField(
                max_length=12,
                validators=[django.core.validators.RegexValidator("\\+?[78]\\d{10}$")],
                verbose_name="Номер телефона",
            ),
        ),
    ]
