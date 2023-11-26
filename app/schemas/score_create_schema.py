# Standard library imports
from datetime import date
from typing import Optional

# Related third-party imports
from pydantic import BaseModel, Field, field_validator


class ScoreCreate(BaseModel):
    player_name: str = Field(..., min_length=1)
    player_team: Optional[str] = None
    score: int = Field(..., ge=0)
    match_date: date

    # This will check for name with only spaces that would bypass the
    # min_length=1 check.
    @field_validator('player_name')
    def name_must_not_be_empty(cls, value):
        if not value.strip():
            raise ValueError("Player name must not be empty.")
        return value
