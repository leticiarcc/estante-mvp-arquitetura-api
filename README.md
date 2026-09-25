# Título: Estante Virtual

Backend da aplicação **Estante Virtual**, desenvolvido para a disciplina *Arquitetura de Software*. Esta API é responsável por toda a regra de negócio e persistência dos livros cadastrados pelo usuário, oferecendo rotas para **cadastro, listagem, edição, remoção**, **busca de livros na API externa do Google Books** (para auto-preenchimento do formulário) e **estatísticas** de leitura.

A documentação interativa da API é gerada automaticamente via **Swagger (OpenAPI)**.

---

## Tecnologias utilizadas

- **Python**
- **Flask** — framework web
- **flask-openapi3** — geração automática de documentação Swagger
- **SQLAlchemy** — ORM para manipulação do banco de dados
- **SQLite** — banco de dados
- **Pydantic** — validação e tipagem de dados das requisições
- **Flask-CORS** — liberação de requisições de origens externas
- **requests** — comunicação HTTP com a API externa do Google Books
- **python-dotenv** — carregamento de variáveis de ambiente a partir do arquivo `.env`
- **Google Books API** — API externa consumida pelo backend para sugestão e auto-preenchimento de dados de livros
- **Docker** — containerização da aplicação

---

## Google Books API (serviço externo)

O projeto consome a **[Google Books API](https://developers.google.com/books)**, um serviço público e gratuito do Google, usado para auto-preenchimento do formulário de cadastro.

### Licença de uso

Regida pelos [Termos de Serviço das APIs do Google](https://developers.google.com/terms). Não é uma licença open source — é um serviço gratuito do Google, sem custo dentro da cota gratuita.

### Cadastro e cota de uso

- **Não é obrigatório** ter chave para realizar buscas — a API aceita requisições sem autenticação, sujeitas a uma cota diária compartilhada e mais restrita
- **Recomendado**: gerar uma chave gratuita no [Google Cloud Console](https://console.cloud.google.com/), o que vincula a cota ao projeto individual (ver passo a passo na seção [Configure a chave da API do Google Books](#2-configure-a-chave-da-api-do-google-books)). A criação e o uso da chave também não geram custos adicionais.

### Rota consumida

| Endpoint da API externa | Método | Uso no projeto |
|---|---|---|
| `https://www.googleapis.com/books/v1/volumes` | `GET` | Busca por título (`q=intitle:{titulo}`), em `services/google_books_service.py` |

Consumida exclusivamente pelo **backend** — o frontend nunca chama a API do Google diretamente. Isso evita expor a chave no navegador e permite tratar a resposta antes de repassá-la. A própria rota da nossa API que expõe essa busca é `GET /buscarlivrogoogle?titulo={titulo}` (ver [Resumo das rotas da estante](#resumo-das-rotas-da-estante)).

### Como funciona o fluxo

1. O usuário digita o título de um livro no formulário de cadastro (frontend)
2. O frontend chama `GET /buscarlivrogoogle?titulo=...` no backend
3. O backend consulta a API do Google, filtrando pelo título (`intitle:`)
4. Os resultados são tratados e devolvidos ao frontend, que exibe sugestões (título, autor, capa)
5. Ao selecionar uma sugestão, o formulário é preenchido automaticamente

### Limitações conhecidas

- O campo de gênero, quando disponível, costuma vir em inglês e nem sempre está preenchido — principalmente em edições nacionais
- A busca é restrita ao campo de título, por escolha de design do projeto

**Documentação oficial:** [developers.google.com/books/docs/v1/using](https://developers.google.com/books/docs/v1/using)

---

## Pré-requisitos

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) instalado e em execução
- *(Opcional)* Um editor de código, caso queira inspecionar ou editar o código-fonte (ex: VS Code)
- *(Opcional)* Uma extensão ou software para visualizar o banco SQLite gerado (ex: extensão **SQLite Viewer** no VS Code, ou o **DB Browser for SQLite**)

---

## Instalação e configuração do ambiente

### 1. Clone o repositório ou realize o download do arquivo zip no repositório

### 2. Configure a chave da API do Google Books

O arquivo `.env` na raiz do projeto contém a variável usada pela integração com o Google Books:

```dotenv
GOOGLE_BOOKS_API_KEY=
```

Para obter uma chave gratuita:

1. Acesse o [Google Cloud Console](https://console.cloud.google.com/)
2. Crie um projeto (ou use um existente) e ative a **Books API**
3. Em *APIs e Serviços → Credenciais*, gere uma **Chave de API**
4. Cole o valor gerado no `.env`, na variável `GOOGLE_BOOKS_API_KEY`

### 3. Banco de dados

O banco de dados **SQLite** é criado automaticamente na primeira execução da aplicação — não é necessário nenhum passo manual de criação de tabelas.

---

## Como executar o projeto

**Antes de tudo**, edite o arquivo `app_api/.env` e insira a chave da API do Google Books na variável `GOOGLE_BOOKS_API_KEY`.

Com o [Docker Desktop](https://www.docker.com/products/docker-desktop/) instalado e em execução, na raiz do projeto:

```bash
# Cria a rede compartilhada com o frontend (executar uma única vez)
docker network create estante-network

# Builda a imagem do backend (inclusão da chave antes de buildar)
docker build -t estante-backend ./app_api

# Roda o container
docker run -d --name backend --network estante-network -p 5000:5000 -v ${PWD}/app_api/database:/app/database estante-backend
```

O servidor rodará em `http://localhost:5000`.

---

## Documentação da API (Swagger)

Após iniciar o servidor, acesse a documentação da API em:

http://localhost:5000/openapi


Nela é possível visualizar todas as rotas disponíveis, os métodos HTTP, os parâmetros esperados, os formatos de requisição/resposta e os possíveis códigos de status, além de poder testar cada rota diretamente pelo navegador.

### Resumo das rotas da estante

| Método | Rota | Descrição |
|---|---|---|
| `GET` | `/` | Redireciona para a documentação Swagger |
| `POST` | `/cadastrarlivro` | Cadastra um novo livro na estante |
| `GET` | `/listarlivros` | Lista todos os livros cadastrados |
| `GET` | `/buscarlivrogoogle?titulo={titulo}` | Busca sugestões de livros na API do Google Books, filtrando por título |
| `PUT` | `/atualizarlivro?id={id}` | Substitui integralmente os dados de um livro existente |
| `DELETE` | `/deletarlivro?id={id}` | Remove um livro da estante |
| `GET` | `/estatisticas/livros-por-status` | Retorna a quantidade de livros por status de leitura |
| `GET` | `/estatisticas/livros-concluidos-por-mes` | Retorna a quantidade de livros concluídos, agrupados por mês |
| `GET` | `/estatisticas/paginas-lidas-por-mes` | Retorna a soma de páginas lidas, agrupadas por mês |

---

## Estrutura simplificada do projeto

.
├── database/ # Arquivo do banco SQLite (gerado automaticamente)
├── model/
│ ├── init.py # Inicialização do pacote e configuração da sessão/engine
│ ├── base.py # Configuração base do SQLAlchemy (Base declarativa)
│ └── livro.py # Definição da tabela/modelo Livro
├── schemas/
│ ├── init.py # Inicialização do pacote de schemas
│ ├── error.py # Schema padrão de retorno de erros
│ ├── livro.py # Schemas de validação e serialização do Livro (Pydantic)
│ └── google_books.py # Schemas da busca e sugestões do Google Books
├── services/
│ ├── init.py # Inicialização do pacote de services
│ └── google_books_service.py # Lógica de comunicação com a API do Google Books
├── app.py # Rotas da API e regras de negócio
├── requirements.txt # Dependências do projeto
├── Dockerfile # Imagem do backend
├── .env # Variáveis de ambiente (chave da API do Google Books)
└── README.md # Este arquivo

---

## Dependências e versões

Referência técnica das bibliotecas usadas no projeto (já incluídas na imagem Docker, sem necessidade de instalação manual):

| Biblioteca | Versão |
|---|---|
| Flask | 3.0.3 |
| Flask-Cors | 4.0.1 |
| flask-openapi3[swagger] | 3.1.2 |
| pydantic | 2.7.1 |
| SQLAlchemy | 2.0.30 |
| SQLAlchemy-Utils | 0.41.2 |
| requests | 2.34.2 |
| python-dotenv | 1.2.3 |