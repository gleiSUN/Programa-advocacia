import sqlite3

#função para abrir conexão com o banco de dados.
def conectar():
    conexao = sqlite3.connect('bd_advocacia.db')
    return conexao

conexao = conectar()
conexao.close()
