# Generated by Django 5.0.3 on 2024-03-24 08:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("categories", "0001_initial"),
        ("products", "0002_alter_unit_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="category",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="products",
                to="categories.category",
                verbose_name="Категория",
            ),
        ),
    ]
