"""Language packs: get_pack(lang). Each pack holds what differs by language: trigger phrases,
alias patterns, places, stub lines, instruction templates and LLM prompts."""
import re
from dataclasses import dataclass


@dataclass(frozen=True)
class LangPack:
    lang: str
    triggers: dict[str, re.Pattern]       # applied to norm(text)
    alias_patterns: list[str]             # "{first} bhai": the name as saved in a phone
    places: list[tuple[str, float, float]]
    stub_lines: list[str]                 # offline filler; never matches a trigger
    instruction_templates: list[str]      # format with {owner}; always matches triggers["instruction"]
    question_texts: dict[str, str]        # who / when / where
    filler_prompt: str                    # str.format fields: see suraag/filler.py
    raw_prompt: str                       # str.format fields: see suraag/rawmode.py
    brief_summary: str                    # str.format fields: {amount}, {date}


def get_pack(lang: str) -> LangPack:
    if lang == "en":
        from suraag.lang.en import PACK
    elif lang == "hinglish":
        from suraag.lang.hinglish import PACK
    elif lang == "hi":
        raise NotImplementedError("Devanagari pack is stretch")
    else:
        raise ValueError(f"unknown language {lang!r}")
    return PACK
