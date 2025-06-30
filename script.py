import sqlite3
from funcoes.DataImporter import carregar_csv_no_sqlite

# Exemplo de uso:
conn = sqlite3.connect('proposicoes.db')
anos = range(1980,2026)
for ano in anos:
    carregar_csv_no_sqlite(ano, conn)
conn.close()


# import pandas as pd
# import wget
# import numpy as np
# import plotly.express as px
# import json

# # Função para download dos arquivos


# def baixar_arquivo(ano):
#     print(f"Baixando arquivos de proposições para o ano de {ano}")
#     url = f"https://dadosabertos.almg.gov.br/arquivo/proposicoes/download?ano={ano}&tipo=CSV"
#     arquivo = wget.download(url, f'{ano}.csv')
#     print(f"Arquivo de {ano} baixado com sucesso")
#     return(arquivo)

# def ler_arquivos_csv(ano):
#     arquivo_csv = pd.read_csv(f"{ano}.csv")
#     return(arquivo_csv)

# def contar_proposicao_tipo():
#     pass

# if __name__ == "__main__":
#     proposicao = []
#     for ano in range(2022,2026):
#         arquivo = baixar_arquivo(ano)
#         arquivo_csv = ler_arquivos_csv(ano)
#         proposicao.append(arquivo_csv)
    
#     tabela_proposicao = pd.concat(proposicao)
#     tabela_proposicao['TipoProposicao'] = tabela_proposicao.TipoProposicao.str.title().str.strip()

#     tabela_proposicao_autores = tabela_proposicao[~tabela_proposicao.Autores.isna()]

#     # Função para fazer o parse do JSON
#     def parse_autores(autores_json):
#         return json.loads(autores_json)

#     # Parse do JSON na coluna Autores
#     tabela_proposicao_autores['autores_parsed'] = tabela_proposicao_autores['Autores'].apply(parse_autores)

#     # Explode para uma linha por autor
#     df_exploded = tabela_proposicao_autores.explode('autores_parsed')

#     # Normalizar o JSON para colunas separadas
#     autores_df = pd.json_normalize(df_exploded['autores_parsed'])

#     # Combinar com os dados originais (removendo colunas desnecessárias)
#     tabela_autores_individual = pd.concat([
#         df_exploded.drop(['Autores', 'autores_parsed'], axis=1).reset_index(drop=True),
#         autores_df
#     ], axis=1)

#     print(f"Linhas originais: {len(tabela_proposicao_autores)}")
#     print(f"Linhas após explosão: {len(tabela_autores_individual)}")

    

#     proposicao_tipo = pd.DataFrame({
#         'count': tabela_proposicao.TipoProposicao.value_counts(),
#         'prop': tabela_proposicao.TipoProposicao.value_counts(normalize=True)
#     })

#     new_index = np.where(proposicao_tipo['prop'] < 0.01, 'Outras', proposicao_tipo.index)

#     proposicao_tipo.index = new_index

#     proposicao_tipo = proposicao_tipo.groupby(proposicao_tipo.index).sum()

#     proposicao_tipo = proposicao_tipo.sort_values('count', ascending=True)

#         # Create bar chart
#     # Create horizontal bar chart
#     fig = px.bar(
#         x=proposicao_tipo['count'],
#         y=proposicao_tipo.index, 
#         orientation='h',
#         title='Distribuição por Tipo de Proposição',
#         labels={'x': '', 'y': ''},
#         text=proposicao_tipo['count']
#     )

#     # Add percentage labels
#     fig.update_traces(
#         texttemplate='%{text} (%{customdata:.1%})', 
#         textposition='inside',
#         customdata=proposicao_tipo['prop']
#     )

#     # Update layout - extend x-axis range to give space for labels
#     fig.update_layout(
#         plot_bgcolor='white',
#         paper_bgcolor='white',
#         xaxis=dict(showgrid=False, zeroline=False),
#         yaxis=dict(showgrid=False, zeroline=False),
#         height=400
#     )

#     fig.show()