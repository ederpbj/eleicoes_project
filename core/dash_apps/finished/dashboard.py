# core/dash_apps/finished/dashboard.py
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
from django_plotly_dash import DjangoDash

# Crie uma instância do DjangoDash
app = DjangoDash('interactive_dashboard')

# Exemplo de dados (substitua com seus dados do Django)
df = pd.DataFrame({
    "CIA": ["A", "B", "C", "D"],
    "Eleitores": [1000, 1500, 1200, 1300],
    "Urnas": [10, 15, 12, 13],
    "Status": ["Instalada", "Não instalada", "Instalada", "Indisponível"]
})

# Layout do Dash
app.layout = html.Div([
    dcc.Graph(id='status-urnas'),
    dcc.Graph(id='eleitores-cia'),
    dcc.Graph(id='status-locais'),
    dcc.Graph(id='fiscalizacao'),

    # Dropdown para selecionar o status da urna
    dcc.Dropdown(
        id='status-dropdown',
        options=[{'label': status, 'value': status} for status in df['Status'].unique()],
        value='Instalada',  # Valor padrão
        clearable=False
    )
])

# Callbacks para interatividade
@app.callback(
    Output('eleitores-cia', 'figure'),
    Output('status-locais', 'figure'),
    Output('fiscalizacao', 'figure'),
    Input('status-dropdown', 'value')  # Quando o dropdown muda
)
def update_graphs(selected_status):
    # Filtrar os dados com base no status selecionado
    filtered_df = df[df['Status'] == selected_status]

    # Gráfico de eleitores por CIA
    eleitores_fig = px.bar(filtered_df, x='CIA', y='Eleitores', title='Eleitores por CIA')

    # Gráfico de status locais
    status_locais_fig = px.pie(filtered_df, names='CIA', values='Urnas', title='Urnas por CIA')

    # Gráfico de fiscalização
    fiscalizacao_fig = px.pie(filtered_df, names='CIA', values='Urnas', title='Fiscalização por CIA')

    return eleitores_fig, status_locais_fig, fiscalizacao_fig
