# model livro.py
from model.base import Base
from sqlalchemy import Column, Integer, String, Text, Date
from datetime import date


class Livro(Base):
    __tablename__ = "livros" """ Tabela no SQLite """

    """ Estrutura do livro no banco de dados """
    id = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String(255), nullable=False, unique=True)
    autor = Column(String(255), nullable=False)
    genero = Column(String(100), nullable=True)
    qtde_paginas = Column(Integer, nullable=False)
    status = Column(String(50), nullable=False)
    data_inicio = Column(Date, nullable=True)
    data_fim = Column(Date, nullable=True)
    anotacoes = Column(Text, nullable=True)
    nota = Column(Integer, default=0)
    pagina_atual = Column(Integer, default=0)
    capa = Column(String(500), nullable=True)

    def __init__(
        self,
        titulo: str,
        autor: str,
        genero: str,
        qtde_paginas: int,
        status: str,
        data_inicio: date = None,
        data_fim: date = None,
        anotacoes: str = None,
        nota: int = 0,
        pagina_atual: int = 0,
        capa: str = None,
    ):

        self.titulo = titulo
        self.autor = autor
        self.genero = genero
        self.qtde_paginas = qtde_paginas
        self.status = status
        self.data_inicio = data_inicio
        self.data_fim = data_fim
        self.anotacoes = anotacoes
        self.nota = nota
        self.pagina_atual = pagina_atual
        self.capa = capa