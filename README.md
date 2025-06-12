# RHarmony - Sistema de Gestão de RH e Frota

##  sobre o projeto

RHarmony é um sistema web desenvolvido para otimizar os processos operacionais e administrativos de empresas de transporte e delivery. A plataforma integra a gestão de pessoal (Recursos Humanos) com o controle de frotas, focando no monitoramento de documentação de veículos para garantir a regularidade e eficiência da operação.

Este projeto foi desenvolvido como parte do Curso de Tecnologia em Análise e Desenvolvimento de Sistemas da Fatec Garça.

## 🚀 Funcionalidades Principais

* **Autenticação de Usuários:** Sistema seguro de login, cadastro e gerenciamento de sessão.
* **Perfil de Usuário:** Cada gestor pode visualizar e editar suas próprias informações (nome, e-mail) e foto de perfil, além de poder excluir sua própria conta.
* **Dashboard Inteligente:** Painel de controle que exibe métricas importantes, como alertas de documentos de veículos que estão próximos do vencimento ou já venceram.
* **Gestão de Frota:**
    * Cadastro, edição e exclusão de veículos da frota.
    * Interface para listar todos os veículos de forma clara.
* **Gestão de Documentos por Veículo:**
    * Sistema flexível para adicionar múltiplos tipos de documentos a cada veículo (CRLV, Seguro, ANTT, etc.).
    * Cadastro da data de vencimento para cada documento.
    * Exclusão de documentos individuais.
* **Design Responsivo:** Interface "floral e fofo" que se adapta a desktops, tablets e celulares.

## 🛠️ Tecnologias Utilizadas

* **Backend:**
    * **Python 3**
    * **Flask:** Micro-framework web para a estrutura da aplicação.
    * **SQLAlchemy:** ORM para mapeamento e interação com o banco de dados.
    * **Flask-Login:** Para gerenciamento de sessão e autenticação de usuários.
    * **Flask-WTF:** Para criação e validação de formulários.
* **Frontend:**
    * **HTML5**
    * **CSS3** com Variáveis e Flexbox.
    * **Bootstrap 5:** Framework para construção de uma interface responsiva.
    * **Jinja2:** Motor de templates do Flask.
* **Banco de Dados:**
    * **MySQL**

## ⚙️ Instalação e Execução

Siga os passos abaixo para executar o projeto localmente.

### Pré-requisitos

* Python 3.8 ou superior
* MySQL Server instalado e em execução

### 1. Preparação do Ambiente

Clone ou faça o download deste repositório para sua máquina local.

Crie e ative um ambiente virtual na pasta raiz do projeto:

```bash
# Criar o ambiente virtual
python -m venv venv

# Ativar no Windows
venv\Scripts\activate

# Ativar no macOS/Linux
source venv/bin/activate
```

### 2. Instalação das Dependências

Com o ambiente virtual ativado, instale todas as bibliotecas necessárias:

```bash
pip install -r requirements.txt
```

### 3. Configuração do Banco de Dados

1.  Acesse seu MySQL e crie o banco de dados para o projeto. Recomendamos o nome `rharmony_db`.
    ```sql
    CREATE DATABASE rharmony_db;
    ```
2.  Abra o arquivo `instance/config.py`.
3.  Atualize a linha `SQLALCHEMY_DATABASE_URI` com suas credenciais do MySQL e o nome do banco de dados que você criou.
    ```python
    SQLALCHEMY_DATABASE_URI = 'mysql://SEU_USUARIO:SUA_SENHA@localhost:3306/rharmony_db'
    ```

### 4. Execução da Aplicação

1.  Certifique-se de que seu ambiente virtual está ativado.
2.  Execute o arquivo `run.py` na raiz do projeto:
    ```bash
    python run.py
    ```
3.  A aplicação será iniciada! Na primeira vez, ela criará automaticamente todas as tabelas (`gestor`, `veiculo`, `documento`) no seu banco de dados.
4.  Abra seu navegador e acesse: **http://127.0.0.1:5000/**

## 📂 Estrutura do Projeto

```
/
|-- app/                    # Pacote principal da aplicação
|   |-- static/             # Arquivos estáticos (CSS, JS, Imagens)
|   |-- templates/          # Arquivos HTML (Jinja2)
|   |-- __init__.py         # Fábrica da aplicação
|   |-- forms.py            # Definição dos formulários (Flask-WTF)
|   |-- models.py           # Modelos do banco de dados (SQLAlchemy)
|   `-- routes.py           # Lógica das rotas e views
|-- instance/
|   `-- config.py           # Arquivo de configuração (não versionado)
|-- venv/                   # Ambiente virtual
|-- requirements.txt        # Lista de dependências Python
`-- run.py                  # Ponto de entrada para executar a aplicação
```

## ✒️ Autores

* **Mariana Leite Ribeiro**
* **Vitor Ribeiro Soares**
