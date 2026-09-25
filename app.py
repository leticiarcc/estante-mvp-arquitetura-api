# app.py
from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func
from datetime import datetime
from model import Session, Livro
from schemas import *
from flask_cors import CORS
from services.google_books_service import buscar_por_titulo, GoogleBooksError

info = Info(title="API Estante Virtual", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

home_tag = Tag(
    name="Documentação", description="Documentações: Swagger, Redoc ou RapiDoc"
)
livro_tag = Tag(
    name="Estante de Livros",
    description="Adição, visualização, edição, remoção e visualização de estatísticas dos livros cadastrados na estante virtual.",
)
google_books_tag = Tag(
    name="Google Books",
    description="Busca de sugestões de livros na API externa do Google Books, usada para auto-preenchimento do formulário de cadastro.",
)


@app.get("/", tags=[home_tag])
def home():
    """Redireciona para a documentação da API (Swagger)."""
    return redirect("/openapi")


@app.get(
    "/buscarlivrogoogle",
    tags=[google_books_tag],
    summary="Busca sugestões de livros no Google Books pelo título",
    responses={"200": ListagemSugestoesGoogleSchema, "400": ErrorSchema},
)
def buscar_livro_google(query: BuscaGoogleBooksSchema):
    """Busca sugestões de livros na API externa do Google Books, filtrando
    exclusivamente pelo título informado (operador 'intitle:').
    """
    try:
        sugestoes = buscar_por_titulo(query.titulo)
        return {"sugestoes": sugestoes}, 200
    except GoogleBooksError:
        error_msg = "Não foi possível consultar o Google Books no momento :/"
        return {"message": error_msg}, 400


@app.post(
    "/cadastrarlivro",
    tags=[livro_tag],
    summary="Cadastra um novo livro",
    responses={"200": LivroViewSchema, "409": ErrorSchema, "400": ErrorSchema},
)
def add_livro(body: LivroCadastroSchema):
    """Cadastra um novo livro na estante.

    Regras de negócio:
        - O título do livro deve ser único na estante (tentativa de duplicado retorna 409).
        - Se status = 'Estou lendo', recomenda-se informar 'data_inicio' e 'pagina_atual', além de: 'titulo', 'autor', 'genero', 'status' e 'qtde_paginas' (Estrutura base para o livro).
        - Se status = 'Concluído', recomenda-se informar 'data_fim' e 'nota' (de 1 a 5 estrelas), além de: 'titulo', 'autor', 'genero', 'status' e 'qtde_paginas' (Estrutura base para o livro).
        - Se status = 'Quero ler', recomenda-se informar apenas: 'titulo', 'autor', 'genero', 'status' e 'qtde_paginas'.


    Retorna o livro cadastrado, incluindo o ID gerado pelo banco de dados.
    """
    livro = Livro(
        titulo=body.titulo,
        autor=body.autor,
        genero=body.genero,
        qtde_paginas=body.qtde_paginas,
        status=body.status,
        data_inicio=body.data_inicio,
        pagina_atual=body.pagina_atual,
        data_fim=body.data_fim,
        anotacoes=body.anotacoes,
        nota=body.nota,
        capa=body.capa,
    )

    try:
        session = Session()
        session.add(livro)
        session.commit()
        return apresenta_livro(livro), 200

    except IntegrityError as e:
        error_msg = "Livro com o mesmo nome já cadastrado na estante :/"
        return {"message": error_msg}, 409
    except Exception as e:
        error_msg = "Não foi possível salvar o novo livro :/"
        return {"message": error_msg}, 400


@app.get(
    "/listarlivros",
    tags=[livro_tag],
    summary="Lista todos os livros cadastrados",
    responses={"200": ListagemLivrosSchema},
)
def get_livros():
    """Retorna a listagem de todos os livros cadastrados na estante.
    Caso não exista nenhum livro cadastrado, retorna uma lista vazia
    com status 200 (não é considerado um erro).
    """
    session = Session()
    livros = session.query(Livro).all()

    if not livros:
        return {"livros": []}, 200
    else:
        return apresenta_livros(livros), 200

@app.put(
    "/atualizarlivro",
    tags=[livro_tag],
    summary="Atualiza por completo um livro existente",
    responses={"200": LivroViewSchema, "404": ErrorSchema, "400": ErrorSchema},
)
def atualizar_livro(query: LivroBuscaSchema, body: LivroSubstituicaoSchema):
    """Atualiza dados de um livro existente a partir do ID.
    """
    session = Session()
    livro = session.query(Livro).filter(Livro.id == query.id).first()

    if not livro:
        return {"message": "Livro não encontrado"}, 404

    try:
        livro.titulo = body.titulo
        livro.autor = body.autor
        livro.genero = body.genero
        livro.qtde_paginas = body.qtde_paginas
        livro.status = body.status
        livro.data_inicio = body.data_inicio
        livro.pagina_atual = body.pagina_atual
        livro.data_fim = body.data_fim
        livro.anotacoes = body.anotacoes
        livro.nota = body.nota
        livro.capa = body.capa

        session.add(livro)
        session.commit()
        session.refresh(livro)
        return apresenta_livro(livro), 200

    except IntegrityError:
        session.rollback()
        error_msg = "Já existe outro livro com esse título na estante :/"
        return {"message": error_msg}, 409
    except Exception:
        session.rollback()
        return {"message": "Erro ao substituir o livro"}, 400


@app.delete(
    "/deletarlivro",
    tags=[livro_tag],
    summary="Remove um livro da estante",
    responses={"200": LivroDeletaSchema, "404": ErrorSchema},
)
def del_livro(query: LivroBuscaSchema):
    """Remove o registro de um livro a partir do ID."""
    livro_id = query.id
    session = Session()
    count = session.query(Livro).filter(Livro.id == livro_id).delete()
    session.commit()

    if count:
        return {
            "message": "Livro removido com sucesso da estante!",
            "id": livro_id,
        }, 200
    else:
        error_msg = "Livro não encontrado na estante :/"
        return {"message": error_msg}, 404


@app.get(
    "/estatisticas/livros-por-status",
    tags=[livro_tag],
    summary="Retorna a quantidade de livros por status",
    responses={"200": EstatisticasSchema},
)
def get_estatisticas_status():
    """Retorna a quantidade de livros cadastrados em cada status de leitura.
    Os rótulos retornados seguem sempre a mesma ordem fixa:
    ['Concluído', 'Estou lendo', 'Quero ler']. Quando não há nenhum
    livro cadastrado, os valores são retornados como 0 (não há erro 404,
    pois a ausência de dados é um cenário válido).
    """

    session = Session()
    concluidos = session.query(Livro).filter(Livro.status == "Concluído").count()
    lendo = session.query(Livro).filter(Livro.status == "Estou lendo").count()
    quero_ler = session.query(Livro).filter(Livro.status == "Quero ler").count()
    return {
        "labels": ["Concluído", "Estou lendo", "Quero ler"],
        "values": [concluidos, lendo, quero_ler],
    }, 200


@app.get(
    "/estatisticas/livros-concluidos-por-mes",
    tags=[livro_tag],
    summary="Retorna a quantidade de livros concluídos por mês",
    responses={"200": EstatisticasSchema},
)
def livros_por_mes():
    """Retorna a quantidade de livros concluídos, agrupados por mês de conclusão.
    Apenas livros com 'data_fim' preenchida são considerados. Os meses são
    retornados no formato 'YYYY-MM', ordenados cronologicamente. Quando não
    há nenhum livro concluído, ambas as listas são retornadas vazias com
    status 200 (não é considerado um erro).
    """
    session = Session()
    livros = session.query(Livro).filter(Livro.data_fim != None).all()
    contagem = {}

    for livro in livros:
        if livro.data_fim:
            mes = livro.data_fim.strftime("%Y-%m")

            if mes in contagem:
                contagem[mes] += 1
            else:
                contagem[mes] = 1

    """ Ordena por mês 
    """
    meses_ordenados = sorted(contagem.keys())

    labels = []
    values = []
    for mes in meses_ordenados:
        labels.append(mes)
        values.append(contagem[mes])
    return {"labels": labels, "values": values}, 200


@app.get(
    "/estatisticas/paginas-lidas-por-mes",
    tags=[livro_tag],
    summary="Retorna a soma de páginas lidas por mês",
    responses={"200": EstatisticasSchema},
)
def paginas_lidas_por_mes():
    """Retorna a soma de páginas dos livros concluídos, agrupadas por mês
    de conclusão. Apenas livros com 'data_fim' preenchida são considerados. Quando não
    há nenhum livro concluído, ambas as listas são retornadas vazias com
    status 200 (não é considerado um erro).
    """
    session = Session()
    livros = session.query(Livro).filter(Livro.data_fim != None).all()
    soma_paginas = {}

    for livro in livros:
        if livro.data_fim:
            mes = livro.data_fim.strftime("%Y-%m")
            paginas = livro.qtde_paginas or 0

            if mes in soma_paginas:
                soma_paginas[mes] += paginas
            else:
                soma_paginas[mes] = paginas

    meses_ordenados = sorted(soma_paginas.keys())

    labels = []
    values = []
    for mes in meses_ordenados:
        labels.append(mes)
        values.append(soma_paginas[mes])
    return {"labels": labels, "values": values}, 200