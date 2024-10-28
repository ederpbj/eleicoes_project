
from .models import LocalVotacao
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from openpyxl import Workbook
from django.urls import path
from django.shortcuts import redirect

from pathlib import Path
from django.http import HttpResponse

from django.contrib import admin
from .models import Ocorrencia

BASE_DIR = Path(__file__).resolve().parent.parent

# Personalizar o título e os textos do Django Admin
admin.site.site_header = _("Administração das Eleições")
admin.site.site_title = _("Painel Administrativo das Eleições")
admin.site.index_title = _("Bem-vindo ao Painel de Controle")



admin.site.register(Ocorrencia)

@admin.register(LocalVotacao)
class LocalVotacaoAdmin(admin.ModelAdmin):
    # Exibir todos os campos do modelo na lista de objetos
    list_display = (
        'cod',
        'opm',
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
        'fiscalizacao',
        'falta_militar',
    )

    # Filtros laterais para facilitar a navegação pelos registros
    list_filter = ('local_urnas', 'local_votacao', 'opm')

    # Campos para busca rápida no topo da página de administração
    search_fields = ('nome_local', 'opm', 'endereco', 'bairro')

    # Ordenação dos registros por 'cod' em ordem crescente
    ordering = ('cod',)

    # Campos editáveis diretamente na visualização da lista
    list_editable = ('local_urnas', 'fiscalizacao', 'local_votacao', 'falta_militar')

    # Número de registros exibidos por página
    list_per_page = 20

    # Adicionar o botão na página de administração
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['export_button'] = True  # Adiciona um contexto extra para exibir o botão
        return super().changelist_view(request, extra_context=extra_context)

    def exportar_para_excel(self, request):
        # Buscar todos os registros do banco de dados
        queryset = LocalVotacao.objects.all()

        try:
            workbook = Workbook()
            worksheet = workbook.active
            worksheet.title = "Locais de Votação"

            headers = [
                'cod', 'opm', 'zona', 'nome_local', 'endereco', 'bairro',
                'secoes', 'data_instalacao', 'horario', 'eleitores',
                'prioridade', 'local_votacao', 'local_urnas', 'fiscalizacao', 'falta_militar'
            ]
            worksheet.append(headers)

            for local in queryset:
                row = [
                    local.cod, local.opm, local.zona, local.nome_local,
                    local.endereco, local.bairro, local.secoes,
                    local.data_instalacao.strftime("%Y-%m-%d") if local.data_instalacao else "",
                    local.horario, local.eleitores, local.prioridade,
                    local.local_votacao, local.local_urnas, local.fiscalizacao, local.falta_militar,
                ]
                worksheet.append(row)

            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename=Dados_eleições_2024.2.xlsx'
            workbook.save(response)
            return response

        except Exception as e:
            self.message_user(request, f"Erro ao gerar o arquivo Excel: {e}", level='error')
            return redirect('admin:core_localvotacao_changelist')

    # Registrar a URL personalizada para o botão de exportação
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('exportar_excel/', self.admin_site.admin_view(self.exportar_para_excel), name='exportar_para_excel'),
        ]
        return custom_urls + urls