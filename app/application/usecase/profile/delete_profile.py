from app.domain.protocols.user_protocol import AbstractUserProtocol



class DeleteProfileUseCase:
    
    def __init__(self, protocol: AbstractUserProtocol):
        self.protocol = protocol


    async def __call__(self, user_id: int):
        await self.protocol.delete(user_id)