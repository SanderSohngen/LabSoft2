from typing import List
from datetime import datetime, timedelta

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
