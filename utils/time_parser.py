import re
from datetime import timedelta

TIME_REGEX = re.compile(r"^(\d+)([smhd])$", re.IGNORECASE)


def parse_duration(duration: str) -> timedelta:
    duration = duration.strip().lower()

    match = TIME_REGEX.match(duration)

    if not match:
        raise ValueError(
            "Invalid duration. Use: 30s, 5m, 2h or 7d."
        )

    amount = int(match.group(1))
    unit = match.group(2)

    if unit == "s":
        return timedelta(seconds=amount)

    if unit == "m":
        return timedelta(minutes=amount)

    if unit == "h":
        return timedelta(hours=amount)

    if unit == "d":
        return timedelta(days=amount)

    raise ValueError("Unknown duration.")
