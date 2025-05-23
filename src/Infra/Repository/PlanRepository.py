from src.Infra.Config import sql_connection
from src.Infra.Entities.PlanEntity import PlanEntity, PlanEntitySchema
from src.Enums.PlanEnum import PlanEnum
from typing import List, Dict, Any, Optional


class PlanRepository:
    
    
    @staticmethod
    def init_plans():
        """Inicializa os planos base no banco de dados"""
        for plan_enum in PlanEnum:
            plan_data = plan_enum.value
            if not PlanEntity.query.filter_by(nome=plan_data['nome']).first():
                plan = PlanEntity(**plan_data)
                sql_connection.get_session().add(plan)
                print(f"Plano {plan_data['nome']} criado com sucesso!")
        
        sql_connection.get_session().commit()
        print("Todos os planos base foram inicializados!")
        
        
    def get_all_plans() -> List[PlanEntity]:
        """Obtém todos os planos do banco de dados"""
        try:
            with sql_connection.get_session() as session:
                return session.query(PlanEntity).all()
        except Exception as e:
            raise e
        
        
    def get_plan_by_id(self, plan_id: int) -> PlanEntity:
        """Obtém um plano pelo ID"""
        try:
            with sql_connection.get_session() as session:
                return session.query(PlanEntity).filter_by(id=plan_id).first()
        except Exception as e:
            raise e
        
    
    def get_plan_by_name(self, nome: str) -> PlanEntity:
        """
        Busca um plano pelo nome
        
        Args:   
            nome (str): Nome do plano
            
        Returns:
            Plan: Plano encontrado ou None se não encontrado
        """
        try:
            with sql_connection.get_session() as session:
                return session.query(PlanEntity).filter_by(nome=nome).first()
        except Exception as e:
            raise e
    
    
    def update_by_id(self, plan_id: int, plan_info: dict) -> PlanEntity:
        """
        Atualiza um plano pelo ID
        
        
        """
        try:
            plan = self.get_plan_by_id(plan_id)
            if not plan:
                raise PlanNotFoundException("Plano não encontrado")
            
            
            updated_plan = PlanEntity.update(plan_info)
            updated_plan.id = plan_id
            
            with sql_connection.get_session() as session:
                session.query(PlanEntity).filter_by(id=plan_id).update(updated_plan.to_dict())
        
            return updated_plan
        
        except PlanNotFoundException as e:
            print(e)
            raise PlanNotFoundException
        
        except Exception as e:
            print(e)
            raise e
