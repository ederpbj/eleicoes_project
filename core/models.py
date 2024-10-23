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
    cia = models.CharField(max_length=100)
    zona = models.IntegerField()
    nome_local = models.CharField(max_length=255)
    endereco = models.CharField(max_length=255)
    bairro = models.CharField(max_length=100)
    secoes = models.IntegerField()
    data_instalacao = models.DateField(null=True, blank=True)  # Permitir valores nulos
    horario = models.CharField(max_length=50)
    eleitores = models.IntegerField()
    prioridade = models.CharField(max_length=50)
    local_votacao = models.CharField(
        max_length=10,
        choices=LOCAL_VOTACAO_CHOICES,
        default='Ativo',
    )
    local_urnas = models.CharField(
        max_length=20,
        choices=STATUS_URNAS_CHOICES,
        default='Não instalada',
    )
    fiscalizacao = models.CharField(
        max_length=20,
        choices=STATUS_FISCALIZACAO,
        default='Não Fiscalizado',
    )

    def __str__(self):
        return f'{self.nome_local} - {self.bairro}'
