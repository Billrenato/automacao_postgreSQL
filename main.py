import os
import platform
import psycopg2
from ftplib import FTP
import rarfile
from datetime import datetime

# ==== CONFIGURAÇÕES ====


# Dados padrão de conexão ao banco principal (serão completados depois)
PG_PRINCIPAL_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'dbname': '',  # vai ser definido dinamicamente
    'user': 'seu_usuario',
    'password': 'sua_senha'
}

FTP_HOST = 'exemplo.dyndns.org'
FTP_USER = 'userr'
FTP_PASS = '0000'
FTP_DOWNLOAD_FOLDER = r'C:\'

# ==== FUNÇÃO DE LOG ====
def write_log(message):
    with open('log.txt', 'a', encoding='utf-8') as log_file:
        log_file.write(f"[{datetime.now()}] {message}\n")

# ==== DETECTAR SISTEMA OPERACIONAL ====
def detectar_so():
    so = platform.system()
    write_log(f"Sistema Operacional detectado: {so}")
    return so

# ==== LOCALIZAR BANCO PRINCIPAL ====
def obter_dados_conexao():
    write_log("Conectando ao banco de CONEXAO (PostgreSQL)...")
    con = psycopg2.connect(**PG_CONEXAO_CONFIG)
    cur = con.cursor()
    cur.execute("SELECT caminho, bd FROM conexao LIMIT 1")
    result = cur.fetchone()
    con.close()

    if not result:
        raise Exception("Nenhum registro encontrado na tabela conexao.")

    caminho, bd = result
    caminho = caminho.strip()

    # Banco principal: nome do banco que será usado
    PG_PRINCIPAL_CONFIG['dbname'] = bd.strip()

    write_log(f"Banco principal localizado: {bd.strip()}")
    return PG_PRINCIPAL_CONFIG

# ==== EXECUTAR ALTERAÇÕES NO BANCO PRINCIPAL ====
def executar_sql_script(conn, script_path):
    write_log(f"Executando script: {script_path}")
    try:
        with open(script_path, 'r', encoding='utf-8') as file:
            sql_script = file.read()

        cursor = conn.cursor()
        try:
            cursor.execute(sql_script)
            conn.commit()
            write_log(f"Script executado com sucesso: {script_path}")
        except Exception as e:
            conn.rollback()
            write_log(f"Erro ao executar {script_path}: {str(e)}")
        finally:
            cursor.close()
    except Exception as e:
        write_log(f"Erro ao ler o arquivo {script_path}: {str(e)}")

def aplicar_alteracoes(pg_config):
    try:
        conn = psycopg2.connect(**pg_config)
        scripts = ['alteracoes/ddl.sql', 'alteracoes/procedures.sql', 'alteracoes/triggers.sql']

        for script in scripts:
            if os.path.exists(script):
                executar_sql_script(conn, script)
            else:
                write_log(f"Script não encontrado: {script}")

        conn.close()
    except Exception as e:
        write_log(f"Erro ao aplicar alterações: {str(e)}")

# ==== DOWNLOAD VIA FTP (APENAS WINDOWS) ====
def baixar_arquivos_ftp():
    try:
        write_log("Iniciando download FTP...")
        ftp = FTP(FTP_HOST)
        ftp.encoding = 'latin-1'
        ftp.login(FTP_USER, FTP_PASS)

        os.makedirs(FTP_DOWNLOAD_FOLDER, exist_ok=True)

        arquivo_remoto = '/exemplo/sistema.12beta5.rar'
        local_path = os.path.join(FTP_DOWNLOAD_FOLDER, 'sistema.12beta5.rar')

        with open(local_path, 'wb') as f:
            ftp.retrbinary(f'RETR {arquivo_remoto}', f.write)
            write_log(f"Arquivo baixado com sucesso: {arquivo_remoto}")

        ftp.quit()
        write_log("Download FTP concluído.")

        # Extraindo apenas a pasta "Piaracaiasoft"
        write_log("Iniciando extração da pasta 'Piaracaiasoft'...")

        rar = rarfile.RarFile(local_path)
        for item in rar.infolist():
            if item.filename.startswith('piaracaiasoft/') or item.filename.startswith('piaracaiasoft\\'):
                rar.extract(item, path=FTP_DOWNLOAD_FOLDER)
                write_log(f"Extraído: {item.filename}")

        write_log("Extração concluída.")
    except Exception as e:
        write_log(f"Erro: {str(e)}")

# ==== EXECUÇÃO PRINCIPAL ====
def main():
    write_log("=== Início da execução ===")
    try:
        so = detectar_so()
        pg_config = obter_dados_conexao()
        aplicar_alteracoes(pg_config)

        if so == 'Windows':
            baixar_arquivos_ftp()
        else:
            write_log("Download via FTP ignorado (SO não-Windows)")

        write_log("=== Processo finalizado com sucesso ===")
    except Exception as e:
        write_log(f"Erro geral: {str(e)}")

if __name__ == '__main__':
    main()
