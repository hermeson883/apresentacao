import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Carregar os dados
df = pd.read_excel("resumo_semanal.xlsx")

# Configurar a página
st.set_page_config(layout="wide")

# Título
st.markdown("<h1 style='text-align: center;'>Preços de Gasolina Ao longo do Brasil</h1>", unsafe_allow_html=True)

# Criar colunas
col1, col2 = st.columns(2)
col3, col4 = st.columns(2)

with col1:
    # Filtro por Região
    selected_region = st.selectbox('Filtro Por Região', options=['Todas'] + list(df['REGIAO'].unique()))

    # Filtrar o DataFrame com base na região selecionada
    if selected_region != 'Todas':
        df = df[df['REGIAO'] == selected_region]
    else:
        df = df

    # Contar a quantidade de registros por região
    df_filter = df.groupby(by='REGIAO', as_index=False).sum('NÚMERO DE POSTOS PESQUISADOS')

    # Gráfico de pizza com percentuais
    fig = px.pie(
        df_filter, 
        names="REGIAO", 
        values="NÚMERO DE POSTOS PESQUISADOS", 
        title="Quantidade de Postos Pesquisados por Região", 
        color='REGIAO',
        hole=0.5
    )

    st.plotly_chart(fig, use_container_width=True)

with col2:

    # Filtro por Região
    selected_estate = st.selectbox('Filtro Por Estado', options=['Todas'] + list(df['ESTADOS'].unique()))

    # Filtrar o DataFrame com base na região selecionada
    if selected_estate != 'Todas':
        df = df[df['ESTADOS'] == selected_estate]
    else:
        df = df

    # Agrupar por ESTADOS e somar o PREÇO MÁXIMO REVENDA
    df_max_value = df.groupby(by='ESTADOS', as_index=False).sum('PREÇO MÁXIMO REVENDA')

    # Ordenar por PREÇO MÁXIMO REVENDA
    df_max_value = df_max_value.sort_values(by='PREÇO MÁXIMO REVENDA', ascending=False)

    # Gráfico de barras
    fig = px.bar(
        df_max_value, 
        x='ESTADOS',
        y='PREÇO MÁXIMO REVENDA',
        title="Preço Máximo de Revenda por Estado",
        text="PREÇO MÁXIMO REVENDA"
    )

    fig.update_traces(
        texttemplate='%{text:.2f}',
        insidetextanchor='middle',          # Centraliza verticalmente
        marker=dict(color='#12A3FE'),
        textfont=dict(color='white', size=14)  # Contraste e tamanho do texto
    )

    st.plotly_chart(fig, use_container_width=True)

with col3:
    # Agrupar por ESTADOS e somar o PREÇO MÍNIMO REVENDA
    df_min_value = df.groupby(by='ESTADOS', as_index=False).sum('PREÇO MÍNIMO REVENDA')

    # Ordenar por PREÇO MÍNIMO REVENDA
    df_min_value = df_min_value.sort_values(by='PREÇO MÍNIMO REVENDA', ascending=True)

    # Gráfico de dispersão
    fig = px.scatter(
        df_min_value,
        x="ESTADOS",
        y="PREÇO MÍNIMO REVENDA",
        title="Preço Mínimo de Revenda por Estado",

    )

    st.plotly_chart(fig, use_container_width=True)

with col4:
    # Agrupar por REGIAO e ESTADOS, calculando a média do PREÇO MÉDIO REVENDA
    df_avg_value = df.groupby(by=['REGIAO', 'ESTADOS'], as_index=False).mean('PREÇO MÉDIO REVENDA')

    # Gráfico de sunburst
    fig = px.sunburst(
        df_avg_value,
        path=['REGIAO', 'ESTADOS'],  # Define a hierarquia: regiões -> estados
        values='PREÇO MÉDIO REVENDA',  # Valores associados aos nós
        title="Preço Médio de Gasolina por Região e Estado",
        color='PREÇO MÉDIO REVENDA',  # Colorir com base no preço
        color_continuous_scale=px.colors.sequential.Blues,  # Escala de cores
        labels={'PREÇO MÉDIO REVENDA': 'Preço Médio (R$)'},
    )


    fig.update_traces(
        textinfo='label+value',  # Pode usar: 'label+percent entry+value'
        textfont=dict(size=14, color='black')  # Opcional
    )

    # Ajustar o layout
    fig.update_layout(
        margin=dict(t=50, l=0, r=0, b=0),

    )

    # Exibir no Streamlit
    st.plotly_chart(fig, use_container_width=True)