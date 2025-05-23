from src.Infra.Config import sql_connection
from typing import List, Optional
from src.Infra.Entities.PlanEntity import PlanEntity
from src.Infra.Entities.UserEntity import UserEntity
from src.Enums.PlanInterestEnum import PlanInterestStatusEnum
from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship

class PlanPurchaseInterest(sql_connection.get_db().Model):
    """
    Modelo para registrar o interesse de compra de planos pelos usuários
    
    Attributes:
        id (int): Identificador único do interesse
        user_id (int): ID do usuário interessado
        plan_id (int): ID do plano de interesse
        interest_date (datetime): Data em que o interesse foi registrado
        status (int): Status do interesse (1: pendente, 2: atendido, 3: cancelado)
        notes (str): Observações sobre o interesse
    """
    __tablename__ = 'plan_purchase_interest'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    plan_id = Column(Integer, ForeignKey('plans.id'), nullable=False)
    interest_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    status = Column(Integer, nullable=False, default=PlanInterestStatusEnum.PENDING.value)
    notes = Column(Text, nullable=True)
    
    # Relacionamentos
    user = relationship('User', back_populates='interests')
    plan = relationship('Plan', back_populates='purchase_interests', foreign_keys=[plan_id])
    
    def __repr__(self):
        return f'<PlanPurchaseInterest {self.id}>'
    
    def to_dict(self):
        """
        Converte o objeto de interesse para um dicionário
        
        Returns:
            dict: Dicionário com os dados do interesse
        """
        return {
            'id': self.id,
            'user_id': self.user_id,
            'plan_id': self.plan_id,
            'interest_date': self.interest_date.isoformat(),
            'status': PlanInterestStatusEnum.from_int(self.status).to_str(),
            'notes': self.notes
        }