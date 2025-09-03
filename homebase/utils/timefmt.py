from __future__ import annotations
from datetime import datetime, timedelta, timezone
from typing import Optional
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

# ---------- TZ helpers ----------

def get_tz(tz_name: str) -> ZoneInfo:
    """
    Return a ZoneInfo for tz_name or raise a clear, actionable error.
    On Windows, ensure 'tzdata' is installed in the environment.
    """
    try:
        return ZoneInfo(tz_name)
    except ZoneInfoNotFoundError as e:
        raise RuntimeError(
            f"Time zone '{tz_name}' not found. On Windows, install tzdata:\n"
            f"    pip install tzdata\n"
            f"Or set HOMEBASE_TZ=UTC in your .env as a temporary workaround."
        ) from e

def validate_timezone(tz_name: str) -> None:
    """Just try to acquire the TZ; surface a friendly error if it fails."""
    _ = get_tz(tz_name)

def ensure_aware(dt: datetime, assume_tz: str = "UTC") -> datetime:
    if dt.tzinfo is None:
        return dt.replace(tzinfo=get_tz(assume_tz) if assume_tz.upper() != "UTC" else timezone.utc)
    return dt

def to_zone(dt: datetime, tz_name: str) -> datetime:
    dt = ensure_aware(dt)
    return dt.astimezone(get_tz(tz_name))

def start_of_local_day(dt: datetime, tz_name: str) -> datetime:
    local = to_zone(dt, tz_name)
    return local.replace(hour=0, minute=0, second=0, microsecond=0)

# ---------- Formatting helpers ----------

def format_clock(dt: datetime, tz_name: str) -> str:
    local = to_zone(dt, tz_name)
    return local.strftime("%I:%M %p").lstrip("0")

def format_date_time(dt: datetime, tz_name: str) -> str:
    local = to_zone(dt, tz_name)
    return f"{local.strftime('%m/%d')} @ {local.strftime('%I:%M %p').lstrip('0')}"

# ---------- Relative due strings ----------

def relative_due(now: datetime, due: Optional[datetime], tz_name: str) -> str:
    if due is None:
        return "(no due date)"

    now = ensure_aware(now)
    due = ensure_aware(due)

    local_now = to_zone(now, tz_name)
    local_due = to_zone(due, tz_name)
    diff = local_due - local_now

    if diff.total_seconds() < 0:
        hrs = int(abs(diff.total_seconds()) // 3600)
        mins = int((abs(diff.total_seconds()) % 3600) // 60)
        when = format_date_time(due, tz_name)
        if hrs == 0:
            return f"overdue by {mins} min, {when}"
        if mins == 0:
            return f"overdue by {hrs} hr, {when}"
        return f"overdue by {hrs} hr {mins} min, {when}"

    if local_due.date() == local_now.date():
        return f"due today @ {format_clock(due, tz_name)}"

    if (start_of_local_day(local_due, tz_name).date()
        - start_of_local_day(local_now, tz_name).date()).days == 1:
        return f"due tomorrow, {format_date_time(due, tz_name)}"

    days = (start_of_local_day(local_due, tz_name)
            - start_of_local_day(local_now, tz_name)).days
    return f"due in {days} days, {format_date_time(due, tz_name)}"
