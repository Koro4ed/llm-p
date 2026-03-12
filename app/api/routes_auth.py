from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.schemas.auth import RegisterRequest, TokenResponse
from app.schemas.user import UserPublic
from app.api.deps import get_auth_usecase, get_current_user_id
from app.usecases.auth import AuthUseCase
from app.core.errors import ConflictError, UnauthorizedError


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserPublic)
async def register(data: RegisterRequest, uc: AuthUseCase = Depends(get_auth_usecase)):

    try:
        user = await uc.register(data.email, data.password)
        return user

    except ConflictError:
        raise HTTPException(status_code=409, detail="Email exists")


@router.post("/login", response_model=TokenResponse)
async def login(
    form: OAuth2PasswordRequestForm = Depends(),
    uc: AuthUseCase = Depends(get_auth_usecase),
):

    try:
        token = await uc.login(form.username, form.password)

        return {
            "access_token": token,
            "token_type": "bearer",
        }

    except UnauthorizedError:
        raise HTTPException(status_code=401, detail="Invalid credentials")


@router.get("/me", response_model=UserPublic)
async def me(
    user_id: int = Depends(get_current_user_id),
    uc: AuthUseCase = Depends(get_auth_usecase),
):

    return await uc.get_profile(user_id)
