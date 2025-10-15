# Sistema de Relatórios Inteligentes com IA (Django + Text-to-SQL)

Este projeto é uma aplicação web robusta, construída com o framework **Django** e **Python**, que revoluciona a maneira como os usuários interagem com dados. Em vez de escrever consultas SQL complexas, o usuário simplesmente faz uma pergunta em **linguagem natural**, e o sistema utiliza Inteligência Artificial (IA) para gerar, executar e apresentar o relatório desejado.

## Visão Geral do Projeto

O objetivo principal é democratizar o acesso aos dados corporativos, permitindo que usuários de diferentes níveis técnicos gerem relatórios customizados. A aplicação opera em um ciclo simples:

1.  **Entrada:** O usuário insere uma pergunta (ex: "Quais são os 10 produtos mais vendidos no último trimestre?").
2.  **Tradução (IA):** Um modelo de linguagem (GPT-4 ou similar) interpreta a pergunta e a converte em uma *query* SQL válida.
3.  **Execução:** A *query* SQL é executada no banco de dados.
4.  **Saída:** Os resultados são processados com **Pandas** e exibidos em formatos visuais e tabulares (HTML e gráficos).

## Funcionalidades Detalhadas

### Entrada e Processamento
* **Interface Amigável:** Formulário web (Django Templates + Bootstrap) para entrada de texto em linguagem natural.
* **Geração de SQL via IA (Text-to-SQL):** Utilização da OpenAI API (GPT-4 / GPT-3.5) ou modelos *Text-to-SQL* baseados em **Hugging Face Transformers** para tradução automática da pergunta.
* **Validação de Segurança:** Mecanismo de validação de *queries* geradas para prevenir injeções de SQL e a execução de comandos destrutivos (`DROP`, `DELETE`, `UPDATE`).

### Resultados e Saída
* **Processamento de Dados:** Uso da biblioteca **Pandas** para manipulação, limpeza e preparação dos dados retornados pela consulta SQL.
* **Visualização de Dados:** Exibição dos resultados em uma **tabela HTML** dinâmica e em **gráficos** interativos (utilizando Matplotlib ou Plotly).
* **Exportação de Relatórios:** Funcionalidade para exportar os resultados em formatos comuns como PDF e Excel.

### Infraestrutura
* **Autenticação:** Sistema completo de login e gerenciamento de usuários fornecido pelo Django.
* **Configuração Modular:** Suporte a diferentes bases de dados (SQLite para desenvolvimento e PostgreSQL para produção).

## Tecnologias Utilizadas

| Categoria | Tecnologia | Uso Específico |
| :--- | :--- | :--- |
| **Backend Principal** | Python 3.12 | Linguagem principal de desenvolvimento. |
| **Framework Web** | Django 4.x | Estrutura para a aplicação web, URLs, Views e Templates. |
| **Processamento de Dados** | Pandas | Análise, manipulação e estruturação dos dados de consulta. |
| **Visualização** | Matplotlib / Plotly | Geração dos gráficos e visualizações estatísticas. |
| **IA/NLP** | OpenAI API (GPT-4) ou Hugging Face | Tradução de linguagem natural para SQL (*Text-to-SQL*). |
| **Banco de Dados** | SQLite / PostgreSQL | Armazenamento dos dados que serão consultados. |
| **Frontend/UI** | Django Templates, Bootstrap, HTML, JavaScript | Interface do usuário e responsividade do layout. |

## Estrutura do Projeto (Exemplo)

O projeto segue a estrutura padrão de um aplicativo Django, com um módulo central de inteligência:

relatorios-ia-django/
├── manage.py
├── core/                        # Configurações e URLs principais
├── reports/                     # App Django para lógica de relatórios
│   ├── models.py
│   ├── views.py                 # Lógica de processamento da pergunta
│   └── templates/
│       └── reports/
│           └── form_pergunta.html
├── nl_to_sql_engine/            # Módulo de inteligência Text-to-SQL
│   ├── query_generator.py       # (Onde o GPT-4 gera o SQL)
│   └── validation.py            # Verificação de segurança da query
├── db_connector.py              # Gerenciamento da conexão com o banco de dados
└── requirements.txt

## Pré-requisitos

Para rodar o projeto, você precisará ter instalado:

1.  **Python 3.12+**
2.  **PostgreSQL** (ou outro SGBD configurado)
3.  Uma **chave de API da OpenAI** (para a funcionalidade Text-to-SQL baseada em GPT).

## Instalação e Configuração

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/seuusuario/relatorios-ia-django.git](https://github.com/seuusuario/relatorios-ia-django.git)
    cd relatorios-ia-django
    ```

2.  **Crie e ative um ambiente virtual:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # Linux/Mac
    # venv\Scripts\activate   # Windows
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure as variáveis de ambiente:**
    Crie um arquivo `.env` na raiz do projeto e adicione sua chave de API:
    ```
    # Variáveis de ambiente
    OPENAI_API_KEY="SUA_CHAVE_AQUI"
    DATABASE_URL="postgresql://user:password@host:port/dbname" 
    ```

5.  **Execute as migrações do banco de dados:**
    ```bash
    python manage.py migrate
    ```

6.  **Inicie o servidor de desenvolvimento:**
    ```bash
    python manage.py runserver
    ```

O sistema estará acessível em `http://127.0.0.1:8000/`.

## Considerações de Segurança

O componente mais crítico deste projeto é a geração de código SQL por IA. Para garantir a segurança:

* **Validação de Query:** O sistema deve sempre passar a *query* SQL gerada por um filtro de segurança (`validar_query`), que impede comandos destrutivos como `DROP TABLE`, `DELETE FROM`, ou `UPDATE` que modifiquem o esquema ou os dados.
* **Permissões de Banco de Dados:** O usuário do banco de dados configurado no Django (`db_connector.py`) deve ter permissões mínimas (`SELECT` apenas) para a execução de consultas, limitando o potencial dano de uma *query* mal-intencionada ou gerada incorretamente.
* **Chave de API:** A `OPENAI_API_KEY` deve ser armazenada como uma variável de ambiente e nunca ser exposta publicamente.
