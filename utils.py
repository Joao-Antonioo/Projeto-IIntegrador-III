import pandas as pd
import numpy as np
import scipy.stats as stats

from dataset import df

def format_number(value, prefix = ''):
    """Formata números para apresentação legível"""
    for unit in ['', 'mil', ]:
        if value < 1000:
            return f'{prefix} {value:.2f}{unit}'
        value /= 1000
    return f'{prefix} {value:.2f} milhões'

def analise_estatistica_descritiva(dataframe):
    """
    Realiza uma análise estatística descritiva completa do DataFrame
    
    Parâmetros:
    - dataframe: DataFrame pandas para análise
    
    Retorna:
    - Estatísticas descritivas
    - Resultados de testes de normalidade
    """
    
    colunas_numericas = dataframe.select_dtypes(include=[np.number]).columns
    
    
    desc_stats = dataframe[colunas_numericas].describe()
    
    
    normalidade = {}
    for coluna in colunas_numericas:
        
        _, p_valor = stats.normaltest(dataframe[coluna])
        normalidade[coluna] = {
            'estatistica': p_valor,
            'distribuicao': 'Normal' if p_valor > 0.05 else 'Não Normal'
        }
    
    return desc_stats, normalidade

def analise_correlacao(dataframe):
    """
    Gera uma matriz de correlação para colunas numéricas
    
    Parâmetros:
    - dataframe: DataFrame pandas para análise
    
    Retorna:
    - Matriz de correlação entre colunas numéricas
    """
    
    colunas_numericas = dataframe.select_dtypes(include=[np.number])
    
    
    matriz_correlacao = colunas_numericas.corr()
    
    return matriz_correlacao

# Dataframes para análises específicas 
df_rec_estado = df.groupby('Local da compra')[['Preço']].sum()
df_rec_estado = df.drop_duplicates(subset='Local da compra')[['Local da compra', 'lat', 'lon']].merge(df_rec_estado, left_on='Local da compra', right_index=True).sort_values('Preço', ascending=False)

df_rec_mensal = df.set_index('Data da Compra').groupby(pd.Grouper(freq='M'))['Preço'].sum().reset_index()
df_rec_mensal['Ano'] = df_rec_mensal['Data da Compra'].dt.year
df_rec_mensal['Mês'] = df_rec_mensal['Data da Compra'].dt.month_name()

df_rec_categoria = df.groupby('Categoria do Produto')[['Preço']].sum().sort_values('Preço', ascending=False)

df_vendedores = pd.DataFrame(df.groupby('Vendedor')['Preço'].agg(['sum', 'count']))