# Generated by Django 4.2.16 on 2024-10-25 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0002_localvotacao_falta_militar_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="localvotacao",
            name="opm",
            field=models.CharField(max_length=100, null=True),
        ),
    ]
