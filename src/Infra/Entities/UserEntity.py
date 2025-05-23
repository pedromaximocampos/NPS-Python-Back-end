from src.Infra.Config import sql_connection
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from typing import Optional, List, Dict, Any
from src.Infra.Entities.PlanEntity import PlanEntity
from src.Infra.Entities.PlanSubscriptionEntity import PlanSubscriptionEntity
from src.Enums.PlanEnum import PlanEnum
from src.Infra.Entities.UserAdminEntity import UserAdminEntity
from src.Enums.PlanEnum import PlanStatusEnum
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

class UserEntity(sql_connection.get_db().Model):
    """
    Modelo de usuário para o sistema
    
    Attributes:
        id (int): Identificador único do usuário
        nome_completo (str): Nome completo do usuário
        email (str): Email do usuário (único)
        telefone (str): Telefone do usuário
        empresa (str): Nome da empresa
        cargo (str): Cargo do usuário
        cnpj (str): CNPJ da empresa
        password_hash (str): Hash da senha do usuário
        created_at (datetime): Data de criação do usuário
        updated_at (datetime): Data da última atualização
        is_admin (bool): Indica se o usuário é administrador
    """
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    nome_completo = Column(String(50), nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    telefone = Column(String(20), nullable=False)
    empresa = Column(String(150), nullable=False)
    cargo = Column(String(100), nullable=False)
    cnpj = Column(String(20), nullable=False)
    password_hash = Column(String(128), nullable=False)
    is_admin = Column(Boolean, default=False)


    # Relacionamentos
    interests = relationship('PlanPurchaseInterest', back_populates='user', lazy=True)
    planos_contratados = relationship('PlanoContratado', backref='user', lazy=True)
    admin_info = relationship('UserAdmin', back_populates='user', uselist=False, lazy=True)
    
    
    def __repr__(self):
        return f'<User(id={self.id}, nome_completo={self.nome_completo}, email={self.email}, telefone={self.telefone}, empresa={self.empresa}, cargo={self.cargo}, cnpj={self.cnpj}, is_admin={self.is_admin})>'


    def to_dict(self):
        return {
            'id': self.id,
            'nome_completo': self.nome_completo,
            'email': self.email,
            'telefone': self.telefone,
            'empresa': self.empresa,
            'cargo': self.cargo,
            'cnpj': self.cnpj,
            'is_admin': self.is_admin
        }
    
    
    
    
    
