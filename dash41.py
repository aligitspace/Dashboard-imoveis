import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.linear_model import LinearRegression

# Função para carregar os dados
def carregar_dados():
    dados = {
        "Ano": [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023],
        "1 Dormitório Bom (Média)": [22.5, 22.2, 21.85, 23.11, 22.84, 25.88, 25.48, 27.09, 30.34],
        "1 Dormitório Regular (Média)": [24.68, 22.87, 24.4, 25.58, 25.16, 25.92, 26.24, 28.95, 30.89],
        "2 Dormitórios Bom (Média)": [21.7, 19.81, 21.34, 22.16, 22.32, 22.92, 23.82, 26.39, 28.37],
        "2 Dormitórios Regular (Média)": [20.8, 17.73, 21.64, 21.53, 24.81, 22.14, 21.22, 23.68, 24.89],
        "3 Dormitórios Bom (Média)": [18.79, 15.61, 18.99, 18.8, 21.87, 19.79, 18.36, 20.24, 21.29],
        "3 Dormitórios Regular (Média)": [19.32, 16.34, 19.58, 19.13, 22.04, 20.13, 18.94, 21.02, 21.67]
    }
    df = pd.DataFrame(dados)
    return df

# Função para exibir a tabela com duas casas decimais e mês de referência
def exibir_tabela(df):
    st.subheader("Tabela de Valores (Referência: Dezembro)")
    df_formatado = df.style.format("{:.2f}")
    st.dataframe(df_formatado)
    st.caption("Fonte dos dados: Adaptado de SECOVI - SP")

# Função para exibir o gráfico interativo com valores visíveis
def exibir_grafico_interativo(df):
    df_melted = df.melt(id_vars=["Ano"], var_name="Categoria", value_name="Valor")
    fig = px.line(df_melted, x="Ano", y="Valor", color="Categoria", markers=True,
                  text="Valor", template="simple_white")

    fig.update_traces(textposition="bottom right")
    
    fig.update_layout(
        title="Média do Valor dos Imóveis por Ano e Estado de Conservação",
        xaxis_title="Ano",
        yaxis_title="Valor (R$)",
        legend_title="Categoria de Imóvel",
        showlegend=True
    )
    
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Fonte dos dados: Adaptado de SECOVI - SP")

# Função para previsão de valores para dezembro de 2024
def prever_valores_2024(df):
    st.subheader("Previsão de Valores para Dezembro de 2024")
    df_copy = df.copy()
    df_copy["Ano"] = df_copy["Ano"].astype(int)

    previsoes = {}
    for coluna in df.columns[1:]:
        X = df_copy["Ano"].values.reshape(-1, 1)
        y = df_copy[coluna].values
        modelo = LinearRegression()
        modelo.fit(X, y)
        previsao = modelo.predict(np.array([[2024]]))[0]
        previsoes[coluna] = previsao

    df_previsao = pd.DataFrame(previsoes, index=[2024])
    st.write(df_previsao.style.format("{:.2f}"))

    st.caption("Metodologia: Utilizou-se o modelo de regressão linear simples para prever os valores dos imóveis em dezembro de 2024. O modelo foi treinado com os dados históricos de 2015 a 2023 e aplicado para projetar os valores para 2024.")

# Função para comparar o valor do imóvel com o ano anterior
def comparar_anos(df):
    st.subheader("Comparação do Valor Médio em Relação ao Ano Anterior")
    ano_selecionado = st.selectbox("Selecione o ano para comparação:", df['Ano'])
    coluna_selecionada = st.selectbox("Selecione a categoria de imóvel:", df.columns[1:])
    
    if ano_selecionado > min(df['Ano']):
        ano_anterior = ano_selecionado - 1
        valor_atual = df.loc[df['Ano'] == ano_selecionado, coluna_selecionada].values[0]
        valor_anterior = df.loc[df['Ano'] == ano_anterior, coluna_selecionada].values[0]
        diferenca = valor_atual - valor_anterior
        porcentagem = (diferenca / valor_anterior) * 100
        if diferenca > 0:
            st.write(f"O valor médio do imóvel **aumentou** em {diferenca:.2f} R$ ({porcentagem:.2f}%) em relação ao ano anterior.")
        else:
            st.write(f"O valor médio do imóvel **diminuiu** em {abs(diferenca):.2f} R$ ({abs(porcentagem):.2f}%) em relação ao ano anterior.")
    else:
        st.write("Não há ano anterior para comparação.")
    st.caption("Fonte dos dados: Adaptado de SECOVI - SP")

# Função para calcular o valor do imóvel com base nas métricas, incluindo metragem
def calcular_valor_imovel(df):
    st.subheader("Cálculo do Valor do Imóvel")
    ano = st.selectbox("Selecione o ano de referência:", df['Ano'])
    categoria = st.selectbox("Selecione a categoria de imóvel:", df.columns[1:])
    metragem = st.number_input("Insira a metragem (m²):", min_value=0.0, step=0.1)

    valor_medio = df.loc[df['Ano'] == ano, categoria].values[0]
    valor_imovel = valor_medio * metragem
    st.write(f"O valor estimado do imóvel para {metragem:.2f} m² é: R$ {valor_imovel:.2f}")
    st.caption("Fonte dos dados: Adaptado de SECOVI - SP")

# Função para cálculo considerando retrofit
def calcular_valor_com_retrofit(df):
    st.subheader("Cálculo do Valor do Imóvel com Retrofit")
    ano = st.selectbox("Selecione o ano de referência (retrofit):", df['Ano'])
    categoria = st.selectbox("Selecione a categoria de imóvel (retrofit):", df.columns[1:])
    porcentagem_retrofit = st.slider("Selecione o percentual de aumento devido ao retrofit:", 0, 400, 10)
    metragem = st.number_input("Insira a metragem (m²) para retrofit:", min_value=0.0, step=0.1)

    valor_medio = df.loc[df['Ano'] == ano, categoria].values[0]
    valor_retrofit = valor_medio * metragem * (1 + porcentagem_retrofit / 100)
    st.write(f"O valor do imóvel com retrofit é: R$ {valor_retrofit:.2f}")
    st.caption("Fonte dos dados: Adaptado de SECOVI - SP")

# Função para upload e download de até 9 arquivos PDF
def upload_download_pdf():
    st.subheader("Upload e Download de Arquivos PDF")
    arquivos_pdf = st.file_uploader("Envie até 9 arquivos PDF", type=["pdf"], accept_multiple_files=True)

    if arquivos_pdf:
        if len(arquivos_pdf) > 9:
            st.warning("Você pode carregar no máximo 9 arquivos.")
        else:
            for i, arquivo in enumerate(arquivos_pdf):
                st.write(f"Arquivo {i+1}: {arquivo.name} carregado com sucesso.")
                st.download_button(label=f"Baixar PDF {i+1}", data=arquivo, file_name=arquivo.name)

# Carregar os dados
df = carregar_dados()

# Exibir as seções do dashboard
st.title("Análise do Valor do Metro Quadrado de Locação Residencial no Centro de São Paulo, SP entre 2015 e 2023")
st.caption("Dashboard criado por Aliandra Gonzaga e Souza (2024)")

# Exibição das seções no menu lateral
secoes = ["Tabela de Valores", "Gráfico de Valores", "Previsão para 2024", "Comparação Anual", "Cálculo do Valor do Imóvel", "Cálculo com Retrofit", "Upload e Download de PDF"]
escolha = st.sidebar.radio("Navegue pelas seções:", secoes)

if escolha == "Tabela de Valores":
    exibir_tabela(df)
elif escolha == "Gráfico de Valores":
    exibir_grafico_interativo(df)
elif escolha == "Previsão para 2024":
    prever_valores_2024(df)
elif escolha == "Comparação Anual":
    comparar_anos(df)
elif escolha == "Cálculo do Valor do Imóvel":
    calcular_valor_imovel(df)
elif escolha == "Cálculo com Retrofit":
    calcular_valor_com_retrofit(df)
elif escolha == "Upload e Download de PDF":
    upload_download_pdf()
