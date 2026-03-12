from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import ChatMessage


class ChatMessagesRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_message(self, user_id: int, role: str, content: str):
        msg = ChatMessage(
            user_id=user_id,
            role=role,
            content=content,
        )

        self.session.add(msg)
        await self.session.commit()

    async def get_last_messages(self, user_id: int, limit: int):
        stmt = (
            select(ChatMessage)
            .where(ChatMessage.user_id == user_id)
            .order_by(ChatMessage.created_at.desc())
            .limit(limit)
        )

        result = await self.session.execute(stmt)

        messages = result.scalars().all()

        return list(reversed(messages))

    async def delete_history(self, user_id: int):
        stmt = delete(ChatMessage).where(ChatMessage.user_id == user_id)
        await self.session.execute(stmt)
        await self.session.commit()
