import dash
from dash import dcc, html, dash_table, Input, Output
import pandas as pd
import plotly.graph_objs as go

# Dados

data = {
    'Ano': [2025, 2026, 2027, 2028, 2029]*3,
    'Crescimento': ['5%']*5 + ['8%']*5 + ['12%']*5,
    'Total_Projetado': [
        2935815, 3082606, 3236736, 3398573, 3568502,
        3019696, 3261272, 3522173, 3803947, 4108263,
        3104409, 3476937, 3894178, 4361499, 4874473
    ],
    'Desconto (%)': [45, 55, 50, 60, 65]*3,
    'Total_com_Transacao': [
        2264045, 2220501, 2413817, 2361695, 2389053,
        2328732, 2349199, 2626684, 2643393, 2750414,
        2392765, 2500832, 2896075, 3020323, 3246702
    ]
}
projecoes = pd.DataFrame(data)

# App Dash
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("📊 Painel de Projeções PGFN e Simulações Tributárias"),
    html.Label("Selecione o cenário de crescimento:"),
    dcc.Dropdown(
        id='crescimento-dropdown',
        options=[{'label': c, 'value': c} for c in sorted(projecoes['Crescimento'].unique())],
        value=sorted(projecoes['Crescimento'].unique())[0],
        clearable=False
    ),
    html.Br(),
    html.H3("Evolução do Débito: Projeção x Transação"),
    dcc.Graph(id='comparativo-graph'),
    html.H3("Tabela de Projeções Detalhada"),
    dash_table.DataTable(
        id='tabela-projecoes',
        columns=[
            {"name": "Ano", "id": "Ano"},
            {"name": "Total Projetado", "id": "Total_Projetado"},
            {"name": "Total com Transação", "id": "Total_com_Transacao"},
            {"name": "Desconto (%)", "id": "Desconto (%)"}
        ],
        style_cell={'textAlign': 'center'},
        style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold'},
        style_data_conditional=[
            {
                'if': {'column_id': 'Desconto (%)'},
                'backgroundColor': 'rgb(240, 248, 255)'
            }
        ],
        page_size=10
    )
])

@app.callback(
    [Output('comparativo-graph', 'figure'), Output('tabela-projecoes', 'data')],
    [Input('crescimento-dropdown', 'value')]
)
def update_dashboard(crescimento):
    df_filtrado = projecoes[projecoes['Crescimento'] == crescimento]
    # Gráfico
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_filtrado['Ano'],
        y=df_filtrado['Total_Projetado'],
        mode='lines+markers',
        name='Total Projetado',
        line=dict(width=2)
    ))
    fig.add_trace(go.Scatter(
        x=df_filtrado['Ano'],
        y=df_filtrado['Total_com_Transacao'],
        mode='lines+markers',
        name='Com Transação',
        line=dict(width=2)
    ))
    fig.update_layout(
        yaxis_title="Valor (R$)",
        xaxis_title="Ano",
        title="Comparativo Anual",
        legend_title_text='',
        yaxis_tickformat=',.0f',
        yaxis_tickprefix='R$'
    )
    # Tabela formatada
    df_formatado = df_filtrado.copy()
    df_formatado['Total_Projetado'] = df_formatado['Total_Projetado'].apply(lambda x: f'R${x:,.0f}'.replace(",", "."))
    df_formatado['Total_com_Transacao'] = df_formatado['Total_com_Transacao'].apply(lambda x: f'R${x:,.0f}'.replace(",", "."))
    return fig, df_formatado[['Ano', 'Total_Projetado', 'Total_com_Transacao', 'Desconto (%)']].to_dict('records')

if __name__ == '__main__':
    app.run_server(debug=True)
