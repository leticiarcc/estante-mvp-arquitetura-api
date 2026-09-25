from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os

from model.base import Base
from model.livro import Livro

db_path = "database/"

# Verifica se o diretório não existe e o cria
if not os.path.exists(db_path):
    os.makedirs(db_path)

# URL de acesso ao banco SQLite
db_url = "sqlite:///%s/livros_estante.sqlite3" % db_path

# Cria a engine de conexão com o banco
engine = create_engine(db_url, echo=False)

# Session que o app.py usa pra interagir com o banco 'livros_estante'
Session = sessionmaker(bind=engine)

# Cria o arquivo se identificar que não existe
if not database_exists(engine.url):
    create_database(engine.url)

# Cria a tabela se identificar que não existe
Base.metadata.create_all(engine)
