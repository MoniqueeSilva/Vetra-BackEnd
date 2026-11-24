# Vetra - Backend

API responsável pelas regras de negócio e pelo gerenciamento das operações do sistema Vetra, desenvolvido para depósitos de bebidas.

O backend foi desenvolvido em Python com Flask e utiliza PostgreSQL para armazenar os dados da aplicação.

## Tecnologias utilizadas

- Python 3.12
- Flask
- PostgreSQL 18
- Psycopg2
- Docker
- Docker Compose

## Estrutura do projeto

O backend possui uma estrutura organizada em módulos:

- `app.py`: inicialização da aplicação Flask.
- `database/`: conexão com o banco de dados e gerenciamento de migrações.
- `repositories/`: acesso e manipulação dos dados.
- `routes/`: definição das rotas da API.
- `services/`: implementação das regras de negócio.
- `requirements.txt`: dependências Python.
- `Dockerfile`: configuração da imagem Docker.
- `docker-compose.yml`: configuração dos serviços da aplicação.

## Dockerfile

O backend utiliza uma imagem baseada em Python 3.12 Slim.

O Dockerfile realiza as seguintes etapas:

1. Define a imagem base Python.
2. Configura o diretório de trabalho.
3. Copia o arquivo de dependências.
4. Instala as bibliotecas necessárias.
5. Copia os arquivos da aplicação.
6. Expõe a porta 5000.
7. Inicia a API Flask.

## Banco de dados

A aplicação utiliza PostgreSQL como banco de dados.

As configurações de conexão são fornecidas por variáveis de ambiente:

- `DB_HOST`
- `DB_PORT`
- `DB_NAME`
- `DB_USER`
- `DB_PASSWORD`

As migrações do banco são executadas automaticamente durante a inicialização do backend pelo Docker Compose.

## Como executar o projeto

### Pré-requisitos

- Git
- Docker
- Docker Compose

### 1. Clonar os repositórios

```bash
mkdir Vetra
cd Vetra

git clone https://github.com/MoniqueeSilva/Vetra-BackEnd.git
git clone https://github.com/MoniqueeSilva/Vetra-FrontEnd.git
```

### 2. Acessar o backend

```bash
cd Vetra-BackEnd
```

### 3. Construir e iniciar os containers

```bash
docker compose up --build -d
```

O Docker Compose iniciará três serviços:

- PostgreSQL: banco de dados.
- Backend: API Flask.
- Frontend: aplicação React servida pelo Nginx.

### 4. Verificar os containers

```bash
docker compose ps
```

### 5. Consultar os logs

```bash
docker compose logs -f
```

### 6. Encerrar os serviços

```bash
docker compose down
```

Os dados do PostgreSQL são armazenados em um volume Docker chamado `postgres_data`, permitindo sua persistência mesmo após a remoção dos containers.

## Endereços de acesso

| Serviço | Endereço |
|---|---|
| API Backend | http://localhost:5000 |
| Frontend | http://localhost:5173 |
| PostgreSQL | Acesso interno pela rede Docker, porta 5432 |

## Repositórios relacionados

- **Backend:** https://github.com/MoniqueeSilva/Vetra-BackEnd
- **Frontend:** https://github.com/MoniqueeSilva/Vetra-FrontEnd
