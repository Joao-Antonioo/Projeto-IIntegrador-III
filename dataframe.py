import streamlit as st
from dataset import df

st.title('Dataset de Vendas')
with st.expander('Colunas'):
    colunas = st.multiselect(
        'Selecione as Colunas',
        list(df.columns), 
        list(df.columns)
        )
st.sidebar.title('Filtros')
with st.sidebar.expander('Categoria do Produto'):
    categorias = st.multiselect(
        'Selecione as categorias',
        df['Categoria do Produto'].unique(),
        df['Categoria do Produto'].unique()
        )


with st.sidebar.expander('Preço do Produto'):
    preco = st.slider(
        'Selecione o Preço',
        0, 5000,
        (0, 5000)
        )


with st.sidebar.expander('Data da compra'):
    data_compra = st.date_input(
        'Selecione a data',
        (df['Data da Compra'].min(),
        df['Data da Compra'].max())    
    )
    
    
query = '''
     `Categoria do Produto` in @categorias and \
     @preco[0] <= Preço <= @preco[1] and \
     @data_compra[0] <= `Data da Compra` <= @data_compra[1]
'''
filtro_dados = df.query(query)
filtro_dados = filtro_dados[colunas]

 
st.dataframe(filtro_dados)