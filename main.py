from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

# Inicializar o app com Bootstrap para estilo
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Dados fictícios representando número de escolas por região
data = {
    'Região': ['Norte', 'Nordeste', 'Centro-Oeste', 'Sudeste', 'Sul'],
    'Número de Escolas': [120, 250, 90, 320, 150]
}
df = pd.DataFrame(data)

# Layout do app
app.layout = dbc.Container([
    dbc.Row(
        dbc.Col(
            html.H1("Suplemento Cursos Técnicos 2023", className="text-center mb-4"),
            width=12
        )
    ),
    dbc.Row(
        [
            dbc.Col(
                dbc.Button("Acesso a base", 
                        href="https://github.com/Adjailson/disc_tac/blob/main/base/suplemento_cursos_tecnicos_2023.csv", 
                        target="_blank",
                        color="success", size="sm", className="mb-6"),
                width="auto"
            ),

            dbc.Col(
                dbc.Button("Mais informações", 
                        href="base/RelatorioAdjailsonDisc-TAC.pdf",
                        target="_blank",
                        color="primary", size="sm", className="mb-6"),
                width="auto"
            )

        ],justify="center", className="mb-4"

    ),

    dbc.Row(
        dbc.Col(
            dcc.Dropdown(
                id='dropdown-grafico',
                options=[
                    {'label': 'Número de Escolas por Região', 'value': 'barras'},
                    {'label': 'Número de Escolas por Zona (Urbana/Rural)', 'value': 'pizza'}
                ],
                value='barras',
                placeholder='Escolha o tipo de gráfico',
                multi=False
            ),
            width=12,
            className="mb-4"
        )
    ),
    dbc.Row(
        dbc.Col(
            dcc.Graph(id='grafico-escolas'),
            width=12
        )
    )
], fluid=True)

# Os Callback do gráfico
@app.callback(
    Output('grafico-escolas', 'figure'),
    Input('dropdown-grafico', 'value')
)
def atualizar_grafico(tipo_grafico):
    if tipo_grafico == 'barras':
        fig = px.bar(df, x='Região', y='Número de Escolas', title="Número de Escolas por Região")
    elif tipo_grafico == 'pizza':
        fig = px.pie(df, names='Região', values='Número de Escolas', title="Número de Escolas Zona Urbana/Rural")
    else:
        fig = {}
    return fig

# Executar o servidor
if __name__ == "__main__":
    app.run_server(debug=True)
