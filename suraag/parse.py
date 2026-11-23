"""Reads artifacts back (chat, calls, EXIF) for the solver, verifier and grader, so "what a
line says" is computed in exactly one place."""
import csv
import hashlib
import io
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from suraag.model import ArtifactName, CallRow
from suraag.timefmt import csv_ts, parse_chat_ts, parse_csv_ts

HEADER = "SYNTHETIC CASE - fictional, for teaching only. Not real data."
CHAT_FILE, CALLS_FILE, PHOTO_FILE = "chat.txt", "calls.csv", "photo.jpg"
# Rule H-08: what a hash does and does not show. One wording everywhere a hash is displayed.
HASH_NOTE = ("A matching hash shows this file has not changed since the hash was computed; it does not show who "
             "made the file or that its content is genuine.")
_BOM = b"\xef\xbb\xbf"


@dataclass(frozen=True)
class ChatLine:
    line: int                # 1-based, the header is line 1
    t: datetime | None
    sender: str | None
    text: str
    raw: str


@dataclass
class Artifacts:
    chat: str
    calls: str
    photo: bytes | None = None

    @classmethod
    def from_dir(cls, path) -> "Artifacts":
        p = Path(path)
        photo = (p / PHOTO_FILE).read_bytes() if (p / PHOTO_FILE).exists() else None
        return cls((p / CHAT_FILE).read_bytes().decode("utf-8"),
                   (p / CALLS_FILE).read_bytes().decode("utf-8-sig"), photo)

    def chat_bytes(self) -> bytes:
        return self.chat.encode("utf-8")

    def calls_bytes(self) -> bytes:
        return _BOM + self.calls.lstrip("﻿").encode("utf-8")

    def sha256(self) -> dict[str, str]:
        out = {CHAT_FILE: hashlib.sha256(self.chat_bytes()).hexdigest(),
               CALLS_FILE: hashlib.sha256(self.calls_bytes()).hexdigest()}
        if self.photo is not None:
            out[PHOTO_FILE] = hashlib.sha256(self.photo).hexdigest()
        return out


def load_chat(text: str) -> list[ChatLine]:
    out = []
    for i, raw in enumerate(text.split("\n")[: None], start=1):
        if i > 1 and raw == "" and i == len(text.split("\n")):
            break  # the trailing newline
        t = sender = None
        body = raw
        if i > 1:
            ts, sep, rest = raw.partition(" - ")
            name, sep2, msg = rest.partition(": ")
            if sep and sep2:
                try:
                    t, sender, body = parse_chat_ts(ts), name, msg
                except ValueError:
                    pass
        out.append(ChatLine(i, t, sender, body, raw))
    return out


def load_calls(text: str) -> list[CallRow]:
    rows = []
    for rec in csv.reader(io.StringIO(text.lstrip("﻿"))):
        if not rec or rec[0].startswith("#") or rec[0] == "row":
            continue
        rows.append(CallRow(row=int(rec[0]), t=parse_csv_ts(rec[1]), direction=rec[2],
                            number=rec[3], contact_name=rec[4], duration_s=int(rec[5])))
    return rows


def text_at(arts: Artifacts, artifact: ArtifactName, *, line: int | None = None,
            row: int | None = None, exif_tag: str | None = None) -> str | None:
    """The text a student would read at one location, or None if the location doesn't exist."""
    if artifact == "chat":
        lines = load_chat(arts.chat)
        return lines[line - 1].raw if line and 1 <= line <= len(lines) else None
    if artifact == "calls":
        for r in load_calls(arts.calls):
            if r.row == row:
                return f"{csv_ts(r.t)},{r.direction},{r.number},{r.contact_name},{r.duration_s}"
        return None
    if artifact == "photo" and arts.photo is not None and exif_tag:
        return load_exif(arts.photo).get(exif_tag)
    return None


def _dms(vals) -> float:
    d, m, s = (n / den for n, den in vals)
    return d + m / 60 + s / 3600


def load_exif(data: bytes) -> dict[str, str]:
    """EXIF fields as the strings a student would read. GPS comes back as signed decimal
    degrees to 4 places (GPSLatitude, GPSLongitude)."""
    import piexif
    try:
        exif = piexif.load(data)
    except Exception:
        return {}

    def txt(v) -> str:
        return v.decode("ascii", "replace") if isinstance(v, bytes) else str(v)

    out: dict[str, str] = {}
    for name, ifd, tag in (("ImageDescription", "0th", piexif.ImageIFD.ImageDescription),
                           ("Make", "0th", piexif.ImageIFD.Make), ("Model", "0th", piexif.ImageIFD.Model),
                           ("ModifyDate", "0th", piexif.ImageIFD.DateTime),
                           ("DateTimeOriginal", "Exif", piexif.ExifIFD.DateTimeOriginal),
                           ("CreateDate", "Exif", piexif.ExifIFD.DateTimeDigitized),
                           ("OffsetTime", "Exif", piexif.ExifIFD.OffsetTime),
                           ("OffsetTimeOriginal", "Exif", piexif.ExifIFD.OffsetTimeOriginal),
                           ("OffsetTimeDigitized", "Exif", piexif.ExifIFD.OffsetTimeDigitized)):
        if tag in exif[ifd]:
            out[name] = txt(exif[ifd][tag])
    gps = exif["GPS"]
    for name, val_tag, ref_tag, neg in (("GPSLatitude", piexif.GPSIFD.GPSLatitude, piexif.GPSIFD.GPSLatitudeRef, b"S"),
                                        ("GPSLongitude", piexif.GPSIFD.GPSLongitude, piexif.GPSIFD.GPSLongitudeRef, b"W")):
        if val_tag in gps and ref_tag in gps:
            out[name] = f"{_dms(gps[val_tag]) * (-1 if gps[ref_tag] == neg else 1):.4f}"
    return out
