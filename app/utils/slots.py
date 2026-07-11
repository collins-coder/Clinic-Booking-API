from datetime import datetime, timedelta, time


def generate_slots(work_start: time, work_end: time, appointment_date):
    """
    Generate 30-minute appointment slots.
    """

    slots = []

    current = datetime.combine(appointment_date, work_start)
    end = datetime.combine(appointment_date, work_end)

    while current < end:
        slots.append(current)
        current += timedelta(minutes=30)

    return slots