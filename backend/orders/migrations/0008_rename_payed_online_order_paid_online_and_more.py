# Generated by Django 5.0.3 on 2024-06-06 07:01

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("orders", "0007_order_total_cost"),
    ]

    operations = [
        migrations.RenameField(
            model_name="order",
            old_name="payed_online",
            new_name="paid_online",
        ),
        migrations.AddField(
            model_name="order",
            name="paid_online_amount",
            field=models.DecimalField(
                decimal_places=2,
                default=0,
                max_digits=10,
                verbose_name="Сумма оплаты онлайн",
            ),
        ),
    ]
