from app.interfaces.protocols.user_protocol import UserProtocol
from app.interfaces.dto.update_profile import UpdateProfileDTO


class UpdateProfileUseCase:
    def __init__(self, protocol: UserProtocol):
        self.protocol = protocol


    async def __call__(self, user_id: int, dto: UpdateProfileDTO):
        check_user = await self.protocol.get_by_id(user_id)
        if check_user is None:
            raise ValueError("Пользователь не найден")
        
        data = dto.model_dump(exclude_none=True)
        
        return await self.protocol.update_profile(user_id=user_id, **data)
        

        