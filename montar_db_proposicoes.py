import sys
import os
import sqlite3

from funcoes.DataImporter import carregar_csv_no_sqlite

conn = sqlite3.connect('database.db')

# Load CSVs into SQLite
anos = range(1959, 1980)
for ano in anos:
    carregar_csv_no_sqlite(ano, conn)

conn.close()