from src.Infra.Entities.PlanSubscriptionEntity import PlanSubscriptionEntity
from src.Enums.PlanEnum import PlanEnum
from src.Enums.PlanEnum import PlanStatusEnum
from typing import Optional
from src.Infra.Config import sql_connection
from src.Infra.Entities.PlanEntity import PlanEntity


        
class PlanSubscriptionRepository:

        
    def check_if_user_has_free_plan(self, user_id: int) -> Optional['PlanSubscriptionEntity']:
        try:
            with sql_connection.get_session() as session:
                return session.query(PlanSubscriptionEntity)\
                    .join(PlanEntity, PlanEntity.id == PlanSubscriptionEntity.plan_id)\
                    .filter(PlanSubscriptionEntity.user_id == user_id, 
                            PlanEntity.nome == PlanEnum.FREE.value, 
                            PlanSubscriptionEntity.status == PlanStatusEnum.ACTIVE.value).first()
        except Exception as e:
            raise e
