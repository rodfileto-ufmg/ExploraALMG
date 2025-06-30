import requests
import pandas as pd
import sqlite3
from io import StringIO

def baixar_arquivo_em_memoria(ano):
    print(f"Baixando arquivos de proposições para o ano de {ano}")
    url = f"https://dadosabertos.almg.gov.br/arquivo/proposicoes/download?ano={ano}&tipo=CSV"
    response = requests.get(url)
    response.raise_for_status()
    print(f"Arquivo de {ano} baixado com sucesso na memória")
    return response.text

def carregar_csv_no_sqlite(ano, conn, tabela_nome='proposicoes'):
    csv_text = baixar_arquivo_em_memoria(ano)
    df = pd.read_csv(StringIO(csv_text))
    # Opcional: adicionar uma coluna com o ano para identificar a origem
    df['ano_arquivo'] = ano
    df.to_sql(tabela_nome, conn, if_exists='append', index=False)
    print(f"Dados do ano {ano} adicionados na tabela '{tabela_nome}'")
