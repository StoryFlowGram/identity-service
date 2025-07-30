from app.interfaces.protocols.user_protocol import UserProtocol



class DeleteProfileUseCase:
    
    def __init__(self, protocol: UserProtocol):
        self.protocol = protocol


    async def __call__(self, user_id: int):
        await self.protocol.delete(user_id)