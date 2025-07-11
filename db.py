from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from flask import g
from models import Base

DATABASE_URL = "postgresql+psycopg2://postgres:admin@localhost:5432/bd_vet"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)

def get_db_session() -> Session:
    
    if 'db_session' not in g:
        g.db_session = SessionLocal()
    return g.db_session

def init_db():
    """
    Função para inicializar o banco de dados.
    Ela importa todos os modelos para que sejam registrados nos metadados da Base
    e então cria todas as tabelas no banco de dados.
    """
    # É crucial importar todos os seus modelos aqui antes de chamar create_all
    # para que o SQLAlchemy saiba quais tabelas criar.
    print("Importando modelos para criação das tabelas...")
    from models.clinica import Clinica
    from models.veterinario import Veterinario
    from models.tutor import Tutor
    from models.pet import Pet
    from models.atendimento import Atendimento
    
    print("Criando tabelas no banco de dados...")
    # O comando create_all usa a 'engine' para criar as tabelas.
    Base.metadata.create_all(bind=engine)
    print("Tabelas criadas com sucesso!")
