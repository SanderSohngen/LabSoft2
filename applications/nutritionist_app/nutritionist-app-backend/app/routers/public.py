from typing import List
from datetime import timedelta, datetime
from fastapi import Depends, APIRouter, status, HTTPException

from ..dependency import get_session
from ..utils import generate_time_slots
from .. import crud, schemas, models, security
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()


@router.post(
    "/token",
    response_model=schemas.Token
)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_session)
) -> schemas.Token:
    user = await security.authenticate_user(
        db,
        form_data.username,
        form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="e-mail ou senha incorreta",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(
        minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    access_token = security.create_access_token(
        data={"sub": user.email},
        expires_delta=access_token_expires
    )
    return schemas.Token(access_token=access_token, token_type="bearer")


@router.post(
    "/users/",
    response_model=schemas.User,
    status_code=status.HTTP_201_CREATED
)
async def create_user(
    user: schemas.UserCreate,
    db: AsyncSession = Depends(get_session)
) -> models.User:
    return await crud.create_user(user, db)


@router.get(
    "/users/{user_id}",
    response_model=schemas.User
)
async def read_user(
    user_id: int,
    db: AsyncSession = Depends(get_session)
) -> models.User:
    return await crud.get_user(user_id, db)


@router.get(
    "/users/",
    response_model=list[schemas.User]
)
async def read_users(
    db: AsyncSession = Depends(get_session)
) -> list[models.User]:
    return await crud.get_users(db)


@router.get(
    "/time_slots/{user_id}",
    response_model=List[datetime]
)
async def get_time_slots(
    user_id: int,
    db: AsyncSession = Depends(get_session)
) -> List[datetime]:
    time_slots = await crud.get_timeslot(user_id, db)
    return generate_time_slots(time_slots)


@router.get(
    "/users/time_slots/",
    response_model=List[schemas.UserAvailability]
)
async def get_users_with_availability(
    db: AsyncSession = Depends(get_session)
) -> List[schemas.UserAvailability]:
    return await crud.get_users_with_availability(db)
