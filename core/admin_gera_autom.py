from .models import LocalVotacao
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
import openpyxl
from openpyxl import Workbook
import os
from pathlib import Path
import django

# Definir a variável de ambiente DJANGO_SETTINGS_MODULE antes de inicializar o Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eleicoes.settings')

# Inicializar o Django
django.setup()

from core.models import LocalVotacao

BASE_DIR = Path(__file__).resolve().parent.parent
# Personalizar o título e os textos do Django Admin
admin.site.site_header = _("Administração das Eleições")
admin.site.site_title = _("Painel Administrativo das Eleições")
admin.site.index_title = _("Bem-vindo ao Painel de Controle")

@admin.register(LocalVotacao)
class LocalVotacaoAdmin(admin.ModelAdmin):
    # Exibir todos os campos do modelo na lista de objetos
    list_display = (
        'cod',
        'cia',
        'zona',
        'nome_local',
        'endereco',
        'bairro',
        'secoes',
        'data_instalacao',
        'horario',
        'eleitores',
        'prioridade',
        'local_votacao',
        'local_urnas',
    )

    # Filtros laterais para facilitar a navegação pelos registros
    list_filter = ('local_votacao', 'local_urnas', 'cia')

    # Campos para busca rápida no topo da página de administração
    search_fields = ('local_votacao', 'cia', 'endereco', 'bairro')

    # Ordenação dos registros por 'cod' em ordem crescente
    ordering = ('cod',)

    # Campos editáveis diretamente na visualização da lista
    list_editable = ('local_urnas', 'local_votacao', 'fiscalizacao')

    # Número de registros exibidos por página
    list_per_page = 20

    # Método sobrescrito para salvar no banco e também gerar o arquivo Excel
    def save_model(self, request, obj, form, change):
        # Salvar o objeto no banco de dados
        super().save_model(request, obj, form, change)

        # Gerar o arquivo Excel com todos os dados da tabela LocalVotacao
        self.exportar_para_excel()

    # Método para exportar os dados para um arquivo Excel
    def exportar_para_excel(self):
        try:
            # Criar uma nova planilha
            workbook = Workbook()
            worksheet = workbook.active
            worksheet.title = "Locais de Votação"

            # Definir cabeçalhos na primeira linha da planilha
            headers = [
                'cod', 'cia', 'zona', 'nome_local', 'endereco', 'bairro',
                'secoes', 'data_instalacao', 'horario', 'eleitores',
                'prioridade', 'local_votacao', 'local_urnas'
            ]
            worksheet.append(headers)

            # Pegar todos os registros do banco de dados
            locais_votacao = LocalVotacao.objects.all()

            # Adicionar os dados de cada local de votação na planilha
            for local in locais_votacao:
                row = [
                    local.cod,
                    local.opm,
                    local.zona,
                    local.nome_local,
                    local.endereco,
                    local.bairro,
                    local.secoes,
                    local.data_instalacao.strftime("%Y-%m-%d") if local.data_instalacao else "",
                    local.horario,
                    local.eleitores,
                    local.prioridade,
                    local.local_votacao,
                    local.local_urnas,
                ]
                worksheet.append(row)

            # Salvar o arquivo Excel no diretório do projeto
            caminho_arquivo = os.path.join(BASE_DIR, 'Dados_eleições_2024.2_Dj.xlsx')
            workbook.save(caminho_arquivo)
            print(f"Arquivo salvo com sucesso em: {caminho_arquivo}")

        except Exception as e:
            print(f"Erro ao salvar o arquivo Excel: {e}")
