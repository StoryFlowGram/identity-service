from app.domain.protocols.user_protocol import AbstractUserProtocol



class ProfileUseCase:
    def __init__(self, protocol: AbstractUserProtocol):
        self.protocol = protocol


    async def __call__(self, user_id: int):
        return await self.protocol.get_by_id(user_id)
        