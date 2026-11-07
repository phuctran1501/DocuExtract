"""Unit tests for text normalization and statistics calculation."""

from app.services.text_service import (
    analyze_text,
    compute_text_stats,
    normalize_text,
)


def test_normalize_empty_and_whitespace_only() -> None:
    """Empty strings or strings with only whitespace must normalize to empty string."""
    assert normalize_text("") == ""
    assert normalize_text("   ") == ""
    assert normalize_text("\t\t\n  \r\n  ") == ""


def test_normalize_unicode_nfc_vietnamese() -> None:
    """Decomposed (NFD) Vietnamese characters must normalize to composed (NFC) form."""
    # "Đại học Bách Khoa" with combining diacritics
    decomposed = "Đa\u0323i ho\u0323c Ba\u0301ch Khoa"
    composed = "Đại học Bách Khoa"

    result = normalize_text(decomposed)
    assert result == composed


def test_normalize_line_endings() -> None:
    """Windows (CRLF) and legacy Mac (CR) line endings must normalize to Unix LF."""
    raw = "Line 1\r\nLine 2\rLine 3\nLine 4"
    expected = "Line 1\nLine 2\nLine 3\nLine 4"
    assert normalize_text(raw) == expected


def test_normalize_control_characters_and_zero_width() -> None:
    """Null bytes, control characters, and zero-width characters must be stripped."""
    raw = "Hello\x00\x08 World\u200b!\ufeff"
    expected = "Hello World!"
    assert normalize_text(raw) == expected


def test_normalize_whitespace_and_tabs() -> None:
    """Multiple spaces, tabs, and Unicode NBSP must collapse to a single space."""
    raw = "   Word1    Word2\t\tWord3\u00a0Word4   "
    expected = "Word1 Word2 Word3 Word4"
    assert normalize_text(raw) == expected


def test_normalize_excessive_blank_lines() -> None:
    """Three or more consecutive newlines must collapse to maximum two newlines."""
    raw = "Paragraph 1\n\n\n\n\nParagraph 2"
    expected = "Paragraph 1\n\nParagraph 2"
    assert normalize_text(raw) == expected


def test_compute_text_stats_empty() -> None:
    """Empty string returns all zeroes."""
    stats = compute_text_stats("")
    assert stats.character_count == 0
    assert stats.word_count == 0
    assert stats.line_count == 0


def test_compute_text_stats_single_line() -> None:
    """Single-line string returns correct length, word, and line count."""
    text = "Hello world from DocuExtract"
    stats = compute_text_stats(text)
    assert stats.character_count == len(text)
    assert stats.word_count == 4
    assert stats.line_count == 1


def test_compute_text_stats_multiline() -> None:
    """Multi-line string returns correct line count."""
    text = "Line 1\nLine 2\nLine 3"
    stats = compute_text_stats(text)
    assert stats.character_count == len(text)
    assert stats.word_count == 6
    assert stats.line_count == 3


def test_analyze_text_combined_pipeline() -> None:
    """analyze_text must normalize then compute stats on the normalized text."""
    raw = "   \r\n  First line  \r\n\r\n\r\n  Second   line  \r\n  "
    normalized, stats = analyze_text(raw)

    assert normalized == "First line\n\nSecond line"
    assert stats.character_count == len(normalized)
    assert stats.word_count == 4
    assert stats.line_count == 3
