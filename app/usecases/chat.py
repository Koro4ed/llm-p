from app.repositories.chat_messages import ChatMessagesRepository
from app.services.openrouter_client import OpenRouterClient


class ChatUseCase:
    def __init__(self, repo: ChatMessagesRepository, llm: OpenRouterClient):
        self.repo = repo
        self.llm = llm

    async def ask(
        self,
        user_id: int,
        prompt: str,
        system: str | None,
        max_history: int,
        temperature: float,
    ):

        messages = []

        if system:
            messages.append({"role": "system", "content": system})

        history = await self.repo.get_last_messages(user_id, max_history)

        for msg in history:
            messages.append(
                {
                    "role": msg.role,
                    "content": msg.content,
                }
            )

        messages.append(
            {
                "role": "user",
                "content": prompt,
            }
        )

        await self.repo.add_message(user_id, "user", prompt)

        answer = await self.llm.chat(messages, temperature)

        await self.repo.add_message(user_id, "assistant", answer)

        return answer

    async def history(self, user_id: int):

        history = await self.repo.get_last_messages(user_id, 100)

        return history

    async def clear(self, user_id: int):

        await self.repo.delete_history(user_id)
