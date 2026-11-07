"""Text analysis and processing routes."""

from fastapi import APIRouter, status

from app.schemas.text import TextAnalyzeRequest, TextAnalyzeResponse
from app.services.text_service import analyze_text

router = APIRouter(prefix="/text", tags=["Text Analysis"])


@router.post(
    "/analyze",
    response_model=TextAnalyzeResponse,
    status_code=status.HTTP_200_OK,
    summary="Analyze and normalize text",
    description=(
        "Normalizes input text and returns deterministic character, word, "
        "and line counts."
    ),
)
async def analyze_text_endpoint(payload: TextAnalyzeRequest) -> TextAnalyzeResponse:
    """Normalize input text and return deterministic text statistics."""
    _, stats = analyze_text(payload.text)
    return TextAnalyzeResponse(
        character_count=stats.character_count,
        word_count=stats.word_count,
        line_count=stats.line_count,
    )
