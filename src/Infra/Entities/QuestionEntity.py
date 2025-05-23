from datetime import datetime
from src.Infra.Config import sql_connection
from typing import Optional, Dict, Any, List
from src.Enums.QuestionTypeEnum import QuestionTypeEnum
from src.Infra.Entities.QuestionOptionsEntity import  QuestionOptionsEntity
from sqlalchemy import or_, Integer, String, ForeignKey, Column
from sqlalchemy.orm import joinedload, relationship


class QuestionEntity(sql_connection.get_db().Model):
    __tablename__ = 'questions'
    
    id = Column(Integer, primary_key=True)
    texto = Column(String(255), nullable=False)
    tipo = Column(String(50), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)

    # Relacionamentos
    usuario = relationship('User', backref='questoes')
    opcoes = relationship('QuestionOptionsEntity', backref='questoes')
    
    def __repr__(self):
        return f"<Questao(id={self.id}, texto='{self.texto}', tipo='{self.tipo}')>"
    
    
    def to_dict(self) -> Dict[str, Any]:
        try:
            if self.tipo == QuestionTypeEnum.MULTIPLE_CHOICE.value:
                opcoes = []
                for op in self.opcoes:
                    opcoes.append({"id": op.id, "texto": op.texto})
                
            else:
                opcoes = None
        
            return {
                "id": self.id,
                "texto": self.texto,
                "tipo": self.tipo,
                "user_id": self.user_id if self.user_id else None,
                "opcoes": opcoes
                }
        
        except Exception as e:
            print(e)
            raise e