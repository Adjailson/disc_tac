from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

# Inicializar o app com Bootstrap para estilo
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Carregar a base real
caminho_base = "base/suplemento_cursos_tecnicos_2023.csv"
dados = pd.read_csv(caminho_base, sep=";", encoding="latin1")

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
                        color="success", size="sm", className="mb-6 me-2"),
                width="auto"
            ),

            dbc.Col(
                dbc.Button("Mais informações", 
                        href="https://github.com/Adjailson/disc_tac/blob/main/base/RelatorioAdjailsonDisc-TAC.pdf",
                        target="_blank",
                        color="primary", size="sm", className="mb-6"),
                width="auto"
            )
        ],
        justify="center",
        className="mb-4"
    ),

    dbc.Row(
        dbc.Col(
            dcc.Dropdown(
                id='dropdown-regiao',
                options=[
                    {'label': 'Cursos com Maior Número de Matrículas por Região', 'value': 'maior_cursos_regiao'},
                    {'label': 'Cursos com Maior Número de Matrículas por Estado', 'value': 'maior_cursos_estado'},
                ],
                value='barras',
                placeholder='Escolha o tipo de gráfico',
                multi=False
            ),
            width=6,
            className="mb-4"
        )
    ),


    dbc.Row(
        dbc.Col(
            dcc.Dropdown(
                id='dropdown-estado',
                options=[{'label': uf, 'value': uf} for uf in dados['SG_UF'].unique()],
                placeholder="Selecione um estado",
                multi=False,  # Permitir seleção de múltiplos estados
                className="mb-4"
            ),
            width=6
        )
    ),

    dbc.Row(
        dbc.Col(
            dcc.Graph(id='grafico-filtro'),
            width=12
        )
    ),
    dbc.Row(
        dbc.Col(
            html.P("© 2023 Suplemento Cursos Técnicos", className="text-center"),
            width=12,
            className="mt-4"
        )
    )
], fluid=True)

@app.callback(
    Output('grafico-filtro', 'figure'),
    [Input('dropdown-regiao', 'value'),
     Input('dropdown-estado', 'value')]
)
def atualizar_grafico(tipo_grafico, estados_selecionados):
    # Filtrar o DataFrame com base nos estados selecionados
    #df_filtrado = dados
    print(estados_selecionados)
    if estados_selecionados:
        df_filtrado = dados[dados['SG_UF'].isin(estados_selecionados)]
        print(df_filtrado)

    #Select - Cursos com Maior Número de Matrículas por Região
    if tipo_grafico == 'maior_cursos_regiao':
        df_cursos_regiao = dados.groupby(['NO_REGIAO', 'NO_CURSO_EDUC_PROFISSIONAL'])['QT_MAT_CURSO_TEC'].sum().reset_index()
        df_cursos_regiao.columns = ['Região', 'Curso', 'Número de Matrículas']

        df_top_cursos = df_cursos_regiao.sort_values(by=['Região', 'Número de Matrículas'], ascending=[True, False])
        df_top_cursos = df_top_cursos.groupby('Região').head(5)  # Pega os 5 maiores por região

        fig = px.bar(
            df_top_cursos,
            x='Região',
            y='Número de Matrículas',
            color='Curso',
            title="Cursos com Maior Número de Matrículas por Região",
            text='Número de Matrículas'
        )
        # Ajustar layout para gráfico empilhado
        fig.update_layout(
            xaxis_title="Região",
            yaxis_title="Número de Matrículas",
            barmode='stack',  # Empilhamento das barras
            legend_title="Curso"
        )

    #Select - Cursos com Maior Número de Matrículas por Estado
    elif tipo_grafico == 'maior_cursos_estado':
        df_cursos_estado = dados.groupby(['SG_UF', 'NO_CURSO_EDUC_PROFISSIONAL'])['QT_MAT_CURSO_TEC'].sum().reset_index()
        df_cursos_estado.columns = ['Estado', 'Curso', 'Número de Matrículas']

        df_top_cursos = df_cursos_estado.sort_values(by=['Estado', 'Número de Matrículas'], ascending=[True, False])
        df_top_cursos = df_top_cursos.groupby('Estado').head(3)  # Pega os 3 maiores por região

        fig = px.bar(
            df_top_cursos,
            x='Estado',
            y='Número de Matrículas',
            color='Curso',
            title="Cursos com Maior Número de Matrículas por Estado",
            text='Número de Matrículas',
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        # Ajustar layout para gráfico empilhado
        fig.update_layout(
            xaxis_title="Estado",
            yaxis_title="Número de Matrículas",
            barmode='stack',  # Empilhamento das barras
            legend_title="Curso"
        )

    else:
        fig = {}
    
    return fig

# Executar o servidor localhost
if __name__ == "__main__":
    app.run_server(debug=True)


