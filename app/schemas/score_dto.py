from datetime import date
from pydantic import BaseModel
from typing import Optional


class ScoreDTO(BaseModel):
    id: int
    player_name: str
    player_team: Optional[str] = None
    score: int
    match_date: date

    class Config:
        from_attributes = True
