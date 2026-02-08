from app.domain.entities.User import User as DomainUser
from app.infrastructure.models.user_models import User as UserModel


def orm_to_domain(orm: UserModel) -> DomainUser:
    return DomainUser(
        id=orm.id,                
        telegram_id=orm.telegram_id,
        google_id=orm.google_id,
        email=orm.email,
        first_name=orm.first_name,
        last_name=orm.last_name,
        username=orm.username,
        avatar_url=orm.avatar_url
    )

def domain_to_orm(domain: DomainUser) -> UserModel:
    return UserModel(
        telegram_id=domain.telegram_id,
        google_id=domain.google_id,
        email=domain.email,
        first_name=domain.first_name,
        last_name=domain.last_name,
        username=domain.username,
        avatar_url=domain.avatar_url
    )