from fastapi import HTTPException, status

from .models import User
from .schemas import UserCreate
from .security import hash_password
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession


async def create_user(
    user_data: UserCreate,
    db: AsyncSession,
) -> User:
    async with db as session:
        result = await session.execute(
            select(User).filter(User.email == user_data.email)
        )
        existing_user = result.scalars().first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_BAD_REQUEST,
                detail="Email already registered."
            )

        hashed_password = hash_password(user_data.password)
        new_user = User(
            **user_data.model_dump(),
            hashed_password=hashed_password
        )
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return new_user


async def get_user(
    user_id: int,
    db: AsyncSession
) -> User:
    async with db as session:
        result = await session.execute(
            select(User).filter(User.id == user_id)
        )
        user = result.scalars().first()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return user


async def get_users(
    db: AsyncSession
) -> list[User]:
    async with db as session:
        result = await session.execute(select(User))
        users = result.scalars().all()
        return users
