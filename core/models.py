from django.db import models
from django.core.exceptions import ValidationError

class LocalVotacao(models.Model):
    LOCAL_VOTACAO_CHOICES = [
        ('Ativo', 'Ativo'),
        ('Inativo', 'Inativo'),
    ]

    OPM_CHOICES = [
        ('1º BPM', '1º BPM'),
        ('5º BPM', '5º BPM'),
        ('BEPTUR', 'BEPTUR'),
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

    cod = models.IntegerField(unique=True)  # Define o campo cod como único
    opm = models.CharField(max_length=100, choices=OPM_CHOICES, null=True,)
    zona = models.IntegerField()
    nome_local = models.CharField(max_length=255)
    endereco = models.CharField(max_length=255)
    bairro = models.CharField(max_length=100)
    secoes = models.IntegerField()
    data_instalacao = models.DateField(null=True, blank=True)
    horario = models.CharField(max_length=50)
    eleitores = models.IntegerField(null=True, blank=True)
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

    falta_militar = models.IntegerField(default=0)  # Adiciona o campo com valor padrão 0

    def clean(self):
        if self.eleitores is not None and self.eleitores < 0:
            raise ValidationError('O número de eleitores não pode ser negativo.')

    def is_active(self):
        return self.local_votacao == 'Ativo'

    def __str__(self):
        return f'{self.nome_local} - {self.bairro}'


class Ocorrencia(models.Model):
    OPM_CHOICES = [
        ('1º BPM', '1º BPM'),
        ('5º BPM', '5º BPM'),
        ('BEPTUR', 'BEPTUR'),
    ]

    codigo_ocorrencia = models.CharField('Código da Ocorrência', max_length=50, unique=True)
    quantidade_conduzidos = models.IntegerField('Quantidade de Conduzidos')
    opm = models.CharField('OPM', max_length=100,choices=OPM_CHOICES)
    tipo = models.CharField('Tipo', max_length=100, default='')

    def save(self, *args, **kwargs):
        # Converter para maiúsculas antes de salvar
        self.codigo_ocorrencia = self.codigo_ocorrencia.upper()
        self.opm = self.opm.upper()
        self.tipo = self.tipo.upper()
        super(Ocorrencia, self).save(*args, **kwargs)

    def __str__(self):
        return f'Ocorrência {self.codigo_ocorrencia}'
