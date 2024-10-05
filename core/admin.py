from .models import LocalVotacao
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
import openpyxl
from openpyxl import Workbook

# Personalizar o título e os textos do Django Admin
admin.site.site_header = _("Administração das Eleições")
admin.site.site_title = _("Painel Administrativo das Eleições")
admin.site.index_title = _("Bem-vindo ao Painel de Controle")

@admin.register(LocalVotacao)
class LocalVotacaoAdmin(admin.ModelAdmin):
    # Exibir todos os campos do modelo na lista de objetos
    list_display = (
        'cod',
        'opm',
        'zona',
        'municipio',
        'nome_local',
        'endereco',
        'bairro',
        'qtde_secoes',
        'data_instalacao',
        'horario',
        'qtde_eleitores',
        'nivel_prioridade',
        'local_votacao',
        'status_urnas',
        'falta_militar',
    )

    # Filtros laterais para facilitar a navegação pelos registros
    list_filter = ('status_urnas', 'local_votacao', 'municipio', 'opm')

    # Campos para busca rápida no topo da página de administração
    search_fields = ('municipio', 'nome_local', 'opm', 'endereco', 'bairro')

    # Ordenação dos registros por 'cod' em ordem crescente
    ordering = ('cod',)

    # Campos editáveis diretamente na visualização da lista
    list_editable = ('status_urnas', 'local_votacao', 'falta_militar')

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
        # Criar uma nova planilha
        workbook = Workbook()
        worksheet = workbook.active
        worksheet.title = "Locais de Votação"

        # Definir cabeçalhos na primeira linha da planilha
        headers = [
            'cod', 'opm', 'zona', 'municipio', 'nome_local', 'endereco', 'bairro',
            'qtde_secoes', 'data_instalacao', 'horario', 'qtde_eleitores',
            'nivel_prioridade', 'local_votacao', 'status_urnas', 'falta_militar'
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
                local.municipio,
                local.nome_local,
                local.endereco,
                local.bairro,
                local.qtde_secoes,
                local.data_instalacao.strftime("%Y-%m-%d") if local.data_instalacao else "",
                local.horario,
                local.qtde_eleitores,
                local.nivel_prioridade,
                local.local_votacao,
                local.status_urnas,
                local.falta_militar,
            ]
            worksheet.append(row)

        # Salvar o arquivo Excel no diretório do projeto
        workbook.save("/Users/user/Desktop/temp/local_votacao_data.xlsx")
