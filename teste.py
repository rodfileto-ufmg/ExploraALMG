import pandas as pd
import plotly.graph_objects as go
import numpy as np
from funcoes.Figuras import create_time_series_chart_go, create_horizontal_bar_chart_go


def ler_arquivos_csv(ano):
    arquivo_csv = pd.read_csv(f"{ano}.csv")
    return(arquivo_csv)

proposicao = []

for ano in range(1980,2024):
    arquivo_csv = ler_arquivos_csv(ano)
    proposicao.append(arquivo_csv)
    
tabela_proposicao = pd.concat(proposicao)

def preprocess_proposicao_simple(df, date_col='DataPublicacao', window=5):
    df_work = df.copy()
    df_work[date_col] = pd.to_datetime(df_work[date_col], format='%d/%m/%Y')
    daily_counts = df_work.groupby(df_work[date_col].dt.date).size().reset_index()
    daily_counts.columns = ['date', 'total_propositions']
    daily_counts['date'] = pd.to_datetime(daily_counts['date'])
    daily_counts = daily_counts.sort_values('date')
    daily_counts['moving_avg_5d'] = daily_counts['total_propositions'].rolling(window=window, min_periods=1).mean()
    return daily_counts

# Process and visualize

# Step 1: Process your data
processed_data = preprocess_proposicao_simple(tabela_proposicao)

# Step 2: Create chart using the new function
fig = create_time_series_chart_go(
    data=processed_data,
    date_col='date',
    value_col='total_propositions',
    ma_col='moving_avg_5d',
    title='Proposições Diárias com Média Móvel de 5 Dias',
    height=500
)

# Step 3: Display
fig.show()

proposicao_tipo = pd.DataFrame({
        'count': tabela_proposicao.TipoProposicao.value_counts(),
        'prop': tabela_proposicao.TipoProposicao.value_counts(normalize=True)
    })

new_index = np.where(proposicao_tipo['prop'] < 0.01, 'Outras', proposicao_tipo.index)

proposicao_tipo.index = new_index

proposicao_tipo = proposicao_tipo.groupby(proposicao_tipo.index).sum()

proposicao_tipo = proposicao_tipo.sort_values('count', ascending=True)

# Resetar o índice para criar uma coluna com os tipos de proposição
proposicao_tipo_reset = proposicao_tipo.reset_index()
proposicao_tipo_reset.columns = ['tipo', 'count', 'prop']  # Renomear as colunas

fig = create_horizontal_bar_chart_go(
    proposicao_tipo_reset,
    'count',
    'tipo', 
    title="Horizontal Bar Chart",
    show_percentages=True,
    height=400,
    text_position='inside',
    bar_color='lightblue'
)
fig.show()

