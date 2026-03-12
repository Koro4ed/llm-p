from fastapi import APIRouter, Depends

from app.schemas.chat import ChatRequest, ChatResponse
from app.api.deps import get_chat_usecase, get_current_user_id
from app.usecases.chat import ChatUseCase


router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("", response_model=ChatResponse)
async def chat(
    data: ChatRequest,
    user_id: int = Depends(get_current_user_id),
    uc: ChatUseCase = Depends(get_chat_usecase),
):

    answer = await uc.ask(
        user_id,
        data.prompt,
        data.system,
        data.max_history,
        data.temperature,
    )

    return {"answer": answer}


@router.get("/history")
async def history(
    user_id: int = Depends(get_current_user_id),
    uc: ChatUseCase = Depends(get_chat_usecase),
):

    return await uc.history(user_id)


@router.delete("/history")
async def clear_history(
    user_id: int = Depends(get_current_user_id),
    uc: ChatUseCase = Depends(get_chat_usecase),
):

    await uc.clear(user_id)

    return {"status": "deleted"}
