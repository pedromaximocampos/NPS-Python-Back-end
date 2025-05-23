from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from src.Infra.Config import sql_connection
from typing import Dict, Any
from marshmallow import Schema, fields, post_load


class ContactEntity(sql_connection.get_db().Model):
    id = Column(Integer, primary_key=True)
    nome = Column(String(255), nullable=True)
    email = Column(String(255), nullable=False)
    telefone = Column(String(255), nullable=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    
    user = relationship('User', backref='contatos')
    
    def __repr__(self):
        return f"<Contatos(id={self.id}, nome='{self.nome}', email='{self.email}', telefone='{self.telefone}')>"
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'nome': self.nome,
            'email': self.email,
            'telefone': self.telefone,
        }
    
    @classmethod
    def validate_and_create(cls, data, user_id):
        
        if not data.get('email'):
            raise ValueError("Email é obrigatório")
        
        return cls(
            nome=data.get('nome'),
            email=data.get('email'),
            user_id=user_id
        )


    def update(self, data):
        try: 
            for key, value in data.items():
                setattr(self, key, value)
            return self
        except Exception as e:
            raise e
