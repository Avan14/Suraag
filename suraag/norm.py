"""Text normalisation used by every comparison (NFC, zero-width, nukta, casefold)."""
import re
import unicodedata

_ZERO_WIDTH = dict.fromkeys(map(ord, "​‌‍⁠﻿"))
_NUKTA = {0x093C: None}
_SPACES = re.compile(r"\s+")


def norm(s: str) -> str:
    s = unicodedata.normalize("NFC", s)
    s = s.translate(_ZERO_WIDTH)
    s = unicodedata.normalize("NFC", s.translate(_NUKTA))  # NFC splits precomposed क़ into क + nukta first
    s = s.replace(" ", " ").replace(" ", " ")
    return _SPACES.sub(" ", s).strip().casefold()
