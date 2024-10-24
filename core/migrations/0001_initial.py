# Generated by Django 4.2.16 on 2024-10-24 01:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="LocalVotacao",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("cod", models.IntegerField(unique=True)),
                ("cia", models.CharField(max_length=100)),
                ("zona", models.IntegerField()),
                ("nome_local", models.CharField(max_length=255)),
                ("endereco", models.CharField(max_length=255)),
                ("bairro", models.CharField(max_length=100)),
                ("secoes", models.IntegerField()),
                ("data_instalacao", models.DateField(blank=True, null=True)),
                ("horario", models.CharField(max_length=50)),
                ("eleitores", models.IntegerField()),
                ("prioridade", models.CharField(max_length=50)),
                (
                    "local_votacao",
                    models.CharField(
                        choices=[("Ativo", "Ativo"), ("Inativo", "Inativo")],
                        default="Ativo",
                        max_length=10,
                    ),
                ),
                (
                    "local_urnas",
                    models.CharField(
                        choices=[
                            ("Instalada", "Instalada"),
                            ("Não instalada", "Não instalada"),
                            ("Indisponível", "Indisponível"),
                            ("Desmobilizado", "Desmobilizado"),
                        ],
                        default="Não instalada",
                        max_length=20,
                    ),
                ),
                (
                    "fiscalizacao",
                    models.CharField(
                        choices=[
                            ("Fiscalizado", "Fiscalizado"),
                            ("Não Fiscalizado", "Não Fiscalizado"),
                        ],
                        default="Não Fiscalizado",
                        max_length=20,
                    ),
                ),
            ],
        ),
    ]
