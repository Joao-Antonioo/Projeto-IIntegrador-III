import plotly.express as px
import plotly.graph_objs as go
from utils import (
    df, 
    df_rec_estado, 
    df_rec_mensal, 
    df_rec_categoria, 
    df_vendedores
)


grafico_map_estado = px.scatter_geo(
    df_rec_estado,
    lat = 'lat',
    lon = 'lon',
    scope = 'south america',
    size = 'Preço',
    template = 'seaborn',
    hover_name = 'Local da compra',
    hover_data = {'lat': False, 'lon': False},
    title = 'Receita por Estado'
)

grafico_rec_mensal = px.line(
    df_rec_mensal,
    x = 'Mês',
    y = 'Preço',
    markers = True,
    range_y = (0, df_rec_mensal.max()),
    color = 'Ano',
    line_dash = 'Ano',
    title = 'Receita Mensal'   
)
grafico_rec_mensal.update_layout(yaxis_title = 'Receita')

grafico_rec_estado = px.bar(
    df_rec_estado.head(7),
    x = 'Local da compra',
    y = 'Preço',
    text_auto = True, 
    title = 'Top Receita por Estados'
)

grafico_rec_categoria = px.bar(
    df_rec_categoria.head(7),
    text_auto = True,
    title = 'Top 7 Categorias com Maior Receita'
)

grafico_rec_vendedores = px.bar(
    df_vendedores[['sum']].sort_values('sum', ascending=False).head(7),
    x = 'sum',
    y = df_vendedores[['sum']].sort_values('sum', ascending=False).head(7).index,
    text_auto = True,
    title = 'Top 7 Vendedores por Receita'
) 

grafico_vendas_vendedores = px.bar(
    df_vendedores[['count']].sort_values('count', ascending=False).head(7),
    x = 'count',
    y = df_vendedores[['count']].sort_values('count', ascending=False).head(7).index,
    text_auto = True,
    title = 'Top 7 Vendedores por Venda'
)



def gerar_grafico_distribuicao_categorias(dataframe):
    """
    Gera gráfico de pizza para distribuição de vendas por categoria
    """
    categoria_vendas = dataframe['Categoria do Produto'].value_counts()
    
    return px.pie(
        values=categoria_vendas.values, 
        names=categoria_vendas.index, 
        title='Participação de Vendas por Categoria'
    )

def gerar_grafico_tipos_pagamento(dataframe):
    """
    Gera gráfico de barras para tipos de pagamento
    """
    tipos_pagamento = dataframe['Tipo de pagamento'].value_counts()
    
    return px.bar(
        x=tipos_pagamento.index, 
        y=tipos_pagamento.values, 
        title='Distribuição de Tipos de Pagamento'
    )

def gerar_grafico_ticket_medio_por_vendedor(dataframe):
    """
    Gera gráfico de barras com ticket médio por vendedor
    """
    ticket_medio = dataframe.groupby('Vendedor')['Preço'].mean().sort_values(ascending=False)
    
    return px.bar(
        x=ticket_medio.index,
        y=ticket_medio.values,
        title='Ticket Médio por Vendedor',
        labels={'x': 'Vendedor', 'y': 'Ticket Médio'}
    )