# schemas livro.py
from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from datetime import date


class LivroCadastroSchema(BaseModel):
    """Estrutura de um livro (inclusão)"""

    titulo: str = Field(..., description="Título do livro. Deve ser único na estante")
    autor: str = Field(..., description="Autor do livro")
    genero: str = Field(..., description="Gênero do livro")
    qtde_paginas: int = Field(..., description="Quantidade total de páginas do livro")
    status: str = Field(
        ..., description="Status de leitura (Quero ler, Estou lendo, Concluido)"
    )
    data_inicio: Optional[date] = Field(
        None,
        description="Data de início da leitura. Obrigatória quando status = 'Estou lendo'",
    )
    pagina_atual: Optional[int] = Field(0, description="Página onde a leitura parou")
    data_fim: Optional[date] = Field(
        None,
        description="Data de conclusão da leitura. Obrigatória quando status = 'Concluido'",
    )
    anotacoes: Optional[str] = Field(
        None, description="Considerações e pensamentos sobre o livro"
    )
    nota: Optional[int] = Field(
        0, description="Nota de 1 a 5 estrelas. Usado quando status = 'Concluido'"
    )
    capa: Optional[str] = Field(
        None, description="URL da capa do livro, obtida via busca no Google Books"
    )

    @field_validator("data_inicio", "data_fim", mode="before")
    @classmethod
    def vazio_para_none(cls, valor):
        if valor in ("", "string", None):
            return None
        return valor


class LivroEdicaoSchema(BaseModel):
    """Estrutura de um livro (edição) - campos opcionais para edições parciais"""

    titulo: Optional[str] = Field(None, description="Título do livro")
    autor: Optional[str] = Field(None, description="Autor do livro")
    genero: Optional[str] = Field(None, description="Gênero do livro")
    qtde_paginas: Optional[int] = Field(
        None, description="Quantidade total de páginas do livro"
    )
    status: Optional[str] = Field(
        None, description="Status de leitura (Quero ler, Estou lendo, Concluido)"
    )
    data_inicio: Optional[date] = Field(
        None,
        description="Data de início da leitura. Obrigatória quando status = 'Estou lendo'",
    )
    pagina_atual: Optional[int] = Field(None, description="Página onde a leitura parou")
    data_fim: Optional[date] = Field(
        None,
        description="Data de conclusão da leitura. Obrigatória quando status = 'Concluido'",
    )
    anotacoes: Optional[str] = Field(
        None, description="Considerações e pensamentos sobre o livro"
    )
    nota: Optional[int] = Field(
        None, description="Nota de 1 a 5 estrelas. Usado quando status = 'Concluido'"
    )
    capa: Optional[str] = Field(
        None, description="URL da capa do livro"
    )

    @field_validator("data_inicio", "data_fim", mode="before")
    @classmethod
    def vazio_para_none(cls, valor):
        if valor in ("", "string", None):
            return None
        return valor

class LivroSubstituicaoSchema(BaseModel):
    """Estrutura de um livro (substituição completa via PUT). Todos os campos são obrigatórios."""

    titulo: str = Field(..., description="Título do livro")
    autor: str = Field(..., description="Autor do livro")
    genero: str = Field(..., description="Gênero do livro")
    qtde_paginas: int = Field(..., description="Quantidade total de páginas do livro")
    status: str = Field(
        ..., description="Status de leitura (Quero ler, Estou lendo, Concluido)"
    )
    data_inicio: Optional[date] = Field(None, description="Data de início da leitura")
    pagina_atual: Optional[int] = Field(0, description="Página onde a leitura parou")
    data_fim: Optional[date] = Field(None, description="Data de conclusão da leitura")
    anotacoes: Optional[str] = Field(None, description="Anotações sobre o livro")
    nota: Optional[int] = Field(0, description="Nota de 1 a 5 estrelas")
    capa: Optional[str] = Field(None, description="URL da capa do livro, obtida via busca no Google Books"
    )

    @field_validator("data_inicio", "data_fim", mode="before")
    @classmethod
    def vazio_para_none(cls, valor):
        if valor in ("", "string", None):
            return None
        return valor

class LivroBuscaSchema(BaseModel):
    """Estrutura de um livro (busca)"""

    id: int = Field(..., description="ID único do livro no banco")


class EstatisticasSchema(BaseModel):
    """Estrutura de retorno para os dados dos gráficos de estatísticas (por status ou por mês)"""

    labels: List[str] = Field(
        ..., description="Rótulos do gráfico (nome dos status ou dos meses)"
    )
    values: List[int] = Field(..., description="Valores do gráfico")


class LivroViewSchema(BaseModel):
    """Estrutura de retorno de um livro (visualização)"""

    id: int = Field(..., description="ID único do livro no banco")
    titulo: str = Field(..., description="Título do livro")
    autor: str = Field(..., description="Autor do livro")
    genero: str = Field(..., description="Gênero do livro")
    qtde_paginas: int = Field(..., description="Quantidade total de páginas do livro")
    status: str = Field(
        ..., description="Status de leitura (Quero ler, Estou lendo, Concluido)"
    )
    data_inicio: Optional[date] = Field(
        None,
        description="Data de início da leitura. Obrigatória quando status = 'Estou lendo'",
    )
    pagina_atual: Optional[int] = Field(None, description="Página onde a leitura parou")
    data_fim: Optional[date] = Field(
        None,
        description="Data de conclusão da leitura. Obrigatória quando status = 'Concluido'",
    )
    anotacoes: Optional[str] = Field(
        None, description="Considerações e pensamentos sobre o livro"
    )
    nota: Optional[int] = Field(
        None, description="Nota de 1 a 5 estrelas. Usado quando status = 'Concluido'"
    )
    capa: Optional[str] = Field(
        None, description="URL da capa do livro"
    )


class LivroDeletaSchema(BaseModel):
    """Estrutura do retorno após uma remoção"""

    message: str = Field(..., description="Mensagem de confirmação da remoção")
    id: int = Field(..., description="ID do livro removido")


class ListagemLivrosSchema(BaseModel):
    """Define como uma lista de livros será retornada"""

    livros: List[LivroViewSchema] = Field(
        ..., description="Lista de livros cadastrados na estante"
    )


def apresenta_livro(livro):
    """Registro de um livro"""
    return {
        "id": livro.id,
        "titulo": livro.titulo,
        "autor": livro.autor,
        "genero": livro.genero,
        "qtde_paginas": livro.qtde_paginas,
        "status": livro.status,
        "data_inicio": livro.data_inicio.isoformat() if livro.data_inicio else None,
        "pagina_atual": livro.pagina_atual,
        "data_fim": livro.data_fim.isoformat() if livro.data_fim else None,
        "anotacoes": livro.anotacoes,
        "nota": livro.nota,
        "capa": livro.capa,
    }


def apresenta_livros(livros):
    """Lista de todos os livros cadastrados"""
    result = []
    for livro in livros:
        result.append(apresenta_livro(livro))
    return {"livros": result}
