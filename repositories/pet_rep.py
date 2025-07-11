from sqlalchemy.orm import Session
from models.pet import Pet
from models.atendimento import Atendimento
from repositories import BaseRepository

class PetRepository(BaseRepository[Pet]):
    # Repositório para operações com a entidade Pet.
    def __init__(self, session: Session):
        super().__init__(Pet, session)
    
    def get_atends(self, pet_id: int) -> list[Atendimento]:
        # Retorna os atendimentos de um pet específico.
        pet = self.get_by_id(pet_id)

        if pet:
            return pet.atendimentos
        
        # Se nao encontrar, retorna lista vazia
        return []