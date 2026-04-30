from datetime import datetime
import re

def strftime_safe(date: datetime, format: str) -> str:
    # Workaround for the bug https://bugs.python.org/issue8304
    pattern = re.compile(r"%[%a-zA-Z]")
    return pattern.sub(lambda match: date.strftime(match.group(0)), format)
