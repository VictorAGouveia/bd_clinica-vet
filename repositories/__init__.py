from typing import Generic, Type, TypeVar
from sqlalchemy.orm import Session
from models import Base

# Tipagem generica para o modelo do SQLAlchemy
ModelType = TypeVar("ModelType", bound=Base)

class BaseRepository(Generic[ModelType]):
    # Repositorio base com operacoes Read e Create genericas.
    def __init__(self, model: Type[ModelType], session: Session):
        # Construtor do repositorio base.

        #model: O modelo do SQLAlchemy com o qual o repositorio ira trabalhar.
        #session: A sessao do banco de dados a ser usada.
        self.model = model
        self.db_session = session

    def create(self, entity: ModelType) -> ModelType:
        # Cria uma nova entidade no banco de dados.
        self.db_session.add(entity)
        self.db_session.commit()
        self.db_session.refresh(entity) # Atualiza o objeto com o ID do banco
        return entity

    def get_all(self) -> list[ModelType]:
        # Retorna todas as entidades de um tipo.
        return self.db_session.query(self.model).all()

    def get_by_id(self, entity_id: int) -> ModelType | None:
        # Retorna uma entidade pelo seu ID.
        return self.db_session.query(self.model).get(entity_id)