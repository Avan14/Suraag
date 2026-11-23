"""The only place times are formatted or parsed (chat, CSV, EXIF; always IST)."""
import re
from datetime import datetime

from suraag.model import IST


def _ist(t: datetime) -> datetime:
    return t.astimezone(IST)


def chat_time(t: datetime) -> str:
    t = _ist(t)
    return f"{t.hour % 12 or 12}:{t.minute:02d} {'am' if t.hour < 12 else 'pm'}"


def chat_ts(t: datetime) -> str:
    t = _ist(t)
    return f"{t:%d/%m/%y}, {chat_time(t)}"


def csv_ts(t: datetime) -> str:
    """ISO 8601 local time with an explicit offset (rule F-07): the offset removes the time-zone trap."""
    return f"{_ist(t):%Y-%m-%dT%H:%M:%S}+05:30"


def csv_hm(t: datetime) -> str:
    return f"{_ist(t):%H:%M}"


def exif_ts(t: datetime) -> str:
    return f"{_ist(t):%Y:%m:%d %H:%M:%S}"


_CHAT = re.compile(r"^(\d{2})/(\d{2})/(\d{2}),\s*(\d{1,2}):(\d{2})\s*(am|pm)$", re.I)


def parse_chat_ts(s: str) -> datetime:
    # Real WhatsApp exports put U+202F (narrow no-break space) before am/pm.
    m = _CHAT.match(s.replace(" ", " ").replace(" ", " ").strip())
    if not m:
        raise ValueError(f"not a chat timestamp: {s!r}")
    dd, mo, yy, hh, mi, ap = m.groups()
    hour = int(hh) % 12 + (12 if ap.lower() == "pm" else 0)
    return datetime(2000 + int(yy), int(mo), int(dd), hour, int(mi), tzinfo=IST)


def parse_csv_ts(s: str) -> datetime:
    """Reads the ISO form; an older bare "YYYY-MM-DD HH:MM:SS" is read as IST."""
    t = datetime.fromisoformat(s.strip())
    return t if t.tzinfo else t.replace(tzinfo=IST)


def parse_exif_ts(s: str) -> datetime:
    return datetime.strptime(s.strip(), "%Y:%m:%d %H:%M:%S").replace(tzinfo=IST)
