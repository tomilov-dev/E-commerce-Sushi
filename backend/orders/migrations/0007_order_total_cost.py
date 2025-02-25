# Generated by Django 5.0.3 on 2024-06-06 06:31

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("orders", "0006_order_payed_online_alter_order_payment"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="total_cost",
            field=models.DecimalField(
                decimal_places=2, default=0, max_digits=10, verbose_name="Сумма оплаты"
            ),
        ),
    ]
