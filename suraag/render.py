"""World model + filler -> chat.txt, calls.csv, photo.jpg. Pure functions: same input, same bytes."""
import csv
import io
import random
from datetime import datetime
from pathlib import Path

import piexif
from PIL import Image, ImageDraw

from suraag.lang import get_pack
from suraag.model import Case, ChatMessage
from suraag.parse import CALLS_FILE, CHAT_FILE, HEADER, PHOTO_FILE, Artifacts
from suraag.timefmt import chat_ts, csv_ts, exif_ts


class FillerShortError(ValueError):
    def __init__(self, needed: int, got: int):
        super().__init__(f"filler has {got} messages, {needed} needed")
        self.needed, self.got = needed, got


def _one_line(s: str) -> str:
    for ch in ("\r\n", "\n", "\r", " ", " "):
        s = s.replace(ch, " ")
    return s


def filler_gaps(case: Case) -> list[tuple[datetime, datetime, list[int]]]:
    """The runs of non-anchor chat lines: (earliest time, latest time, line numbers)."""
    bounds = ([(1, case.chat_window[0])]
              + [(a.line, a.message.t) for a in sorted(case.chat_anchors, key=lambda a: a.line)]
              + [(case.chat_length + 1, case.chat_window[1])])
    gaps = []
    for (l0, t0), (l1, t1) in zip(bounds, bounds[1:]):
        lines = list(range(l0 + 1, l1))
        if lines:
            gaps.append((t0, t1, lines))
    return gaps


def stub_filler(case: Case) -> list[ChatMessage]:
    """Offline, deterministic filler: times spread evenly inside each gap, never a trigger phrase."""
    rng = random.Random(case.seed)
    pack = get_pack(case.lang)
    senders = [case.person(p).saved_as for p in case.chat_members]
    out = []
    for t0, t1, lines in filler_gaps(case):
        m = len(lines)
        for k in range(m):
            t = (t0 + (t1 - t0) * (k + 1) / (m + 1)).replace(second=0, microsecond=0)
            out.append(ChatMessage(t=t, sender=rng.choice(senders), text=rng.choice(pack.stub_lines)))
    return out


def render_chat(case: Case, filler: list[ChatMessage]) -> str:
    """Anchors go at their exact lines; filler fills the rest in order, unchanged (no time fixing)."""
    needed = case.filler_needed()
    if len(filler) < needed:
        raise FillerShortError(needed, len(filler))
    anchors = {a.line: a.message for a in case.chat_anchors}
    it = iter(filler)
    lines = [HEADER]
    for n in range(2, case.chat_length + 1):
        m = anchors[n] if n in anchors else next(it)
        lines.append(f"{chat_ts(m.t)} - {_one_line(m.sender)}: {_one_line(m.text)}")
    return "\n".join(lines) + "\n"


def render_calls(case: Case) -> str:
    buf = io.StringIO()
    # CRLF line ends and quoted text fields (rule F-06) so Excel and strict parsers agree.
    buf.write(f"# {HEADER}\r\n")
    w = csv.writer(buf, lineterminator="\r\n", quoting=csv.QUOTE_NONNUMERIC)
    w.writerow(["row", "datetime", "direction", "number", "contact_name", "duration_s"])
    for r in sorted(case.calls, key=lambda r: r.row):
        w.writerow([r.row, csv_ts(r.t), r.direction, r.number, r.contact_name, r.duration_s])
    return buf.getvalue()


def _dms(x: float):
    x = abs(x)
    deg = int(x)
    mins = int((x - deg) * 60)
    sec = ((x - deg) * 60 - mins) * 60
    return ((deg, 1), (mins, 1), (int(round(sec * 10000)), 10000))


def render_photo(case: Case) -> bytes:
    if case.photo is None:
        raise ValueError("this case has no photo")
    p = case.photo
    ts, off = exif_ts(p.t, p.offset).encode("ascii"), p.offset.encode("ascii")
    rng = random.Random(case.seed)
    image = Image.new("RGB", (640, 480), (rng.randint(60, 200), rng.randint(60, 200), rng.randint(60, 200)))
    ImageDraw.Draw(image).text((24, 24), "SYNTHETIC", fill=(255, 255, 255))
    exif = piexif.dump({
        "0th": {piexif.ImageIFD.ImageDescription: HEADER.encode("ascii"),
                piexif.ImageIFD.Make: p.make.encode("ascii"), piexif.ImageIFD.Model: p.model.encode("ascii"),
                piexif.ImageIFD.DateTime: ts},  # ModifyDate equals capture time: a clean original
        "Exif": {piexif.ExifIFD.DateTimeOriginal: ts,
                 piexif.ExifIFD.DateTimeDigitized: ts,  # CreateDate
                 piexif.ExifIFD.OffsetTime: off, piexif.ExifIFD.OffsetTimeOriginal: off,
                 piexif.ExifIFD.OffsetTimeDigitized: off},
        "GPS": {piexif.GPSIFD.GPSLatitudeRef: b"N" if p.lat >= 0 else b"S",
                piexif.GPSIFD.GPSLatitude: _dms(p.lat),
                piexif.GPSIFD.GPSLongitudeRef: b"E" if p.lon >= 0 else b"W",
                piexif.GPSIFD.GPSLongitude: _dms(p.lon)},
    })
    buf = io.BytesIO()
    image.save(buf, "JPEG", quality=85, exif=exif)
    return buf.getvalue()


def write_artifacts(arts: Artifacts, out_dir) -> None:
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    (out / CHAT_FILE).write_bytes(arts.chat_bytes())
    (out / CALLS_FILE).write_bytes(arts.calls_bytes())
    if arts.photo is not None:
        (out / PHOTO_FILE).write_bytes(arts.photo)
