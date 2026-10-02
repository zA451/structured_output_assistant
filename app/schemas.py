"""Pydantic model for the assistant's structured response."""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class StructuredAnswer(BaseModel):
    """The fields expected in every study assistant response."""
    model_config = ConfigDict(extra="forbid")

    question: str
    answer: str
    topic: str
    difficulty: Literal["easy", "medium", "hard"]
    key_points: list[str] = Field(min_length=2, max_length=5)
