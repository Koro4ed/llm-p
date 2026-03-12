from app.repositories.users import UsersRepository
from app.core.security import hash_password, verify_password, create_access_token
from app.core.errors import ConflictError, UnauthorizedError, NotFoundError


class AuthUseCase:
    def __init__(self, users_repo: UsersRepository):
        self.users_repo = users_repo

    async def register(self, email: str, password: str):

        existing = await self.users_repo.get_by_email(email)

        if existing:
            raise ConflictError("Email already exists")

        password_hash = hash_password(password)

        user = await self.users_repo.create(email, password_hash)

        return user

    async def login(self, email: str, password: str):

        user = await self.users_repo.get_by_email(email)

        if not user:
            raise UnauthorizedError()

        if not verify_password(password, user.password_hash):
            raise UnauthorizedError()

        token = create_access_token(user.id, user.role)

        return token

    async def get_profile(self, user_id: int):

        user = await self.users_repo.get_by_id(user_id)

        if not user:
            raise NotFoundError()

        return user
