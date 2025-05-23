from datetime import datetime
from src.Infra.Config import sql_connection
from typing import Optional, Dict, Any
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class QuestionOptionsEntity(sql_connection.get_db().Model):
    __tablename__ = 'question_options'
    
    id = Column(Integer, primary_key=True)
    questao_id = Column(Integer, ForeignKey('questions.id'), nullable=False)
    texto = Column(String(255), nullable=False)

    # Relacionamentos
    questao = relationship('QuestionEntity', backref='opcoes')
    
    def __repr__(self):
        return f"<OpcoesQuestao(id={self.id}, texto='{self.texto}')>"
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'texto': self.texto,
            'questao_id': self.questao_id,
        }



