from sqlalchemy.orm import Session
from models.veterinario import Veterinario
from models.atendimento import Atendimento
from repositories import BaseRepository

class VeterinarioRepository(BaseRepository[Veterinario]):
    # Repositório para operações com a entidade Veterinario.
    def __init__(self, session: Session):
        super().__init__(Veterinario, session)
    
    def get_atends(self, vet_id: int) -> list[Atendimento]:
        # Retorna os atendimentos de um veterinario específico.
        # vet_id: O ID do tutor.
        # return: Uma lista de objetos Atendimento, ou uma lista vazia se o veterinario não for encontrado.
        # 1. Primeiro, encontramos a clínica pelo seu ID
        vet = self.get_by_id(vet_id)

        # 2. Se o veterinario existir, simplesmente retornamos o atributo do relacionamento.
        if vet:
            return vet.atendimentos
        
        # Se o veterinario não for encontrado, retornamos uma lista vazia.
        return []