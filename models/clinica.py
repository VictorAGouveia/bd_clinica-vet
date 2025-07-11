from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

# Importa a Base do __init__.py
from . import Base

class Clinica(Base):
    __tablename__ = 'clinicas'

    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    cidade = Column(String(100))

    # O relacionamento usa o NOME DA CLASSE como uma string ("Veterinario")
    # para evitar problemas de importação circular.
    veterinarios = relationship("Veterinario", back_populates="clinica")

    def __repr__(self):
        return f"<Clinica(nome='{self.nome}', cidade='{self.cidade}')>"
    
    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "cidade": self.cidade
        }