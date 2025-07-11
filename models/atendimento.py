# models/atendimento.py

import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from . import Base

class Atendimento(Base):
    __tablename__ = 'atendimentos'

    id = Column(Integer, primary_key=True)
    data = Column(DateTime, default=datetime.datetime.utcnow)
    descricao = Column(String(255))
    pet_id = Column(Integer, ForeignKey('pets.id'))
    veterinario_id = Column(Integer, ForeignKey('veterinarios.id'))

    pet = relationship("Pet", back_populates="atendimentos")
    
    veterinario = relationship("Veterinario", back_populates="atendimentos")

    def __repr__(self):
        return f"<Atendimento(data='{self.data.strftime('%Y-%m-%d')}')>"
    
    def to_dict(self):
        return {
            "id": self.id,
            "data": self.data.isoformat(),
            "descricao": self.descricao,
            "pet_id": self.pet_id,
            "veterinario_id": self.veterinario_id
        }