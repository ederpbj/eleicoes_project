# Generated by Django 4.2.16 on 2024-10-05 00:00

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
                ("cod", models.IntegerField()),
                ("opm", models.CharField(max_length=100)),
                ("zona", models.IntegerField()),
                ("municipio", models.CharField(max_length=100)),
                ("nome_local", models.CharField(max_length=255)),
                ("endereco", models.CharField(max_length=255)),
                ("bairro", models.CharField(max_length=100)),
                ("qtde_secoes", models.IntegerField()),
                ("data_instalacao", models.DateField(blank=True, null=True)),
                ("horario", models.CharField(max_length=50)),
                ("qtde_eleitores", models.IntegerField()),
                ("nivel_prioridade", models.CharField(max_length=50)),
                (
                    "local_votacao",
                    models.CharField(
                        choices=[("ativo", "Ativo"), ("inativo", "Inativo")],
                        default="ativo",
                        max_length=10,
                    ),
                ),
                (
                    "status_urnas",
                    models.CharField(
                        choices=[
                            ("instalada", "Instalada"),
                            ("nao_instalada", "Não instalada"),
                            ("indisponivel", "Indisponível"),
                            ("desmobilizado", "Desmobilizado"),
                        ],
                        default="indisponivel",
                        max_length=20,
                    ),
                ),
                ("falta_militar", models.IntegerField()),
            ],
        ),
    ]
