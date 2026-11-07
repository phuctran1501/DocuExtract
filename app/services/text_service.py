"""Text processing and normalization service."""

import re
import unicodedata
from dataclasses import dataclass

# Remove null bytes and non-printable ASCII control characters except \t and \n
_CONTROL_CHAR_RE = re.compile(r"[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]")

# Invisible and zero-width characters: ZWSP, ZWNJ, ZWJ, BOM
_ZERO_WIDTH_RE = re.compile(r"[\u200b\u200c\u200d\ufeff]")

# Unicode space variants (NBSP, em-space, en-space, etc.)
_UNICODE_SPACES_RE = re.compile(r"[\u00a0\u1680\u2000-\u200a\u202f\u205f\u3000]")

# Standardize line breaks: CRLF and CR -> LF
_LINE_BREAK_RE = re.compile(r"\r\n|\r")

# Horizontal whitespace sequence (spaces and tabs)
_HORIZONTAL_SPACES_RE = re.compile(r"[^\S\n]+")

# Excessive blank lines (collapse 3 or more consecutive newlines to 2)
_EXCESSIVE_NEWLINES_RE = re.compile(r"\n{3,}")


@dataclass(frozen=True)
class TextStats:
    """Deterministic text statistics."""

    character_count: int
    word_count: int
    line_count: int


def normalize_text(text: str) -> str:
    """Normalize raw text into clean, deterministic Unicode text.

    Pipeline:
    1. Strip zero-width characters and non-printable control characters.
    2. Normalize Unicode to canonical composition (NFC).
    3. Convert Unicode space variants to standard ASCII space.
    4. Normalize line breaks to Unix LF (\\n).
    5. Collapse multiple horizontal whitespace on each line and strip line ends.
    6. Limit consecutive blank lines to at most two newlines.
    7. Strip leading and trailing whitespace from the document.
    """
    if not text:
        return ""

    # 1. Strip zero-width characters and control chars
    text = _ZERO_WIDTH_RE.sub("", text)
    text = _CONTROL_CHAR_RE.sub("", text)

    # 2. Normalize Unicode to NFC
    text = unicodedata.normalize("NFC", text)

    # 3. Convert Unicode spaces to standard space
    text = _UNICODE_SPACES_RE.sub(" ", text)

    # 4. Standardize line breaks
    text = _LINE_BREAK_RE.sub("\n", text)

    # 5. Collapse horizontal whitespace and strip each line
    lines = [_HORIZONTAL_SPACES_RE.sub(" ", line).strip() for line in text.split("\n")]
    text = "\n".join(lines)

    # 6. Collapse excessive blank lines (max 2 consecutive newlines)
    text = _EXCESSIVE_NEWLINES_RE.sub("\n\n", text)

    # 7. Strip leading and trailing whitespace
    return text.strip()


def compute_text_stats(text: str) -> TextStats:
    """Compute deterministic character, word, and line counts.

    - character_count: Total characters in the string.
    - word_count: POSIX-style whitespace word count (len(text.split())).
    - line_count: Total lines in the string (0 for empty string).
    """
    if not text:
        return TextStats(character_count=0, word_count=0, line_count=0)

    character_count = len(text)
    word_count = len(text.split())
    lines = text.splitlines()
    line_count = len(lines) if lines else 0

    return TextStats(
        character_count=character_count,
        word_count=word_count,
        line_count=line_count,
    )


def analyze_text(text: str) -> tuple[str, TextStats]:
    """Normalize text and compute statistics in a single call."""
    normalized = normalize_text(text)
    stats = compute_text_stats(normalized)
    return normalized, stats
