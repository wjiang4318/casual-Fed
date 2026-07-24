from typing import Literal
from pydantic import BaseModel, Field


class Dissenter(BaseModel):
    name: str
    preferred_action: Literal["more_dovish", "more_hawkish", "procedural"]


class MeetingExtraction(BaseModel):
    is_rate_decision: bool
    decision: Literal["hike", "hold", "cut"] | None = None
    magnitude_bps: int | None = Field(default=None, ge=0)
    tone: Literal["hawkish", "dovish", "neutral"] | None = None
    tone_confidence: float | None = Field(default=None, ge=0.0, le=1.0)
    dissenters: list[Dissenter] = []