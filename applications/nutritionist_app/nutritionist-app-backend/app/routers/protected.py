from fastapi import Depends, APIRouter

from ..dependency import (
    get_current_user,
)

router = APIRouter(dependencies=[Depends(get_current_user)])
