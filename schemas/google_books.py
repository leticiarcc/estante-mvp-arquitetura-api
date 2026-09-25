from pydantic import BaseModel, Field
from typing import List, Optional


class BuscaGoogleBooksSchema(BaseModel):
    """Estrutura da busca por título de livro na API do Google Books"""

    titulo: str = Field(
        ...,
        min_length=3,
        description="Título do título do livro a ser pesquisado",
    )


class SugestaoGoogleBooksSchema(BaseModel):
    """Estrutura de uma sugestão de livro vinda do Google Books"""

    titulo: str = Field(..., description="Título do livro sugerido")
    autor: str = Field(..., description="Autor(es) do livro, separados por vírgula")
    genero: str = Field(
        "",
        description="Gênero/categoria do livro, quando disponível (ex: Fiction, Romance, etc.)",
    )
    qtde_paginas: Optional[int] = Field(
        None, description="Quantidade de páginas, quando disponível"
    )
    capa: str = Field(
        "",
        description="URL da miniatura da capa, usada para exibição na lista de sugestões",
    )


class ListagemSugestoesGoogleSchema(BaseModel):
    """Lista de sugestões retornadas pela busca no Google Books"""

    sugestoes: List[SugestaoGoogleBooksSchema] = Field(
        ..., description="Sugestões de livros encontradas"
    )