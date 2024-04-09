from typing import Dict, List
from datetime import datetime, timedelta

from sqlalchemy import Result

from .models import TimeSlot


def generate_time_slots(
    time_slots: List[TimeSlot],
    weeks: int = 4
) -> List[datetime]:
    current_time = datetime.now()
    return [
        datetime.combine(
            current_time.date() + timedelta(
                days=(
                    (slot.day_of_week - current_time.weekday() + 7) % 7
                    + week * 7
                )
            ),
            slot.time
        )
        for week in range(weeks)
        for slot in time_slots
    ]


def build_user_data(
    result: Result
) -> List[Dict[str, int | str | List[int]]]:
    user_data = {}
    for user_id, name, email, day_of_week in result.fetchall():
        if user_id not in user_data:
            user_data[user_id] = {
                "id": user_id,
                "name": name,
                "email": email,
                "days_available": set()
            }
        user_data[user_id]["days_available"].add(day_of_week)
    return user_data.values()
