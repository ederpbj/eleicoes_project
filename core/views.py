from django.shortcuts import render
from .models import LocalVotacao
import plotly.express as px
from django.db.models import Sum, Count

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

    # Contagem do status das urnas
    status_urnas = locais.values_list('local_urnas', flat=True)
    status_fiscalizacao = locais.values_list('fiscalizacao', flat=True)
    status_local = locais.values_list('local_votacao', flat=True)

    # Gráfico de Pizza para Status das Urnas
    fig_status_urnas = px.pie(
        names=status_urnas,
        title='Distribuição do Status das Urnas',
        color_discrete_sequence=['#EEE8AA', '#B0E0E6']  # Cores personalizadas
    )
    fig_status_urnas.update_traces(textinfo='label+percent+value', marker=dict(colors=['#636EFA', '#EF553B', '#00CC96', '#AB63FA', '#FFA15A']))  # Forçar cores personalizadas
    fig_status_urnas.update_layout(height=350)  # Reduzir altura do gráfico
    graph_status_urnas = fig_status_urnas.to_html()

    # Gráfico de Pizza para Fiscalização
    fig_status_fiscalizacao = px.pie(
        names=status_fiscalizacao,
        title='Distribuição do Status de Fiscalização',
        color_discrete_sequence=['#EEE8AA', '#B0E0E6']  # Cores personalizadas
    )
    fig_status_fiscalizacao.update_traces(textinfo='label+percent+value', marker=dict(colors=['#19D3F3', '#FF6692', '#B6E880', '#FF97FF', '#FECB52']))  # Forçar cores personalizadas
    fig_status_fiscalizacao.update_layout(height=350)  # Reduzir altura do gráfico
    graph_status_fiscalizacao = fig_status_fiscalizacao.to_html()

    # Gráfico de Pizza para Local de votação
    fig_status_local = px.pie(
        names=status_local,
        title='Distribuição do Status de Locais',
        color_discrete_sequence=['#EEE8AA', '#B0E0E6']  # Cores personalizadas
    )
    fig_status_local.update_traces(textinfo='label+percent+value', marker=dict(colors=['#FF4500', '#B0E0E6']))  # Forçar cores personalizadas
    fig_status_local.update_layout(height=350)  # Reduzir altura do gráfico
    graph_status_local = fig_status_local.to_html()

    # Agrupando locais de votação por CIA e contando
    locais_por_cia = (
        locais
        .values('cia')  # Agrupar por CIA
        .annotate(total_locais=Count('cia'))  # Contar o número de locais de votação por CIA
        .order_by('-total_locais')  # Ordenar em ordem decrescente
    )

    # Extraindo os dados para o gráfico
    cias = [item['cia'] for item in locais_por_cia]
    locais_votacao = [item['total_locais'] for item in locais_por_cia]

    # Gráfico de Pizza para Locais de Votação por CIA
    fig_locais_votacao_cia = px.pie(
        names=cias,
        values=locais_votacao,
        title='Distribuição de Locais de Votação por CIA',
        color_discrete_sequence=['#E74C3C', '#3498DB', '#2ECC71', '#9B59B6', '#F1C40F']  # Cores personalizadas
    )
    fig_locais_votacao_cia.update_traces(textinfo='label+percent+value', marker=dict(colors=['#FF4500', '#B0E0E6']))  # Forçar cores personalizadas
    fig_locais_votacao_cia.update_layout(height=350)  # Reduzir altura do gráfico
    graph_locais_votacao_cia = fig_locais_votacao_cia.to_html()

    # Renderizar os gráficos no template
    return render(request, 'dashboard.html', {
        'graph_status_urnas': graph_status_urnas,
        'graph_status_fiscalizacao': graph_status_fiscalizacao,
        'graph_status_local': graph_status_local,
        'graph_locais_votacao_cia': graph_locais_votacao_cia,  # Gráfico de Locais de Votação por CIA
    })