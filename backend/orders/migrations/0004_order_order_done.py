# Generated by Django 5.0.3 on 2024-04-04 11:45

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("orders", "0003_alter_order_account_alter_orderitem_order_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="order_done",
            field=models.BooleanField(default=False, verbose_name="Заказ выполнен"),
        ),
    ]
