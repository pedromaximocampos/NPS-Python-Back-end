from src.Infra.Config import sql_connection
from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship

class UserAdminEntity(sql_connection.get_db().Model):
    """
    Modelo para usuários administradores
    
    Attributes:
        id (int): Identificador único do registro de administrador
        user_id (int): ID do usuário que é administrador
        nivel_acesso (str): Nível de acesso do administrador
        data_nomeacao (datetime): Data em que o usuário foi nomeado administrador
    """
    __tablename__ = 'user_admin'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, unique=True)
    nivel_acesso = Column(String(50), nullable=False, default='admin')
    data_nomeacao = Column(DateTime, nullable=False, default=datetime.utcnow)
    
    # Usando string reference para evitar importação circular
    user = relationship('User', back_populates='admin_info', foreign_keys=[user_id])
    
    def __repr__(self):
        return f'<UserAdmin {self.user_id}>'
    