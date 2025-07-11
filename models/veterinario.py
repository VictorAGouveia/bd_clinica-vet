from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from . import Base

class Veterinario(Base):
    __tablename__ = 'veterinarios'

    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    especialidade = Column(String(100))
    clinica_id = Column(Integer, ForeignKey('clinicas.id'))

    # Relacionamentos usando strings para os nomes das classes
    clinica = relationship("Clinica", back_populates="veterinarios")
    atendimentos = relationship("Atendimento", back_populates="veterinario")

    def __repr__(self):
        return f"<Veterinario(nome='{self.nome}')>"
    
    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "especialidade": self.especialidade,
            "clinica_id": self.clinica_id
        }