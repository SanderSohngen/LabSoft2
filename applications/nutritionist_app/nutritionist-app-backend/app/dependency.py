from fastapi import Depends

from .models import User
from sqlalchemy.future import select
from .database import AsyncSessionLocal
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordBearer
from .security import decode_token, CREDENTIALS_EXCEPTION

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_session():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_session)
) -> User:
    token_data = decode_token(token)
    user = await db.execute(
        select(User).filter(User.email == token_data.email)
    )

    user = user.scalar()
    if user is None:
        raise CREDENTIALS_EXCEPTION
    return user
