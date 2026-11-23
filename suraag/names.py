"""Seeded name draws from data/names.json. Guilt is never linked to region or community:
each person's region is drawn independently, and roles are shuffled elsewhere."""
import json
import random
import unicodedata
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

_DATA = Path(__file__).parent / "data" / "names.json"


@dataclass(frozen=True)
class DrawnName:
    first: str
    surname: str
    first_deva: str
    surname_deva: str
    gender: str  # "m" or "f": only used to pick a natural form of address

    @property
    def full(self) -> str:
        return f"{self.first} {self.surname}"

    @property
    def full_deva(self) -> str:
        return f"{self.first_deva} {self.surname_deva}"


@lru_cache(maxsize=1)
def load_names() -> dict:
    data = json.loads(_DATA.read_text("utf-8"))
    nfc = lambda s: unicodedata.normalize("NFC", s)  # noqa: E731
    for region in data["regions"].values():
        for key in ("first", "surname"):
            region[key] = [[nfc(x[0]), nfc(x[1]), *x[2:]] for x in region[key]]
    data["blocklist"] = {nfc(b).casefold() for b in data["blocklist"]}
    return data


def draw_people(rng: random.Random, n: int = 4) -> list[DrawnName]:
    """n names with distinct first names, distinct first-initial/surname-initial pairs, distinct
    surname initials, none on the blocklist. Raises if the pools can't satisfy that."""
    data = load_names()
    regions = sorted(data["regions"])
    for _ in range(500):
        picks = []
        for _ in range(n):
            r = data["regions"][rng.choice(regions)]
            (f, fd, g), (s, sd) = rng.choice(r["first"]), rng.choice(r["surname"])
            picks.append(DrawnName(f, s, fd, sd, g))
        if (len({p.first for p in picks}) == n
                and len({p.surname[0] for p in picks}) == n
                and len({(p.first[0], p.surname[0]) for p in picks}) == n
                and not any(p.full.casefold() in data["blocklist"] for p in picks)):
            return picks
    raise RuntimeError("could not draw distinct names")
