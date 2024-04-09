from typing import List
from fastapi import Depends, APIRouter, status

from .. import crud, schemas
from ..models import TimeSlot, User
from sqlalchemy.ext.asyncio import AsyncSession
from ..dependency import get_current_user, get_session
from ..schemas import TimeSlotCreate


router = APIRouter(dependencies=[Depends(get_current_user)])


@router.get(
    "/users/me",
    response_model=schemas.User,
)
async def read_me(
    current_user: User = Depends(get_current_user)
) -> User:
    return current_user


@router.post(
    "/time_slots/",
    response_model=List[schemas.TimeSlot],
    status_code=status.HTTP_201_CREATED,
)
async def create_time_slots(
    time_slots_data: List[TimeSlotCreate],
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
) -> List[TimeSlot]:
    return await crud.create_timeslot(time_slots_data, current_user, db)


@router.get(
    "/time_slots/me",
    response_model=List[schemas.TimeSlot],
)
async def get_my_time_slots(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session)
) -> list[TimeSlot]:
    return await crud.get_timeslot(current_user.id, db)
