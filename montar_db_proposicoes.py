import requests
import sqlite3
import csv
from io import StringIO

def baixar_arquivo_em_memoria(ano):
    print(f"Baixando arquivos de proposições para o ano de {ano}")
    url = f"https://dadosabertos.almg.gov.br/arquivo/proposicoes/download?ano={ano}&tipo=CSV"
    response = requests.get(url)
    response.raise_for_status()
    print(f"Arquivo de {ano} baixado com sucesso na memória")
    return response.text

def criar_tabela_proposicoes(conn):
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS proposicoes (
            Codigo TEXT PRIMARY KEY,
            TipoProposicao TEXT,
            SiglaTipoProposicao TEXT,
            Numero TEXT,
            Ano TEXT,
            Ementa TEXT,
            Indexacao TEXT,
            Situacao TEXT,
            DataPublicacao TEXT,
            DataAtualizacao TEXT,
            DataUltimaAcao TEXT,
            Regime TEXT,
            Resumo TEXT,
            Origem TEXT,
            Local TEXT,
            NomeFaseAtual TEXT,
            Legislatura TEXT,
            Autores TEXT,
            LinkTextos TEXT,
            ano_arquivo INTEGER
        )
    ''')
    conn.commit()

def carregar_csv_no_sqlite(ano, conn):
    csv_text = baixar_arquivo_em_memoria(ano)
    csv_file = StringIO(csv_text)
    reader = csv.DictReader(csv_file, delimiter=',')

    cursor = conn.cursor()

    for row in reader:
        # Adiciona o ano na linha
        row['ano_arquivo'] = ano

        # Cria uma tupla com os valores na ordem correta
        values = (
            row.get('Codigo'),
            row.get('TipoProposicao'),
            row.get('SiglaTipoProposicao'),
            row.get('Numero'),
            row.get('Ano'),
            row.get('Ementa'),
            row.get('Indexacao'),
            row.get('Situacao'),
            row.get('DataPublicacao'),
            row.get('DataAtualizacao'),
            row.get('DataUltimaAcao'),
            row.get('Regime'),
            row.get('Resumo'),
            row.get('Origem'),
            row.get('Local'),
            row.get('NomeFaseAtual'),
            row.get('Legislatura'),
            row.get('Autores'),
            row.get('LinkTextos'),
            row.get('ano_arquivo')
        )

        # Executa o insert ou replace
        cursor.execute('''
            INSERT OR REPLACE INTO proposicoes (
                Codigo, TipoProposicao, SiglaTipoProposicao, Numero, Ano,
                Ementa, Indexacao, Situacao, DataPublicacao, DataAtualizacao,
                DataUltimaAcao, Regime, Resumo, Origem, Local, NomeFaseAtual,
                Legislatura, Autores, LinkTextos, ano_arquivo
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', values)

    conn.commit()
    print(f"Dados do ano {ano} adicionados/atualizados na tabela 'proposicoes'")

# Conectar ao banco SQLite
conn = sqlite3.connect('database.db')

# Criar tabela (se não existir)
criar_tabela_proposicoes(conn)

# Carregar dados de anos específicos
anos = range(1959, 1980)
for ano in anos:
    carregar_csv_no_sqlite(ano, conn)

# Fechar conexão
conn.close()
