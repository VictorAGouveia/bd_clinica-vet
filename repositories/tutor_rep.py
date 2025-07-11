from sqlalchemy.orm import Session
from models.tutor import Tutor
from models.pet import Pet
from repositories import BaseRepository

class TutorRepository(BaseRepository[Tutor]):
    # Repositório para operações com a entidade Tutor.
    def __init__(self, session: Session):
        # Chama o construtor da classe pai (BaseRepository)
        # passando o modelo Tutor e a sessão.
        super().__init__(Tutor, session)

    def get_pets(self, tutor_id: int) -> list[Pet]:
        # Retorna os pets de um tutor específico.
        # tutor_id: O ID do tutor.
        # return: Uma lista de objetos Pet, ou uma lista vazia se o tutor não for encontrada.
        # 1. Primeiro, encontramos a clínica pelo seu ID
        tutor = self.get_by_id(tutor_id)

        # 2. Se o tutor existir, simplesmente retornamos o atributo do relacionamento.
        if tutor:
            return tutor.pets
        
        # Se o tutor não for encontrado, retornamos uma lista vazia.
        return []
