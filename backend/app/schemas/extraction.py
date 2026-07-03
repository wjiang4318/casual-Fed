from typing import Literal
from pydantic import BaseModel, Field


class MeetingExtraction(BaseModel):
    decision: Literal["hike", "hold", "cut"]
    magnitude_bps: int = Field(ge=0)
    tone: Literal["hawkish", "dovish", "neutral"]
    tone_confidence: float = Field(ge=0.0, le=1.0)
