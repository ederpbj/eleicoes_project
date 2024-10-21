from django.db import models

class LocalVotacao(models.Model):
    LOCAL_VOTACAO_CHOICES = [
        ('Ativo', 'Ativo'),
        ('Inativo', 'Inativo'),
    ]

    STATUS_URNAS_CHOICES = [
        ('Instalada', 'Instalada'),
        ('Não instalada', 'Não instalada'),
        ('Indisponível', 'Indisponível'),
        ('Desmobilizado', 'Desmobilizado'),
    ]

    STATUS_FISCALIZACAO = [
        ('Fiscalizado', 'Fiscalizado'),
        ('Não Fiscalizado', 'Não Fiscalizado'),
    ]

    cod = models.IntegerField()
    opm = models.CharField(max_length=100)
    zona = models.IntegerField()
    municipio = models.CharField(max_length=100)
    nome_local = models.CharField(max_length=255)
    endereco = models.CharField(max_length=255)
    bairro = models.CharField(max_length=100)
    qtde_secoes = models.IntegerField()
    data_instalacao = models.DateField(null=True, blank=True)  # Permitir valores nulos
    horario = models.CharField(max_length=50)
    qtde_eleitores = models.IntegerField()
    nivel_prioridade = models.CharField(max_length=50)
    local_votacao = models.CharField(
        max_length=10,
        choices=LOCAL_VOTACAO_CHOICES,
        default='Ativo',
    )
    status_urnas = models.CharField(
        max_length=20,
        choices=STATUS_URNAS_CHOICES,
        default='Indisponível',
    )
    status_fiscalizacao = models.CharField(
        max_length=20,
        choices=STATUS_FISCALIZACAO,
        default='Não Fiscalizado',
    )
    falta_militar = models.IntegerField()

    def __str__(self):
        return f'{self.nome_local} - {self.municipio}'
