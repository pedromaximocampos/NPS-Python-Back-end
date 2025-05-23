from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from src.Infra.Config import sql_connection
from marshmallow import Schema, fields, post_load

class PlanEntity(sql_connection.get_db().Model):
    """
    Modelo de plano para o sistema
    
    Attributes:
        id (int): Identificador único do plano
        nome (str): Nome do plano
        limite_pesquisas (int): Limite de pesquisas por ano
        preco (float): Preço do plano
        descricao (str): Descrição do plano
    """
    __tablename__ = 'plans'
    
    id = Column(Integer, primary_key=True)
    nome = Column(String(50), nullable=False)
    limite_pesquisas = Column(Integer, nullable=False)
    limite_de_envios = Column(Integer, nullable=False)
    preco = Column(Float, nullable=False)
    descricao = Column(String(255))
    
    # Relacionamentos
    planos_contratados = relationship('PlanoContratado', backref='plan', lazy=True)
    purchase_interests = relationship('PlanPurchaseInterest', back_populates='plan', lazy=True)
    
    def __repr__(self):
        return f"<Plan(id={self.id}, nome='{self.nome}', limite_pesquisas={self.limite_pesquisas}, preco={self.preco}, descricao='{self.descricao}')>"
    
    
    def to_dict(self):
        """
        Converte o objeto Plan em um dicionário
        
        Returns:
            dict: Dicionário com os dados do plano
        """
        return {
            'id': self.id,
            'nome': self.nome,
            'limite_pesquisas': self.limite_pesquisas,
            'limite_de_envios': self.limite_de_envios,
            'preco': self.preco,
            'descricao': self.descricao
        }
        
    
    @classmethod
    def validate_and_create(cls, data):
        if not data.get('nome') or not data.get('limite_pesquisas') or not data.get('limite_de_envios') or not data.get('preco') :
            raise ValueError("Todos os campos são obrigatórios")
        
        return cls(**data)
        

    def update(self, data):
        try: 
            for key, value in data.items():
                setattr(self, key, value)
            return self
        except Exception as e:
            raise e
