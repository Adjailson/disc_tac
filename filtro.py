from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

# Inicializar o app com Bootstrap para estilo
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Carregar a base real
caminho_base = "base/suplemento_cursos_tecnicos_2023.csv"
df = pd.read_csv(caminho_base, sep=";", encoding="latin1")

# Limpar e preparar os dados


df_localizacao = df.groupby('TP_LOCALIZACAO')['NO_ENTIDADE'].count().reset_index()
df_localizacao['Zona'] = df_localizacao['TP_LOCALIZACAO'].map({1: 'Urbana', 2: 'Rural'})
df_localizacao.columns = ['TP_LOCALIZACAO', 'Número de Escolas', 'Zona']

#Comparação por Dependência Administrativa (Pública, privada , federal..)
df_dependencia = df.groupby('TP_DEPENDENCIA')['NO_ENTIDADE'].count().reset_index()
df_dependencia['Dependência'] = df_dependencia['TP_DEPENDENCIA'].map({
    1: 'Federal', 2: 'Estadual', 3: 'Municipal', 4: 'Privada'
})
df_dependencia.columns = ['TP_DEPENDENCIA', 'Número de Escolas', 'Dependência']

# Agrupar os dados por Ano e Região
df_ano_regiao = df.groupby(['NU_ANO_CENSO', 'NO_REGIAO'])['NO_ENTIDADE'].count().reset_index()
df_ano_regiao.columns = ['Ano', 'Região', 'Número de Escolas']

# Agrupar os dados para calcular o número de cursos por estado
df_cursos_estado = df.groupby('NO_UF')['NO_ENTIDADE'].count().reset_index()
df_cursos_estado.columns = ['Estado', 'Número de Cursos']

# Agrupar os dados para calcular o número de matrículas por curso
df_matriculas_curso = df.groupby('NO_CURSO_EDUC_PROFISSIONAL')['QT_MAT_CURSO_TEC'].sum().reset_index()
df_matriculas_curso.columns = ['Curso', 'Número de Matrículas']
df_matriculas_curso = df_matriculas_curso.sort_values(by='Número de Matrículas', ascending=False)

# Agrupar os dados para calcular o número de alunos por estado
df_alunos_estado = df.groupby('NO_UF')['QT_MAT_CURSO_TEC'].sum().reset_index()
df_alunos_estado.columns = ['Estado', 'Número de Alunos']

# Agrupar os dados para calcular o número de alunos por curso
df_alunos_curso = df.groupby('NO_CURSO_EDUC_PROFISSIONAL')['QT_MAT_CURSO_TEC'].sum().reset_index()
df_alunos_curso.columns = ['Curso', 'Número de Alunos']
df_alunos_curso = df_alunos_curso.sort_values(by='Número de Alunos', ascending=False)

# Agrupar os dados por estado e modalidade
df_cursos_modalidade = df.groupby('NO_UF').agg({
    'QT_CURSO_TEC_CT': 'sum',
    'QT_CURSO_TEC_SUBS': 'sum'
}).reset_index()
# Ajustar os nomes das colunas
df_cursos_modalidade.columns = ['Estado', 'Ensino Médio Integrado', 'Educação Subsequente']



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
                id='dropdown-grafico',
                options=[
                    {'label': 'Número de Escolas por Região', 'value': 'barras'},
                    {'label': 'Número de Escolas por Zona (Urbana/Rural)', 'value': 'pizza'},
                    {'label': 'Comparação por Dependência Administrativa', 'value': 'dependencia'},
                    {'label': 'Análise por Ano e Região', 'value': 'ano_regiao'},
                    {'label': 'Número de Cursos por Estado', 'value': 'cursos_estado'},
                    {'label': 'Matrículas por Curso', 'value': 'matriculas_curso'},
                    {'label': 'Número de Alunos por Estado', 'value': 'alunos_estado'},
                    {'label': 'Número de Alunos por Curso', 'value': 'alunos_curso'},
                    {'label': 'Número de Cursos Técnicos por Modalidade', 'value': 'cursos_modalidade'},


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
            dcc.Dropdown(
                id='dropdown-estado',
                options=[{'label': uf, 'value': uf} for uf in df['SG_UF'].unique()],
                placeholder="Selecione um estado",
                multi=True,  # Permitir seleção de múltiplos estados
                className="mb-4"
            ),
            width=12
        )
    ),



    dbc.Row(
        dbc.Col(
            dcc.Graph(id='grafico-escolas'),
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
    Output('grafico-escolas', 'figure'),
    [Input('dropdown-grafico', 'value'),
     Input('dropdown-estado', 'value')]
)
def atualizar_grafico(tipo_grafico, estados_selecionados):
    # Filtrar o DataFrame com base nos estados selecionados
    df_filtrado = df
    if estados_selecionados:
        df_filtrado = df[df['SG_UF'].isin(estados_selecionados)]

    # Lógica para os diferentes tipos de gráficos
    if tipo_grafico == 'barras':
        df_regioes = df_filtrado.groupby('NO_REGIAO')['NO_ENTIDADE'].count().reset_index()
        fig = px.bar(
            df_regioes,
            x='NO_REGIAO',
            y='NO_ENTIDADE',
            title="Número de Escolas por Região",
            text='NO_ENTIDADE'
        )
        fig.update_traces(texttemplate='%{text}', textposition='outside')
        fig.update_layout(xaxis_title="Região", yaxis_title="Número de Escolas")

    elif tipo_grafico == 'cursos_modalidade':
        df_cursos_modalidade = df_filtrado.groupby('NO_UF').agg({
            'QT_CURSO_TEC_CT': 'sum',
            'QT_CURSO_TEC_SUBS': 'sum'
        }).reset_index()
        df_cursos_modalidade.columns = ['Estado', 'Ensino Médio Integrado', 'Educação Subsequente']

        df_long = df_cursos_modalidade.melt(
            id_vars=['Estado'],
            value_vars=['Ensino Médio Integrado', 'Educação Subsequente'],
            var_name='Modalidade',
            value_name='Número de Cursos'
        )

        fig = px.bar(
            df_long,
            x='Estado',
            y='Número de Cursos',
            color='Modalidade',
            title="Número de Cursos Técnicos por Modalidade e Estado",
            text='Número de Cursos'
        )
        fig.update_traces(texttemplate='%{text}', textposition='inside')
        fig.update_layout(xaxis_title="Estado", yaxis_title="Número de Cursos", barmode='stack')

    # Adicionar outros tipos de gráficos conforme necessário

    else:
        fig = {}
    
    return fig


