##🔧 Atualizador de Banco de Dados e Arquivos via FTP

Este script automatiza a atualização de bancos de dados PostgreSQL e o download de arquivos via FTP (com extração automática de arquivos `.rar`) em sistemas Windows.

## 📌 Funcionalidades

- Conecta-se a um banco de dados central para obter o nome do banco principal.
- Executa scripts SQL (`DDL`, `procedures`, `triggers`) automaticamente no banco principal.
- Em sistemas Windows, realiza download de um arquivo `.rar` via FTP e extrai apenas a pasta desejada.
- Gera logs detalhados da execução em `log.txt`.

## 🛠️ Pré-requisitos

- Python 3.8+
- PostgreSQL
- Dependências Python:


pip install psycopg2 rarfile
⚠️ O rarfile requer que o unrar esteja instalado no sistema. Em Windows, baixe de: https://www.rarlab.com/rar_add.htm

🧬 Estrutura do Projeto


    atualizador/
    ├── alteracoes/
    │   ├── ddl.sql
    │   ├── procedures.sql
    │   └── triggers.sql
    ├── log.txt
    ├── script.py
    ⚙️ Configuração
    
Edite os dicionários PG_CONEXAO_CONFIG e PG_PRINCIPAL_CONFIG no início do arquivo para configurar os dados de acesso ao PostgreSQL:


    PG_CONEXAO_CONFIG = {
        'host': 'localhost',
        'port': 5432,
        'dbname': 'conexao_db',
        'user': 'seu_usuario',
        'password': 'sua_senha'
    }
    Configure também os dados FTP:
    
    
    FTP_HOST = 'exemplo.dyndns.org'
    FTP_USER = 'user'
    FTP_PASS = '0000'
    FTP_DOWNLOAD_FOLDER = r'C:\'




## 🚀 Execução
No terminal:


python script.py
O script irá:

Detectar o sistema operacional.

Conectar-se ao banco de "conexão".

Aplicar os scripts SQL no banco principal.

Se for Windows, baixar e extrair o arquivo .rar via FTP.

## 📝 Logs
Todos os eventos são registrados em tempo real no arquivo log.txt, incluindo erros de conexão, execução de scripts e status do FTP.

##❗ Observações
O caminho do arquivo .rar no FTP está fixo como /vndTeste/VND5.48-beta5.rar.

Apenas a pasta piaracaiasoft dentro do .rar será extraída.

Este projeto foi criado com foco em ambientes Windows; o recurso de download FTP é ignorado em outros sistemas operacionais.

## 🧑‍💻 Autor
Renato Junior Mathias
LinkedIn | renatojrmathias94@gmail.com
