import streamlit as st
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd
import numpy as np
from dataset import df
from utils import format_number
from graficos import (
    grafico_map_estado, 
    grafico_rec_mensal, 
    grafico_rec_estado, 
    grafico_rec_categoria, 
    grafico_rec_vendedores, 
    grafico_vendas_vendedores
)

st.set_page_config(
    page_title="Dashboard de Vendas Avançado",
    page_icon=":shopping_cart:",
    layout='wide',
    initial_sidebar_state='expanded'
)

def main():
    st.markdown("""
    # 📊 Dashboard Avançado de Análise de Vendas
    ## Insights Estratégicos e Visualizações Detalhadas
    """)
    
    st.sidebar.header('🔍 Painel de Filtros Avançados')
    
    # Filtros expandidos
    filtro_vendedor = st.sidebar.multiselect(
        'Selecione Vendedores',
        df['Vendedor'].unique(),
        default=None
    )
    
    filtro_categoria = st.sidebar.multiselect(
        'Selecione Categorias',
        df['Categoria do Produto'].unique(),
        default=None
    )
    
    filtro_produto = st.sidebar.multiselect(
        'Selecione Produtos',
        df['Produto'].unique(),
        default=None
    )
    
    filtro_pagamento = st.sidebar.multiselect(
        'Tipo de Pagamento',
        df['Tipo de pagamento'].unique(),
        default=None
    )
    
    preco_min, preco_max = st.sidebar.slider(
        'Faixa de Preço', 
        float(df['Preço'].min()), 
        float(df['Preço'].max()), 
        (float(df['Preço'].min()), float(df['Preço'].max()))
    )
    
    data_min = df['Data da Compra'].min()
    data_max = df['Data da Compra'].max()
    filtro_data = st.sidebar.date_input(
        'Período de Vendas', 
        value=(data_min, data_max),
        min_value=data_min,
        max_value=data_max
    )
    
    # Aplicação dos filtros
    df_filtrado = df.copy()
    
    if filtro_vendedor:
        df_filtrado = df_filtrado[df_filtrado['Vendedor'].isin(filtro_vendedor)]
    if filtro_categoria:
        df_filtrado = df_filtrado[df_filtrado['Categoria do Produto'].isin(filtro_categoria)]
    if filtro_produto:
        df_filtrado = df_filtrado[df_filtrado['Produto'].isin(filtro_produto)]
    if filtro_pagamento:
        df_filtrado = df_filtrado[df_filtrado['Tipo de pagamento'].isin(filtro_pagamento)]
    
    df_filtrado = df_filtrado[
        (df_filtrado['Preço'] >= preco_min) & 
        (df_filtrado['Preço'] <= preco_max)
    ]
    
    tab1, tab2, tab3 = st.tabs([
        'Visão Geral', 
        'Análise Detalhada',
        'Insights Avançados'
    ])
    
    with tab1:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric('Receita Total', format_number(df_filtrado['Preço'].sum(), 'R$'))
        with col2:
            st.metric('Quantidade de Vendas', format_number(df_filtrado.shape[0]))
        with col3:
            st.metric('Ticket Médio', format_number(df_filtrado['Preço'].mean(), 'R$'))
        with col4:
            st.metric('Frete Médio', format_number(df_filtrado['Frete'].mean(), 'R$'))
        
        col4, col5 = st.columns(2)
        with col4:
            st.plotly_chart(grafico_map_estado, use_container_width=True)
        with col5:
            st.plotly_chart(grafico_rec_estado, use_container_width=True)
    
    with tab2:
        col1, col2 = st.columns(2)
        
        with col1:
            st.plotly_chart(grafico_rec_mensal, use_container_width=True)
            st.plotly_chart(grafico_rec_categoria, use_container_width=True)
        
        with col2:
            st.plotly_chart(grafico_rec_vendedores)
            st.plotly_chart(grafico_vendas_vendedores)
    
    with tab3:
        st.header('Análise Detalhada por Vendedor')
        
        if filtro_vendedor:
            for vendedor in filtro_vendedor:
                dados_vendedor = df_filtrado[df_filtrado['Vendedor'] == vendedor]
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric(f'Receita Total - {vendedor}', 
                             format_number(dados_vendedor['Preço'].sum(), 'R$'))
                with col2:
                    st.metric(f'Vendas - {vendedor}', 
                             format_number(len(dados_vendedor)))
                with col3:
                    st.metric(f'Ticket Médio - {vendedor}', 
                             format_number(dados_vendedor['Preço'].mean(), 'R$'))
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # Vendas por categoria
                    fig_cat = px.pie(
                        dados_vendedor,
                        names='Categoria do Produto',
                        values='Preço',
                        title=f'Vendas por Categoria - {vendedor}'
                    )
                    st.plotly_chart(fig_cat, use_container_width=True)
                
                with col2:
                    # Vendas por tipo de pagamento
                    fig_pag = px.bar(
                        dados_vendedor.groupby('Tipo de pagamento')['Preço'].sum().reset_index(),
                        x='Tipo de pagamento',
                        y='Preço',
                        title=f'Vendas por Tipo de Pagamento - {vendedor}'
                    )
                    st.plotly_chart(fig_pag, use_container_width=True)
                
                # Evolução temporal das vendas
                fig_temp = px.line(
                    dados_vendedor.groupby('Data da Compra')['Preço'].sum().reset_index(),
                    x='Data da Compra',
                    y='Preço',
                    title=f'Evolução das Vendas - {vendedor}'
                )
                st.plotly_chart(fig_temp, use_container_width=True)
                
                st.divider()
        
        # Análise geral
        st.header('Análise Geral das Vendas')
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Top produtos mais vendidos
            top_produtos = df_filtrado.groupby('Produto')['Preço'].agg(['count', 'sum']).sort_values('count', ascending=False).head(10)
            fig_produtos = px.bar(
                top_produtos,
                y=top_produtos.index,
                x='count',
                title='Top 10 Produtos Mais Vendidos',
                labels={'count': 'Quantidade de Vendas'}
            )
            st.plotly_chart(fig_produtos, use_container_width=True)
        
        with col2:
            # Distribuição de avaliações
            fig_aval = px.histogram(
                df_filtrado,
                x='Avaliação da compra',
                title='Distribuição das Avaliações',
                nbins=5
            )
            st.plotly_chart(fig_aval, use_container_width=True)
        
        # Mapa de calor de vendas por estado e categoria
        vendas_estado_categoria = pd.pivot_table(
            df_filtrado,
            values='Preço',
            index='Local da compra',
            columns='Categoria do Produto',
            aggfunc='sum',
            fill_value=0
        )
        
        fig_heatmap = px.imshow(
            vendas_estado_categoria,
            title='Mapa de Calor: Vendas por Estado e Categoria',
            labels=dict(x='Categoria', y='Estado', color='Valor das Vendas')
        )
        st.plotly_chart(fig_heatmap, use_container_width=True)

if __name__ == '__main__':
    main()