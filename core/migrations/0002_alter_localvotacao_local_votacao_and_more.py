# Generated by Django 4.2.16 on 2024-10-05 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="localvotacao",
            name="local_votacao",
            field=models.CharField(
                choices=[("Ativo", "Ativo"), ("Inativo", "Inativo")],
                default="Ativo",
                max_length=10,
            ),
        ),
        migrations.AlterField(
            model_name="localvotacao",
            name="status_urnas",
            field=models.CharField(
                choices=[
                    ("Instalada", "Instalada"),
                    ("Não instalada", "Não instalada"),
                    ("Indisponível", "Indisponível"),
                    ("Desmobilizado", "Desmobilizado"),
                ],
                default="Indisponível",
                max_length=20,
            ),
        ),
    ]
