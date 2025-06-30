import requests
import sqlite3

# URL do JSON
url = "https://dadosabertos.almg.gov.br/api/v2/legislaturas/lista?formato=json"

# Baixar o JSON
response = requests.get(url)
data = response.json()

# Conectar ao banco SQLite (cria se não existir)
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Criar tabela legislaturas
cursor.execute('''
CREATE TABLE IF NOT EXISTS legislaturas (
    id INTEGER PRIMARY KEY,
    dataInicio TEXT,
    dataTermino TEXT,
    dataEleicao TEXT
)
''')

# Inserir dados na tabela
for item in data.get('listaLegislatura', []):
    cursor.execute('''
    INSERT OR REPLACE INTO legislaturas (id, dataInicio, dataTermino, dataEleicao)
    VALUES (?, ?, ?, ?)
    ''', (
        item.get('id'),
        item.get('dataInicio'),
        item.get('dataTermino'),
        item.get('dataEleicao')  # Pode ser None se não existir
    ))

# Salvar (commit) e fechar conexão
conn.commit()
conn.close()

print("Dados inseridos com sucesso na tabela legislaturas.")