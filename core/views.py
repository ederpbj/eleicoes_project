from django.shortcuts import render, get_object_or_404, redirect
from .models import LocalVotacao
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
    # Obtenha os dados do modelo LocalVotacao
    locais = LocalVotacao.objects.all()

    # Gráfico de Pizza para Status das Urnas
    fig_status_urnas = px.pie(
        names=locais.values_list('local_urnas', flat=True),
        title='Distribuição do Status das Urnas',
        color_discrete_sequence=['#EEE8AA', '#B0E0E6']
    )
    fig_status_urnas.update_traces(
        textinfo='label+percent',
        texttemplate='%{label}: %{percent} <b>%{value}</b>',  # Formatação com valor em negrito
        textposition='outside',
        marker=dict(colors=['#636EFA', '#EF553B', '#00CC96', '#AB63FA', '#FFA15A'])
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
    fig_status_fiscalizacao = px.pie(
        names=locais.values_list('fiscalizacao', flat=True),
        title='Distribuição do Status de Fiscalização',
        color_discrete_sequence=['#EEE8AA', '#B0E0E6']
    )
    fig_status_fiscalizacao.update_traces(
        textinfo='label+percent',
        texttemplate='%{label}: %{percent} <b>%{value}</b>',
        textposition='outside',
        marker=dict(colors=['#19D3F3', '#FF6692', '#B6E880', '#FF97FF', '#FECB52'])
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
    fig_status_local = px.pie(
        names=locais.values_list('local_votacao', flat=True),
        title='Distribuição do Status de Locais',
        color_discrete_sequence=['#EEE8AA', '#B0E0E6']
    )
    fig_status_local.update_traces(
        textinfo='label+percent',
        texttemplate='%{label}: %{percent} <b>%{value}</b>',
        textposition='outside',
        marker=dict(colors=['#FF4500', '#B0E0E6'])
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

    # Extraindo os dados para o gráfico
    cias = [item['cia'] for item in locais_por_cia]
    locais_votacao = [item['total_locais'] for item in locais_por_cia]

    # Gráfico de Pizza para Locais de Votação por OPM
    fig_locais_votacao_cia = px.pie(
        names=cias,
        values=locais_votacao,
        title='Distribuição de Locais de Votação por OPM',
        color_discrete_sequence=['#E74C3C', '#3498DB', '#9B59B6', '#2ECC71', '#F1C40F']
    )
    fig_locais_votacao_cia.update_traces(
        textinfo='label+percent',
        texttemplate='%{label}: %{percent} <b>%{value}</b>',
        textposition='outside',
        marker=dict(colors=['#FF4500', '#B0E0E6', '#90EE90'])
    )
    fig_locais_votacao_cia.update_layout(
        height=400,
        margin=dict(t=110, b=40, l=40, r=40),
        title={'font': {'size': 24}},
        font=dict(size=18),
        legend=dict(font=dict(size=16))
    )
    graph_locais_votacao_cia = fig_locais_votacao_cia.to_html()

    # Cálculo do total de faltas militares
    total_faltas_militar = locais.aggregate(total_faltas=Sum('falta_militar'))['total_faltas'] or 0

    # Renderizar os gráficos no template
    return render(request, 'dashboard.html', {
        'graph_status_urnas': graph_status_urnas,
        'graph_status_fiscalizacao': graph_status_fiscalizacao,
        'graph_status_local': graph_status_local,
        'graph_locais_votacao_cia': graph_locais_votacao_cia,
        'total_faltas_militar': total_faltas_militar,
    })
