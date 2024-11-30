import pyodbc

server = '192.168.0.11'
database = 'JCIHistorianDB'
username = 'py'
password = 'py'

# Corrija o nome do driver para o correto
connection_string = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password

def testar_conexao():
    try:
        conn = pyodbc.connect(connection_string)
        print("Conexão bem-sucedida!")
        conn.close()
        return "Conexão bem-sucedida!"
    except Exception as e:
        print(f"Erro de conexão: {e}")
        return f"Erro de conexão: {e}"
