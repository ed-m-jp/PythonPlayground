from sqlalchemy.orm import Session
from app.models.baseball_player_score import BaseballPlayerScore
from datetime import date


def seed_data(db: Session):
    player_scores = [
        BaseballPlayerScore(
            player_name="John Doe",
            player_team="Team A",
            score=5,
            match_date=date(2023, 1, 1)
        ),
        BaseballPlayerScore(
            player_name="Jane Smith",
            player_team="Team B",
            score=3,
            match_date=date(2023, 1, 2)
        ),
    ]

    for score in player_scores:
        db.add(score)
    db.commit()
