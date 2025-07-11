from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from . import Base

class Pet(Base):
    __tablename__ = 'pets'

    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    especie = Column(String(50))
    idade = Column(Integer)
    tutor_id = Column(Integer, ForeignKey('tutores.id'))

    tutor = relationship("Tutor", back_populates="pets")
    atendimentos = relationship("Atendimento", back_populates="pet")

    def __repr__(self):
        return f"<Pet(nome='{self.nome}', especie='{self.especie}')>"
    
    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "especie": self.especie,
            "idade": self.idade,
            "tutor_id": self.tutor_id
        }