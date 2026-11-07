"""Pydantic schemas for text analysis endpoint."""

from pydantic import BaseModel, Field


class TextAnalyzeRequest(BaseModel):
    """Request payload for text analysis."""

    text: str = Field(
        ...,
        max_length=1_000_000,
        description="The raw text to normalize and analyze.",
    )


class TextAnalyzeResponse(BaseModel):
    """Response payload containing deterministic text statistics."""

    character_count: int = Field(
        ..., ge=0, description="Total characters after normalization."
    )
    word_count: int = Field(..., ge=0, description="Total word count.")
    line_count: int = Field(..., ge=0, description="Total line count.")
