from django.shortcuts import render, get_object_or_404, redirect
from .models import LocalVotacao, Ocorrencia
import plotly.express as px  # Importando a biblioteca Plotly Express para criar gráficos
from django.db.models import Sum, Count  # Importando métodos de agregação para manipulação de dados

def listar_locais(request):
    locais = LocalVotacao.objects.all()
    return render(request, 'eleicoes_app/listar_locais.html', {'locais': locais})

def editar_local(request, id):
    local = get_object_or_404(LocalVotacao, pk=id)
    if request.method == 'POST':
        local.nome_local = request.POST.get('nome_local')
        local.endereco = request.POST.get('endereco')
        # Adicione outros campos conforme necessário
        local.save()
        return redirect('listar_locais')
    return render(request, 'eleicoes_app/editar_local.html', {'local': local})

# GERA GRÁFICOS
def dashboard_view(request):
    # Obtenha o valor do filtro CIA do parâmetro GET
    selected_cia = request.GET.get('cia')

    # Obtenha os locais, aplicando o filtro por CIA se selecionado
    if selected_cia:
        locais = LocalVotacao.objects.filter(cia=selected_cia)
    else:
        locais = LocalVotacao.objects.all()

    # Lista de todas as CIAs para popular o dropdown
    cia_list = LocalVotacao.objects.values_list('cia', flat=True).distinct()

    # Mapeamento de cores para Status das Urnas e criação dos gráficos
    status_urnas_colors = {
        'Instalada': '#EEE8AA',
        'Não instalada': '#636EFA',
    }
    urna_labels = locais.values_list('local_urnas', flat=True)
    urna_colors = [status_urnas_colors.get(label, '#808080') for label in urna_labels]

    fig_status_urnas = px.pie(
        names=urna_labels,
        title='Distribuição do Status das Urnas',
    )
    fig_status_urnas.update_traces(
        textinfo='label+percent',
        texttemplate='%{label}: %{percent} <b>%{value}</b>',
        textposition='outside',
        marker=dict(colors=urna_colors)
    )
    fig_status_urnas.update_layout(
        height=400,
        margin=dict(t=110, b=40, l=40, r=40),
        title={'font': {'size': 24}},
        font=dict(size=18),
        legend=dict(font=dict(size=16))
    )
    graph_status_urnas = fig_status_urnas.to_html()

    # Gráfico de Pizza para Fiscalização
    fiscalizacao_colors = {
        'Fiscalizado': '#EEE8AA',
        'Não Fiscalizado': '#636EFA',
    }
    fiscalizacao_labels = locais.values_list('fiscalizacao', flat=True)
    fiscalizacao_colors = [fiscalizacao_colors.get(label, '#808080') for label in fiscalizacao_labels]

    fig_status_fiscalizacao = px.pie(
        names=fiscalizacao_labels,
        title='Distribuição do Status de Fiscalização',
    )
    fig_status_fiscalizacao.update_traces(
        textinfo='label+percent',
        texttemplate='%{label}: %{percent} <b>%{value}</b>',
        textposition='outside',
        marker=dict(colors=fiscalizacao_colors)
    )
    fig_status_fiscalizacao.update_layout(
        height=400,
        margin=dict(t=110, b=40, l=40, r=40),
        title={'font': {'size': 24}},
        font=dict(size=18),
        legend=dict(font=dict(size=16))
    )
    graph_status_fiscalizacao = fig_status_fiscalizacao.to_html()

    # Gráfico de Pizza para Status de Locais
    status_local_colors = {
        'Ativo': '#EEE8AA',
        'Inativo': '#636EFA'
    }
    local_labels = locais.values_list('local_votacao', flat=True)
    local_colors = [status_local_colors.get(label, '#808080') for label in local_labels]

    fig_status_local = px.pie(
        names=local_labels,
        title='Distribuição do Status de Locais',
    )
    fig_status_local.update_traces(
        textinfo='label+percent',
        texttemplate='%{label}: %{percent} <b>%{value}</b>',
        textposition='outside',
        marker=dict(colors=local_colors)
    )
    fig_status_local.update_layout(
        height=400,
        margin=dict(t=110, b=40, l=40, r=40),
        title={'font': {'size': 24}},
        font=dict(size=18),
        legend=dict(font=dict(size=16))
    )
    graph_status_local = fig_status_local.to_html()

    # Agrupando locais de votação por CIA e contando
    locais_por_cia = (
        locais
        .values('cia')
        .annotate(total_locais=Count('cia'))
        .order_by('-total_locais')
    )

    cias = [item['cia'] for item in locais_por_cia]
    locais_votacao = [item['total_locais'] for item in locais_por_cia]

    # Gráfico de Barras Horizontal para Locais de Votação por CIA
    fig_locais_votacao_cia = px.bar(
        x=locais_votacao,
        y=cias,
        orientation='h',
        title='Distribuição de Locais de Votação por OPM',
        category_orders={"y": cias}
    )
    fig_locais_votacao_cia.update_traces(
        texttemplate='%{x}',
        textposition='outside'
    )
    fig_locais_votacao_cia.update_layout(
        height=400,
        margin=dict(t=110, b=40, l=40, r=40),
        title={'font': {'size': 24}},
        xaxis_title="Quantidade de Locais",
        yaxis_title="CIA",
        font=dict(size=18)
    )
    graph_locais_votacao_cia = fig_locais_votacao_cia.to_html()

    # Cálculo do total de faltas militares
    total_faltas_militar = locais.aggregate(total_faltas=Sum('falta_militar'))['total_faltas'] or 0

    # Cálculo do total de ocorrências
    total_ocorrencias_registradas = Ocorrencia.objects.aggregate(total_ocorrencias=Sum('quantidade_conduzidos'))['total_ocorrencias'] or 0

    # Renderizar o template com todos os gráficos e variáveis
    return render(request, 'dashboard.html', {
        'graph_status_urnas': graph_status_urnas,
        'graph_status_fiscalizacao': graph_status_fiscalizacao,
        'graph_status_local': graph_status_local,
        'graph_locais_votacao_cia': graph_locais_votacao_cia,
        'total_faltas_militar': total_faltas_militar,
        'total_ocorrencias_registradas': total_ocorrencias_registradas,
        'cia_list': cia_list,
        'selected_cia': selected_cia,
    })