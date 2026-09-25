# Estrutura para chamar a api do Google Books
import os
import requests
from dotenv import load_dotenv

load_dotenv()

GOOGLE_BOOKS_URL = "https://www.googleapis.com/books/v1/volumes"
GOOGLE_BOOKS_API_KEY = os.getenv("GOOGLE_BOOKS_API_KEY")

# Tradução das categorias mais comuns do Google Books para português. Categorias não mapeadas aqui são exibidas no idioma original (inglês).
TRADUCAO_GENEROS = {
    "fiction": "Ficção",
    "juvenile fiction": "Ficção Juvenil",
    "young adult fiction": "Ficção Jovem Adulto",
    "biography & autobiography": "Biografia e Autobiografia",
    "history": "História",
    "poetry": "Poesia",
    "drama": "Drama",
    "romance": "Romance",
    "science fiction": "Ficção Científica",
    "fantasy": "Fantasia",
    "horror": "Terror",
    "mystery": "Mistério",
    "thriller": "Suspense",
    "comics & graphic novels": "Quadrinhos e Graphic Novels",
    "self-help": "Autoajuda",
    "business & economics": "Negócios e Economia",
    "philosophy": "Filosofia",
    "religion": "Religião",
    "psychology": "Psicologia",
    "science": "Ciência",
    "cooking": "Culinária",
    "art": "Arte",
    "travel": "Viagem",
    "true crime": "Crime Real",
    "juvenile nonfiction": "Não Ficção Juvenil",
    "literary criticism": "Crítica Literária",
    "family & relationships": "Família e Relacionamentos",
    "health & fitness": "Saúde e Bem-estar",
}


def traduzir_genero(genero_original: str) -> str:
    """
    Traduz categorias do Google Books (em inglês) para português,
    usando um dicionário de termos comuns. Categorias com múltiplos
    valores (separadas por vírgula) são traduzidas individualmente.
    Termos não mapeados são mantidos no idioma original.
    """
    if not genero_original:
        return genero_original

    partes = [parte.strip() for parte in genero_original.split(",")]
    traduzidas = []

    for parte in partes:
        traducao = TRADUCAO_GENEROS.get(parte.lower())
        traduzidas.append(traducao if traducao else parte)

    return ", ".join(traduzidas)


class GoogleBooksError(Exception):
    """Erro ao consultar a API do Google Books (rede, timeout, resposta inválida etc.)"""
    pass


def buscar_por_titulo(titulo: str, max_resultados: int = 5) -> list[dict]:
    """
    Busca livros no Google Books filtrando SOMENTE pelo título.

    Usa o operador 'intitle:' da API pra restringir a busca ao campo
    título, evitando que o termo digitado pelo usuário busque também
    em autor, editora etc.
    """
    titulo_limpo = (titulo or "").strip()

    if len(titulo_limpo) < 3:
        return []

    params = {
        "q": f"intitle:{titulo_limpo}",
        "maxResults": max_resultados,
        "langRestrict": "pt",
    }

    if GOOGLE_BOOKS_API_KEY:
        params["key"] = GOOGLE_BOOKS_API_KEY

    try:
        resposta = requests.get(GOOGLE_BOOKS_URL, params=params, timeout=5)
        resposta.raise_for_status()
    except requests.RequestException as erro:
        raise GoogleBooksError(
            f"Falha ao consultar a API do Google Books: {erro}"
        ) from erro

    dados = resposta.json()
    itens = dados.get("items", [])

    sugestoes = []
    for item in itens:
        info = item.get("volumeInfo", {})

        genero_original = ", ".join(info.get("categories", []))
        sugestoes.append(
            {
                "titulo": info.get("title", ""),
                "autor": ", ".join(info.get("authors", [])),
                "genero": traduzir_genero(genero_original),
                "qtde_paginas": info.get("pageCount"),
                "capa": info.get("imageLinks", {}).get("thumbnail", ""),
            }
        )

    return sugestoes
