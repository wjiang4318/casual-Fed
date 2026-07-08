from datetime import date, datetime
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field


class MeetingResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True) # by default pydantic knows how to build a model
    # from dict-like input (ie: data['decision], data['tone']). But a SQLAlchemy Meeting object isn't a dict but a python
    # object where you access fields via .decision, .tone. from_attributes=true 
    # just tells Pydantic: "it's fine if the input looks like an object instead of a dictionary — go ahead and pull the fields off it either way."
    id: int
    date: date
    decision: Literal["hike", "hold", "cut"]
    magnitude_bps: int = Field(ge=0)
    tone: Literal["hawkish", "dovish", "neutral"]
    tone_confidence: float = Field(ge=0.0, le=1.0)
    statement_text: str
    created_at: datetime
