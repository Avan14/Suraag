"""Language packs: get_pack(lang). Each pack holds what differs by language: trigger phrases,
alias patterns, places, stub lines, instruction templates and LLM prompts."""
import re
from dataclasses import dataclass, field


@dataclass(frozen=True)
class LangPack:
    lang: str
    triggers: dict[str, re.Pattern]       # applied to norm(text)
    alias_patterns: dict[str, str]        # by gender ("m"/"f"): the name as saved in a phone, e.g. "{first} bhai"
    places: list[tuple[str, float, float]]
    stub_lines: list[str]                 # offline filler; never matches a trigger
    instruction_templates: list[str]      # format with {owner}; always matches triggers["instruction"]
    question_texts: dict[str, str]        # who / when / where
    filler_prompt: str                    # str.format fields: see suraag/filler.py
    raw_prompt: str                       # str.format fields: see suraag/rawmode.py
    brief_summary: str                    # str.format fields: {amount}, {date}
    # Practice levels (suraag/levels.py). Every line below is written verbatim by code, never by the LLM.
    call_ref: str = ""                    # "as I said on the phone, ": must match triggers["call_ref"]
    go_templates: tuple[str, ...] = ()    # the order with {owner} and {call}; with call="" they equal instruction_templates
    code_words: tuple[str, ...] = ()      # innocent-looking phrases that stand for the order
    code_def_templates: tuple[str, ...] = ()  # {code}; matches triggers["code_def"] AND triggers["instruction"] (the trap)
    code_go_templates: tuple[str, ...] = ()   # {owner}, {call}, {code}; never matches triggers["instruction"]
    confirm_templates: tuple[str, ...] = ()   # the mule's "done"; matches triggers["confirm"]
    decoy_templates: tuple[str, ...] = ()     # {owner}; a harmless request that still matches triggers["instruction"]
    alibi_templates: tuple[str, ...] = ()     # {place}; the mule's claim about where they are
    # Case families (suraag/families.py): family -> template name -> text, all written verbatim by code.
    families: dict = field(default_factory=dict)


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
