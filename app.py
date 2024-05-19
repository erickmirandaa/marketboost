# Importando as bibliotecas necessárias
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

# Função para analisar os produtos no arquivo CSV

# Caminho do arquivo CSV
arquivo_csv = r'C:\Users\ERICK NUCLEO\Downloads\Shopee_ads.csv'

def analisar_produtos(arquivo_csv):
    df = pd.read_csv(arquivo_csv)

    colunas_analisadas = ['Localização / Palavra-Chave', 'Nome do Produto / Anúncio', 'Impressão', 'Cliques', 'CTR', 'Conversões', 'Conversões Diretas', 
                          'Taxa de Conversão', 'Taxa de Conversão Direta', 'VBM', 'Receita direta', 'Despesas', 
                          'ROAS', 'ROAS Direto', 'ACOS', 'ACOS Direto']

    metricas_por_localizacao_palavra_chave = {}

    for index, row in df.iterrows():
        localizacao_palavra_chave = row['Localização / Palavra-Chave']
        produto = row['Nome do Produto / Anúncio']

        if localizacao_palavra_chave not in metricas_por_localizacao_palavra_chave:
            metricas_por_localizacao_palavra_chave[localizacao_palavra_chave] = {
                'Itens Vendidos': 0,
                'Produtos': {}
            }

        if produto not in metricas_por_localizacao_palavra_chave[localizacao_palavra_chave]['Produtos']:
            metricas_por_localizacao_palavra_chave[localizacao_palavra_chave]['Produtos'][produto] = {
                'Impressão': 0,
                'Cliques': 0,
                'Conversões': 0
            }

        metricas_por_localizacao_palavra_chave[localizacao_palavra_chave]['Produtos'][produto]['Impressão'] += row['Impressão']
        metricas_por_localizacao_palavra_chave[localizacao_palavra_chave]['Produtos'][produto]['Cliques'] += row['Cliques']
        metricas_por_localizacao_palavra_chave[localizacao_palavra_chave]['Produtos'][produto]['Conversões'] += row['Conversões']

        metricas_por_localizacao_palavra_chave[localizacao_palavra_chave]['Itens Vendidos'] += row['Conversões']

    return metricas_por_localizacao_palavra_chave

# Chamando a função para analisar os produtos
metricas_por_localizacao_palavra_chave = analisar_produtos(arquivo_csv)

# Layout do aplicativo
app.layout = html.Div([
    html.H1("Dashboard de Análise de Produtos", style={'textAlign': 'center', 'marginBottom': '20px'}),
    html.Div([
        dcc.Dropdown(
            id='localizacao-palavra-chave-dropdown',
            options=[{'label': localizacao_palavra_chave, 'value': localizacao_palavra_chave} for localizacao_palavra_chave in metricas_por_localizacao_palavra_chave.keys()],
            value=list(metricas_por_localizacao_palavra_chave.keys())[0]
        )
    ], style={'marginBottom': '20px'}),
    html.Div(id='metricas-container'),
    dcc.Graph(id='grafico-metricas')
], style={'maxWidth': '800px', 'margin': 'auto'})

# Callback para atualizar as métricas exibidas com base na localização/palavra-chave selecionada
@app.callback(
    Output('metricas-container', 'children'),
    [Input('localizacao-palavra-chave-dropdown', 'value')]
)
def atualizar_metricas(localizacao_palavra_chave_selecionada):
    metricas = metricas_por_localizacao_palavra_chave[localizacao_palavra_chave_selecionada]
    metricas_html = [
        html.H3(f"Métricas da Localização/Palavra-Chave: {localizacao_palavra_chave_selecionada}", style={'marginTop': '30px'}),
        html.P(f"Total de Itens Vendidos: {metricas['Itens Vendidos']}"),
        html.H4("Métricas por Produto:")
    ]
    for produto, valores in metricas['Produtos'].items():
        metricas_html.append(html.Hr())
        metricas_html.append(html.H4(f"Produto: {produto}"))
        metricas_html.append(html.P(f"Impressão: {valores['Impressão']}"))
        metricas_html.append(html.P(f"Cliques: {valores['Cliques']}"))
        metricas_html.append(html.P(f"Conversões: {valores['Conversões']}"))

    return metricas_html

# Callback para atualizar o gráfico com base na localização/palavra-chave selecionada
@app.callback(
    Output('grafico-metricas', 'figure'),
    [Input('localizacao-palavra-chave-dropdown', 'value')]
)
def atualizar_grafico(localizacao_palavra_chave_selecionada):
    metricas = metricas_por_localizacao_palavra_chave[localizacao_palavra_chave_selecionada]['Produtos']
    produtos = list(metricas.keys())
    impressoes = [metricas[produto]['Impressão'] for produto in produtos]
    cliques = [metricas[produto]['Cliques'] for produto in produtos]
    conversoes = [metricas[produto]['Conversões'] for produto in produtos]

    fig = go.Figure(data=[
        go.Bar(name='Impressões', x=produtos, y=impressoes),
        go.Bar(name='Cliques', x=produtos, y=cliques),
        go.Bar(name='Conversões', x=produtos, y=conversoes)
    ])

    fig.update_layout(barmode='group', title=f'Métricas por Produto para {localizacao_palavra_chave_selecionada}', xaxis_title='Produtos', yaxis_title='Quantidade')

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
