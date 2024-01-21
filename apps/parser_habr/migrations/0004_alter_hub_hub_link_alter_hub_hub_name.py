# Generated by Django 5.0 on 2024-01-21 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("parser_habr", "0003_delete_timer"),
    ]

    operations = [
        migrations.AlterField(
            model_name="hub",
            name="hub_link",
            field=models.URLField(
                max_length=10000, unique=True, verbose_name="Ссылка на хаб"
            ),
        ),
        migrations.AlterField(
            model_name="hub",
            name="hub_name",
            field=models.CharField(
                max_length=255, unique=True, verbose_name="Название хаба"
            ),
        ),
    ]
