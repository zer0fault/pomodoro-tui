"""
Helper utility functions for the Pomodoro TUI application.
"""
from typing import Tuple


def format_time(seconds: int) -> str:
    """
    Format seconds into MM:SS string format.

    Args:
        seconds: Total seconds to format

    Returns:
        Formatted time string (MM:SS)
    """
    minutes = seconds // 60
    secs = seconds % 60
    return f"{minutes:02d}:{secs:02d}"


def parse_time(time_str: str) -> int:
    """
    Parse MM:SS time string into total seconds.

    Args:
        time_str: Time string in MM:SS format

    Returns:
        Total seconds
    """
    try:
        parts = time_str.split(":")
        if len(parts) != 2:
            raise ValueError("Invalid time format")
        minutes = int(parts[0])
        seconds = int(parts[1])
        return minutes * 60 + seconds
    except (ValueError, IndexError):
        return 0


def minutes_to_seconds(minutes: int) -> int:
    """
    Convert minutes to seconds.

    Args:
        minutes: Number of minutes

    Returns:
        Total seconds
    """
    return minutes * 60


def seconds_to_minutes(seconds: int) -> int:
    """
    Convert seconds to minutes (rounded down).

    Args:
        seconds: Number of seconds

    Returns:
        Number of minutes
    """
    return seconds // 60


def calculate_progress(elapsed: int, total: int) -> float:
    """
    Calculate progress percentage.

    Args:
        elapsed: Elapsed time in seconds
        total: Total time in seconds

    Returns:
        Progress as a float between 0.0 and 1.0
    """
    if total <= 0:
        return 0.0
    progress = elapsed / total
    return min(1.0, max(0.0, progress))


def validate_duration(duration: int, min_val: int, max_val: int) -> bool:
    """
    Validate that a duration is within acceptable range.

    Args:
        duration: Duration to validate (in minutes)
        min_val: Minimum acceptable value
        max_val: Maximum acceptable value

    Returns:
        True if valid, False otherwise
    """
    return min_val <= duration <= max_val
