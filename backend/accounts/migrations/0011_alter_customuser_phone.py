# Generated by Django 5.0.3 on 2024-04-10 14:00

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0010_alter_customuser_phone"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customuser",
            name="phone",
            field=models.CharField(
                max_length=12,
                unique=True,
                validators=[
                    django.core.validators.RegexValidator(
                        "\\+?[78]\\d{10}$",
                        message="Некорректно введен номер. Корректный пример: 89012209999",
                    )
                ],
                verbose_name="Номер телефона",
            ),
        ),
    ]
