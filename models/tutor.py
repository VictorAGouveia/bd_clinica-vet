from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from . import Base

class Tutor(Base):
    __tablename__ = 'tutores'

    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    telefone = Column(String(20))

    pets = relationship("Pet", back_populates="tutor")

    def __repr__(self):
        return f"<Tutor(nome='{self.nome}')>"

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "telefone": self.telefone
        }