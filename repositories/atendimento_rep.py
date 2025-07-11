from sqlalchemy.orm import Session
from models.atendimento import Atendimento
from repositories import BaseRepository

class AtendimentoRepository(BaseRepository[Atendimento]):
    # Repositório para operações com a entidade Atendimento.
    def __init__(self, session: Session):
        super().__init__(Atendimento, session)