from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import AsyncSessionLocal
from app.repositories.users import UsersRepository
from app.repositories.chat_messages import ChatMessagesRepository
from app.usecases.auth import AuthUseCase
from app.usecases.chat import ChatUseCase
from app.services.openrouter_client import OpenRouterClient
from app.core.security import decode_token


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_db():

    async with AsyncSessionLocal() as session:
        yield session


def get_auth_usecase(db: AsyncSession = Depends(get_db)):

    repo = UsersRepository(db)
    return AuthUseCase(repo)


def get_chat_usecase(db: AsyncSession = Depends(get_db)):

    repo = ChatMessagesRepository(db)
    llm = OpenRouterClient()

    return ChatUseCase(repo, llm)


async def get_current_user_id(token: str = Depends(oauth2_scheme)):

    try:
        payload = decode_token(token)
        return int(payload["sub"])
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")
