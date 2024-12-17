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
                id='dropdown-grafico',
                options=[
                    {'label': 'Número de Escolas por Região', 'value': 'regiao'},
                    {'label': 'Número de Escolas por Zona (Urbana/Rural)', 'value': 'zona'},
                    {'label': 'Número por Dependência Administrativa', 'value': 'dependencia'},
                    {'label': 'Análise por Ano e Região', 'value': 'ano_regiao'},
                    {'label': 'Número de Cursos por Estado', 'value': 'cursos_estado'},
                    {'label': 'Matrículas por Curso', 'value': 'matriculas_curso'},
                    {'label': 'Número de Alunos por Estado', 'value': 'alunos_estado'},
                    {'label': 'Número de Alunos por Curso', 'value': 'alunos_curso'},
                    {'label': 'Número de Cursos Técnicos por Modalidade', 'value': 'cursos_modalidade'},
                    {'label': 'Matrículas por Dependência Administrativa', 'value': 'matriculas_dependencia'},
                    {'label': 'Evolução de Matrículas ao Longo dos Anos', 'value': 'evolucao_matriculas'},
                    {'label': 'Cursos com Maior Número de Matrículas por Região', 'value': 'maior_cursos_regiao'},
                    {'label': 'Cursos com Maior Número de Matrículas por Estado', 'value': 'maior_cursos_estado'},
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
    
    #Select - Número de Escolas por Região
    if tipo_grafico == 'regiao':
        
        df_regioes = dados.groupby('NO_REGIAO')['NO_ENTIDADE'].count().reset_index()
        df_regioes.columns = ['Região', 'Número de Escolas']

        
        df_regioes['Porcentagem'] = (df_regioes['Número de Escolas'] / df_regioes['Número de Escolas'].sum()) * 100

        # Criar o gráfico
        fig = px.bar(
            df_regioes, 
            x='Região', 
            y='Número de Escolas', 
            title="Número de Escolas por Região",
            text=df_regioes.apply(lambda row: f"{row['Número de Escolas']} ({row['Porcentagem']:.1f}%)", axis=1),  # Valores + Porcentagem
            color='Região',
            color_discrete_sequence=px.colors.qualitative.Set2
        )

        # Ajustar posição e layout do texto
        fig.update_traces(
            textposition='outside'
        )
        fig.update_layout(
            xaxis_title="Região",
            yaxis_title="Número de Escolas",
            uniformtext_minsize=8,
            uniformtext_mode='hide'
        )

    #Select - Número de Escolas por Zona (Urbana/Rural)
    elif tipo_grafico == 'zona':
        # Número de escolas por Zona
        df_localizacao = dados.groupby('TP_LOCALIZACAO')['NO_ENTIDADE'].count().reset_index()
        df_localizacao['Zona'] = df_localizacao['TP_LOCALIZACAO'].map({1: 'Urbana', 2: 'Rural'})
        df_localizacao.columns = ['TP_LOCALIZACAO', 'Número de Escolas', 'Zona']

        fig = px.pie(
            df_localizacao, 
            names='Zona', 
            values='Número de Escolas', 
            title="Distribuição de Escolas por Zona Urbana/Rural",
            hole=0.4,  # Gráfico de pizza semi-donut
            color='Zona',
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        # Adicionar valores e porcentagens nos rótulos
        fig.update_traces(
            textinfo='label+percent+value',
            texttemplate='%{label}: %{value} (%{percent})'
        )

    #Número por Dependência Administrativa
    elif tipo_grafico == 'dependencia':
        #Comparação por Dependência Administrativa (Pública, privada , federal..)
        df_dependencia = dados.groupby('TP_DEPENDENCIA')['NO_ENTIDADE'].count().reset_index()
        df_dependencia['Dependência'] = df_dependencia['TP_DEPENDENCIA'].map({
            1: 'Federal', 2: 'Estadual', 3: 'Municipal', 4: 'Privada'
        })
        df_dependencia.columns = ['TP_DEPENDENCIA', 'Número de Escolas', 'Dependência']
        # Calcular a porcentagem
        df_dependencia['Porcentagem'] = (df_dependencia['Número de Escolas'] / df_dependencia['Número de Escolas'].sum()) * 100

        # Criar o gráfico
        fig = px.bar(
            df_dependencia,
            x='Dependência',
            y='Número de Escolas',
            title="Comparação por Dependência Administrativa",
            text=df_dependencia.apply(lambda row: f"{row['Número de Escolas']} ({row['Porcentagem']:.1f}%)", axis=1),
            color='Dependência',
            color_discrete_sequence=px.colors.qualitative.Set2
        )

        # Ajustar a posição do texto e layout
        fig.update_traces(textposition='outside')
        fig.update_layout(
            xaxis_title="Dependência Administrativa",
            yaxis_title="Número de Escolas",
            uniformtext_minsize=8,
            uniformtext_mode='hide'
        )


    elif tipo_grafico == 'ano_regiao':

        # Agrupar os dados por Ano e Região
        df_ano_regiao = dados.groupby(['NU_ANO_CENSO', 'NO_REGIAO'])['NO_ENTIDADE'].count().reset_index()
        df_ano_regiao.columns = ['Ano', 'Região', 'Número de Escolas']

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
        # Agrupar os dados para calcular o número de cursos por estado
        df_cursos_estado = dados.groupby('NO_UF')['NO_ENTIDADE'].count().reset_index()
        df_cursos_estado.columns = ['Estado', 'Número de Cursos']

        fig = px.bar(
            df_cursos_estado,
            x='Estado',
            y='Número de Cursos',
            title="Número de Cursos por Estado",
            text='Número de Cursos',
            color='Estado',
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        # Adicionar valores como rótulos e ajustar layout
        fig.update_traces(texttemplate='%{text}', textposition='outside')
        fig.update_layout(xaxis_title="Estado", yaxis_title="Número de Cursos")

    elif tipo_grafico == 'matriculas_curso':
        # Agrupar os dados para calcular o número de matrículas por curso
        df_matriculas_curso = dados.groupby('NO_CURSO_EDUC_PROFISSIONAL')['QT_MAT_CURSO_TEC'].sum().reset_index()
        df_matriculas_curso.columns = ['Curso', 'Número de Matrículas']
        df_matriculas_curso = df_matriculas_curso.sort_values(by='Número de Matrículas', ascending=False)

        fig = px.bar(
            df_matriculas_curso.head(10),  # Mostrar os 10 cursos com mais matrículas
            x='Número de Matrículas',
            y='Curso',
            orientation='h',  # Gráfico de barras horizontal
            title="Top 10 Cursos por Matrículas",
            text='Número de Matrículas',
            color='Curso',
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        # Adicionar rótulos com os valores e ajustar layout
        fig.update_traces(texttemplate='%{text}', textposition='outside')
        fig.update_layout(
            yaxis_title="Curso",
            xaxis_title="Número de Matrículas",
            #yaxis=dict(autorange="reversed")  # Reverter ordem para exibir do maior ao menor
        )

    #Select  - Número de Alunos por Estado
    elif tipo_grafico == 'alunos_estado':
        # Agrupar os dados para calcular o número de alunos por estado
        df_alunos_estado = dados.groupby('NO_UF')['QT_MAT_CURSO_TEC'].sum().reset_index()
        df_alunos_estado.columns = ['Estado', 'Número de Alunos']

        fig = px.bar(
            df_alunos_estado,
            x='Estado',
            y='Número de Alunos',
            title="Número de Alunos por Estado",
            text='Número de Alunos',
            color='Estado',
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        # Adicionar rótulos com os valores e ajustar layout
        fig.update_traces(texttemplate='%{text}', textposition='outside')
        fig.update_layout(xaxis_title="Estado", yaxis_title="Número de Alunos")

    #select - Número de Alunos por Curso
    elif tipo_grafico == 'alunos_curso':
        # Agrupar os dados para calcular o número de alunos por curso
        df_alunos_curso = dados.groupby('NO_CURSO_EDUC_PROFISSIONAL')['QT_MAT_CURSO_TEC'].sum().reset_index()
        df_alunos_curso.columns = ['Curso', 'Número de Alunos']
        df_alunos_curso = df_alunos_curso.sort_values(by='Número de Alunos', ascending=False)

        fig = px.bar(
            df_alunos_curso.head(10),  # Mostrar os 10 cursos com mais alunos
            x='Número de Alunos',
            y='Curso',
            orientation='h',  # Gráfico de barras horizontal
            title="Top 10 Cursos por Número de Alunos",
            text='Número de Alunos',
            color='Curso',
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        # Adicionar rótulos com os valores e ajustar layout
        fig.update_traces(texttemplate='%{text}', textposition='outside')
        fig.update_layout(
            yaxis_title="Curso",
            xaxis_title="Número de Alunos",
            
        )

    #Select - Número de Cursos Técnicos por Modalidade
    elif tipo_grafico == 'cursos_modalidade':
        # Agrupar os dados por estado e modalidade
        df_cursos_modalidade = dados.groupby('NO_UF').agg({
            'QT_CURSO_TEC_CT': 'sum',
            'QT_CURSO_TEC_SUBS': 'sum'
        }).reset_index()
        # Ajustar os nomes das colunas
        df_cursos_modalidade.columns = ['Estado', 'Ensino Médio Integrado', 'Educação Subsequente']
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
            text='Número de Cursos',
            color_discrete_sequence=['#00FA9A', '#00BFFF']
        )
        # Ajustar layout e rótulos
        fig.update_traces(texttemplate='%{text}', textposition='inside')
        fig.update_layout(
            xaxis_title="Estado",
            yaxis_title="Número de Cursos",
            barmode='stack'  # Empilhamento das barras,
        )

    elif tipo_grafico == 'matriculas_dependencia':
        
        # Agrupar os dados por dependência administrativa e somar o número de matrículas
        df_matriculas_dependencia = dados.groupby('TP_DEPENDENCIA')['QT_MAT_CURSO_TEC'].sum().reset_index()

        # Mapear os códigos de dependência administrativa para nomes mais intuitivos
        df_matriculas_dependencia['Dependência'] = df_matriculas_dependencia['TP_DEPENDENCIA'].map({
            1: 'Federal', 2: 'Estadual', 3: 'Municipal', 4: 'Privada'
        })

        # Renomear as colunas
        df_matriculas_dependencia.columns = ['Código', 'Número de Matrículas', 'Dependência']
        # Paleta de cores personalizada
        cores_personalizadas = ['#1f77b4', '#ff7f0e','#d62728','#2ca02c']  # Azul, Laranja, Vermelho e Verde

        # Criar o gráfico de barras
        fig = px.bar(
            df_matriculas_dependencia,
            x='Dependência',
            y='Número de Matrículas',
            title="Número de Matrículas por Dependência Administrativa",
            text='Número de Matrículas',  # Exibe o número de matrículas nos rótulos
            color='Dependência',  # Adiciona cores distintas
            color_discrete_sequence=cores_personalizadas  # Aplicar paleta de cores
        )

        # Ajustar a posição dos rótulos e layout
        fig.update_traces(texttemplate='%{text}', textposition='outside')
        fig.update_layout(
            xaxis_title="Dependência Administrativa",
            yaxis_title="Número de Matrículas",
            uniformtext_minsize=8,
            uniformtext_mode='hide'
        )

    #Select - Evolução de Matrículas ao Longo dos Anos
    elif tipo_grafico == 'evolucao_matriculas':
        # Agrupar os dados por ano
        df_evolucao = dados.groupby('NU_ANO_CENSO')['QT_MAT_CURSO_TEC'].sum().reset_index()
        df_evolucao.columns = ['Ano', 'Número de Matrículas']
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

    #Select - Cursos com Menor Número de Matrículas
    elif tipo_grafico == 'menor_matriculas':
        # Agrupar os dados para calcular o número de matrículas por curso
        df_menor_matriculas = dados.groupby('NO_CURSO_EDUC_PROFISSIONAL')['QT_MAT_CURSO_TEC'].sum().reset_index()
        df_menor_matriculas.columns = ['Curso', 'Número de Matrículas']
        # Ordenar pelo menor número de matrículas e pegar os 10 menores
        df_menor_matriculas = df_menor_matriculas.sort_values(by='Número de Matrículas', ascending=True).head(10)

        fig = px.bar(
            df_menor_matriculas,
            x='Número de Matrículas',
            y='Curso',
            orientation='h',  # Gráfico de barras horizontais
            title="Top 10 Cursos com Menor Número de Matrículas",
            text='Número de Matrículas',
            color='Curso',
            color_discrete_sequence=px.colors.qualitative.Set2  # Paleta de cores do Plotly
        )
        # Adicionar rótulos com os valores e ajustar layout
        fig.update_traces(texttemplate='%{text}', textposition='outside')
        fig.update_layout(
            xaxis_title="Número de Matrículas",
            yaxis_title="Curso",
            #yaxis=dict(autorange="reversed")  # Reverter ordem para exibir do menor para o maior
        )

    #Select - Cursos com Maior Número de Matrículas por Região
    elif tipo_grafico == 'maior_cursos_regiao':
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
