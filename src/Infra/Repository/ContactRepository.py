from src.Infra.Config import sql_connection
from src.Infra.Entities.ContactEntity import ContactEntity
from typing import List, Dict, Any


class ContactRepository:
    
    def create_multiple_contatos(self, contatos: List[Dict[str, Any]], user_id: int) -> List[ContactEntity]:
        try:
            try:
                contatos_validos_obj = [ContactEntity.validate_and_create(contato, user_id) for contato in contatos]
            except ValueError as e:
                pass 
            
            with sql_connection.get_session() as session:
                session.bulk_save_objects(contatos_validos_obj)
                return contatos_validos_obj
        
        except Exception as e:
            raise e
                
                
    def get_all_contatos(self, user_id: int) -> List[ContactEntity]:
        try:
            with sql_connection.get_session() as session:
                return session.query(ContactEntity).filter_by(user_id=user_id).all()
        except Exception as e:
            raise e
    
    
    
    def get_contato_by_id(self, contato_id: int) -> ContactEntity:
        try:
            with sql_connection.get_session() as session:
                return session.query(ContactEntity).filter_by(id=contato_id).first()
        except Exception as e:
            raise e
        
    
    def update_contato(self, contato_id: int, contato: Dict[str, Any]) -> ContactEntity:
        try:
            contato_existente = self.get_contato_by_id(contato_id)
            if not contato_existente:
                raise ValueError("Contato não encontrado")
            
            updated_contato = ContactEntity.update(contato)
            
            with sql_connection.get_session() as session:
                session.query(ContactEntity).filter_by(id=contato_id).update(updated_contato)
                return updated_contato
        except Exception as e:
            raise e
    
    
            
