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


# Agrupar os dados para calcular o número de matrículas por dependência administrativa
df_dependencia = df.groupby('TP_DEPENDENCIA')['QT_MAT_CURSO_TEC'].sum().reset_index()
# Mapear os códigos para os nomes das dependências
df_dependencia['Dependência'] = df_dependencia['TP_DEPENDENCIA'].map({
    1: 'Federal',
    2: 'Estadual',
    3: 'Municipal',
    4: 'Privada'
})
df_dependencia.columns = ['Código', 'Número de Matrículas', 'Dependência']

# Agrupar os dados por ano
df_evolucao = df.groupby('NU_ANO_CENSO')['QT_MAT_CURSO_TEC'].sum().reset_index()
df_evolucao.columns = ['Ano', 'Número de Matrículas']

# Agrupar os dados para calcular o número de matrículas por curso
df_menor_matriculas = df.groupby('NO_CURSO_EDUC_PROFISSIONAL')['QT_MAT_CURSO_TEC'].sum().reset_index()
df_menor_matriculas.columns = ['Curso', 'Número de Matrículas']
# Ordenar pelo menor número de matrículas e pegar os 10 menores
df_menor_matriculas = df_menor_matriculas.sort_values(by='Número de Matrículas', ascending=True).head(10)



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
                    {'label': 'Matrículas por Dependência Administrativa', 'value': 'matriculas_dependencia'},
                    {'label': 'Evolução de Matrículas ao Longo dos Anos', 'value': 'evolucao_matriculas'},
                    {'label': 'Cursos com Menor Número de Matrículas', 'value': 'menor_matriculas'},


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
    ),
    dbc.Row(
        dbc.Col(
            html.P("© 2023 Suplemento Cursos Técnicos", className="text-center"),
            width=12,
            className="mt-4"
        )
    )
], fluid=True)

# Callback para os gráficos
@app.callback(
    Output('grafico-escolas', 'figure'),
    Input('dropdown-grafico', 'value')
)
def atualizar_grafico(tipo_grafico):
    
    if tipo_grafico == 'barras':
        df_regioes = df.groupby('NO_REGIAO')['NO_ENTIDADE'].count().reset_index()
        df_regioes.columns = ['Região', 'Número de Escolas']

        fig = px.bar(
            df_regioes, 
            x='Região', 
            y='Número de Escolas', 
            title="Número de Escolas por Região",
            text='Número de Escolas'  # Exibir valores diretamente
        )
        # Adicionar porcentagem nos rótulos
        fig.update_traces(
            texttemplate='%{text} (%{percent:.1%})', 
            textposition='outside'
        )
        fig.update_layout(
            uniformtext_minsize=8,
            uniformtext_mode='hide'
        )
    elif tipo_grafico == 'pizza':
        fig = px.pie(
            df_localizacao, 
            names='Zona', 
            values='Número de Escolas', 
            title="Distribuição de Escolas por Zona Urbana/Rural",
            hole=0.4  # Gráfico de pizza semi-donut
        )
        # Adicionar valores e porcentagens nos rótulos
        fig.update_traces(
            textinfo='label+percent+value',
            texttemplate='%{label}: %{value} (%{percent})'
        )

    elif tipo_grafico == 'dependencia':
        fig = px.bar(
            df_dependencia,
            x='Dependência',
            y='Número de Escolas',
            title="Comparação por Dependência Administrativa",
            text='Número de Escolas'
        )
        fig.update_traces(texttemplate='%{text} (%{percent:.1%})', textposition='outside')
        fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')

    elif tipo_grafico == 'ano_regiao':
        fig = px.line(
            df_ano_regiao,
            x='Ano',
            y='Número de Escolas',
            color='Região',
            title="Número de Escolas por Ano e Região",
            markers=True
        )
        # Adicionar rótulos nos pontos
        fig.update_traces(text='Número de Escolas', textposition='top center')
        # Ajustar o layout para melhor visualização
        fig.update_layout(hovermode='x unified')

    elif tipo_grafico == 'cursos_estado':
        fig = px.bar(
            df_cursos_estado,
            x='Estado',
            y='Número de Cursos',
            title="Número de Cursos por Estado",
            text='Número de Cursos'
        )
        # Adicionar valores como rótulos e ajustar layout
        fig.update_traces(texttemplate='%{text}', textposition='outside')
        fig.update_layout(xaxis_title="Estado", yaxis_title="Número de Cursos")

    elif tipo_grafico == 'matriculas_curso':
        fig = px.bar(
            df_matriculas_curso.head(10),  # Mostrar os 10 cursos com mais matrículas
            x='Número de Matrículas',
            y='Curso',
            orientation='h',  # Gráfico de barras horizontal
            title="Top 10 Cursos por Matrículas",
            text='Número de Matrículas'
        )
        # Adicionar rótulos com os valores e ajustar layout
        fig.update_traces(texttemplate='%{text}', textposition='outside')
        fig.update_layout(
            yaxis_title="Curso",
            xaxis_title="Número de Matrículas",
            yaxis=dict(autorange="reversed")  # Reverter ordem para exibir do maior ao menor
        )

    elif tipo_grafico == 'alunos_estado':
        fig = px.bar(
            df_alunos_estado,
            x='Estado',
            y='Número de Alunos',
            title="Número de Alunos por Estado",
            text='Número de Alunos'
        )
        # Adicionar rótulos com os valores e ajustar layout
        fig.update_traces(texttemplate='%{text}', textposition='outside')
        fig.update_layout(xaxis_title="Estado", yaxis_title="Número de Alunos")

    elif tipo_grafico == 'alunos_curso':
        fig = px.bar(
            df_alunos_curso.head(10),  # Mostrar os 10 cursos com mais alunos
            x='Número de Alunos',
            y='Curso',
            orientation='h',  # Gráfico de barras horizontal
            title="Top 10 Cursos por Número de Alunos",
            text='Número de Alunos'
        )
        # Adicionar rótulos com os valores e ajustar layout
        fig.update_traces(texttemplate='%{text}', textposition='outside')
        fig.update_layout(
            yaxis_title="Curso",
            xaxis_title="Número de Alunos",
            yaxis=dict(autorange="reversed")  # Reverter ordem para exibir do maior ao menor
        )

    elif tipo_grafico == 'cursos_modalidade':
    # Transformar os dados em formato longo para barras empilhadas
        df_long = df_cursos_modalidade.melt(
            id_vars=['Estado'],
            value_vars=['Ensino Médio Integrado', 'Educação Subsequente'],
            var_name='Modalidade',
            value_name='Número de Cursos'
        )
        
        # Criar o gráfico de barras empilhadas
        fig = px.bar(
            df_long,
            x='Estado',
            y='Número de Cursos',
            color='Modalidade',
            title="Número de Cursos Técnicos por Modalidade e Estado",
            text='Número de Cursos'
        )
        # Ajustar layout e rótulos
        fig.update_traces(texttemplate='%{text}', textposition='inside')
        fig.update_layout(
            xaxis_title="Estado",
            yaxis_title="Número de Cursos",
            barmode='stack'  # Empilhamento das barras
        )

    elif tipo_grafico == 'matriculas_dependencia':
        fig = px.pie(
            df_dependencia,
            names='Dependência',
            values='Número de Matrículas',
            title="Distribuição de Matrículas por Dependência Administrativa"
        )
        # Adicionar porcentagens e valores diretamente no gráfico
        fig.update_traces(
            textinfo='label+percent+value',
            texttemplate='%{label}: %{value} (%{percent})'
        )
        fig.update_layout(
            legend_title="Dependência Administrativa"
        )

    elif tipo_grafico == 'evolucao_matriculas':
        fig = px.line(
            df_evolucao,
            x='Ano',
            y='Número de Matrículas',
            title="Evolução de Matrículas ao Longo dos Anos",
            markers=True  # Adiciona marcadores nos pontos
        )
        # Adicionar rótulos nos pontos
        fig.update_traces(text='Número de Matrículas', textposition='top center')
        fig.update_layout(
            xaxis_title="Ano",
            yaxis_title="Número de Matrículas",
            hovermode='x unified'
        )

    elif tipo_grafico == 'menor_matriculas':
        fig = px.bar(
            df_menor_matriculas,
            x='Número de Matrículas',
            y='Curso',
            orientation='h',  # Gráfico de barras horizontais
            title="Top 10 Cursos com Menor Número de Matrículas",
            text='Número de Matrículas'
        )
        # Adicionar rótulos com os valores e ajustar layout
        fig.update_traces(texttemplate='%{text}', textposition='outside')
        fig.update_layout(
            xaxis_title="Número de Matrículas",
            yaxis_title="Curso",
            yaxis=dict(autorange="reversed")  # Reverter ordem para exibir do menor para o maior
        )



    else:
        fig = {}
    return fig

# Executar o servidor
if __name__ == "__main__":
    app.run_server(debug=True)
