# Generated by Django 5.0.3 on 2024-04-03 08:23

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0008_alter_characteristics_unit"),
    ]

    operations = [
        migrations.AddField(
            model_name="measure",
            name="display_name",
            field=models.CharField(default="NONE"),
            preserve_default=False,
        ),
    ]
