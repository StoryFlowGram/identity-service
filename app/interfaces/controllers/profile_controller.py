from fastapi import APIRouter, Depends, HTTPException, status

from app.usecase.delete_profile import DeleteProfileUseCase
from app.infrastructure.security.depends import get_user_protocol
from app.interfaces.protocols.user_protocol import UserProtocol
from app.interfaces.dto.profile import ProfileResponseDTO
from app.interfaces.dto.update_profile import UpdateProfileDTO
from app.infrastructure.security.depends import get_current_user

from app.usecase.profile import ProfileUseCase
from app.usecase.update_profile_telegram import UpdateProfileUseCase

profile_router = APIRouter(prefix="/api/v1/user", tags=["User"])


@profile_router.get("/me",response_model=ProfileResponseDTO)
async def read_profile(user_id: int = Depends(get_current_user), protocol: UserProtocol = Depends(get_user_protocol)):
    user = await protocol.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")
    return user

@profile_router.put("/profile", response_model=dict)
async def update_profile(dto:UpdateProfileDTO, user_id: int = Depends(get_current_user), protocol: UserProtocol = Depends(get_user_protocol)):
    usecase = UpdateProfileUseCase(protocol)
    update_user = await usecase(user_id, dto)
    return {"message": "Профиль обновлен", "user": update_user}

@profile_router.delete("/profile", response_model=dict)
async def delete_profile(user_id: int = Depends(get_current_user), protocol: UserProtocol = Depends(get_user_protocol)):
    usecase = DeleteProfileUseCase(protocol)
    await usecase(user_id)
    return {"message": "Профиль удален"}

