from datetime import datetime
from src.Infra.Config import sql_connection
from typing import Optional, Dict, Any
from src.Infra.Entities.PlanEntity import PlanEntity
from src.Enums.PlanEnum import PlanStatusEnum
from sqlalchemy import Column, Integer, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship


class PlanSubscriptionEntity(sql_connection.get_db().Model):
    """
    Modelo para gerenciar os planos contratados pelos usuários
    
    Attributes:
        id (int): Identificador único do plano contratado
        user_id (int): ID do usuário
        plan_id (int): ID do plano
        limite_pesquisas (int): Limite de pesquisas disponíveis
        status (str): Status do plano (ATIVO/INATIVO)
    """
    __tablename__ = 'user_subscription'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    plan_id = Column(Integer, ForeignKey('plans.id'), nullable=False)
    limite_pesquisas = Column(Integer, nullable=False)
    limite_de_envios = Column(Integer, nullable=False)
    status = Column(String(50), nullable=False)
    
    # Relacionamentos
    user = relationship('User', back_populates='subscriptions')
    plan = relationship('Plan', back_populates='subscriptions')
    
    def __repr__(self):
        return f'<PlanSubscription {self.id} user_id={self.user_id} plan_id={self.plan_id} limite_pesquisas={self.limite_pesquisas} limite_de_envios={self.limite_de_envios} status={self.status}>'
    
    
    def to_dict(self):
        """
        Converte o objeto PlanSubscription em um dicionário
        
        Returns:
            dict: Dicionário com os dados do plano contratado
        """
        return {
            'id': self.id,
            'user_id': self.user_id,
            'plan_id': self.plan_id,
            'limite_pesquisas': self.limite_pesquisas,
            'limite_de_envios': self.limite_de_envios,
        }