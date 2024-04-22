from typing import List
from sqlalchemy import delete
from fastapi import HTTPException, status

from .models import User, TimeSlot
from .security import hash_password
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from .schemas import UserCreate, TimeSlotCreate, UserAvailability
from .utils import build_user_data


async def create_user(
    user_data: UserCreate,
    db: AsyncSession,
) -> User:
    async with db as session:
        result = await session.execute(
            select(User).filter(
                (User.email == user_data.email) | (User.name == user_data.name)
            )
        )
        existing_user = result.scalars().first()
        if existing_user:
            if existing_user.email == user_data.email:
                detail = "Email já registrado."
            else:
                detail = "Nome já registrado."
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=detail
            )

        hashed_password = hash_password(user_data.password)
        new_user = User(
            **user_data.model_dump(exclude={'password'}),
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
                detail="Usuário não encontrado."
            )
        return user


async def get_users(
    db: AsyncSession
) -> List[User]:
    async with db as session:
        result = await session.execute(select(User))
        users = result.scalars().all()
        return users


async def create_timeslot(
    time_slots_data: List[TimeSlotCreate],
    user: User,
    db: AsyncSession
) -> List[TimeSlot]:
    async with db as session:
        await session.execute(
            delete(TimeSlot).where(TimeSlot.user_id == user.id)
        )
        await session.commit()

        new_time_slots = [
            TimeSlot(
                **time_slot.model_dump()
            )
            for time_slot in time_slots_data
        ]
        session.add_all(new_time_slots)
        await session.flush()
        await session.commit()
        for time_slot in new_time_slots:
            await session.refresh(time_slot)
        return new_time_slots


async def get_timeslot(
    user_id: int,
    db: AsyncSession
) -> List[TimeSlot]:
    async with db as session:
        result = await session.execute(
            select(TimeSlot).filter(TimeSlot.user_id == user_id)
        )
        time_slots = result.scalars().all()
        return time_slots


async def get_users_with_availability(
    db: AsyncSession
) -> List[UserAvailability]:
    async with db as session:
        result = await session.execute(
            select(
                User.id,
                User.name,
                User.email,
                TimeSlot.day_of_week
            ).join(
                TimeSlot, TimeSlot.user_id == User.id
            ).order_by(User.id)
        )
        user_data = build_user_data(result)

        return [
            UserAvailability(**user)
            for user in user_data
        ]
