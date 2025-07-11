from sqlalchemy.orm import Session
from models.clinica import Clinica
from models.veterinario import Veterinario
from repositories import BaseRepository

class ClinicaRepository(BaseRepository[Clinica]):
    # Repositório para operações com a entidade Clinica.
    def __init__(self, session: Session):
        super().__init__(Clinica, session)

    def get_vets(self, clinica_id: int) -> list[Veterinario]:
        # Retorna os veterinários de uma clínica específica.
        # clinica_id: O ID da clínica.
        # return: Uma lista de objetos Veterinario, ou uma lista vazia se a clínica não for encontrada.
        # 1. Primeiro, encontramos a clínica pelo seu ID
        clinica = self.get_by_id(clinica_id)

        # 2. Se a clínica existir, simplesmente retornamos o atributo do relacionamento.
        if clinica:
            return clinica.veterinarios
        
        # Se a clínica não for encontrada, retornamos uma lista vazia.
        return []