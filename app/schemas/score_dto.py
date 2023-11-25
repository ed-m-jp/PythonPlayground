# Standard library imports
from datetime import date
from typing import Optional

# Related third-party imports
from pydantic import BaseModel


class ScoreDTO(BaseModel):
    id: int
    player_name: str
    player_team: Optional[str] = None
    score: int
    match_date: date

    class Config:
        from_attributes = True
