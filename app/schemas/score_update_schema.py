# Standard library imports
from datetime import date
from typing import Optional

# Related third-party imports
from pydantic import BaseModel, Field, model_validator, validator


class ScoreUpdate(BaseModel):
    player_name: Optional[str] = Field(None, min_length=1)
    player_team: Optional[str] = None
    score: Optional[int] = Field(None, ge=1)
    match_date: Optional[date] = None

    @model_validator(mode='after')
    def check_at_least_one_field(self):
        if not any(
            [
                self.player_name,
                self.player_team,
                self.score,
                self.match_date
            ]
        ):
            raise ValueError("At least one field must be provided for update")
        return self

    @validator("player_name", always=True)
    def validate_player_name(cls, value):
        if value is not None and not value.strip():
            raise ValueError("Player name must not be empty or blank")
        return value
