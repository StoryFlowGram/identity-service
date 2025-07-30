from app.interfaces.protocols.user_protocol import UserProtocol



class ProfileUseCase:
    def __init__(self, protocol: UserProtocol):
        self.protocol = protocol


    async def __call__(self, user_id: int):
        return await self.protocol.get_by_id(user_id)
        