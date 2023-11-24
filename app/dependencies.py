from sqlalchemy.orm import Session
from fastapi import Depends
from app.database.database import SessionLocal
from app.repositories.baseball_player_score_repository import (
    BaseballPlayerScoreRepository,
)
from app.services.score_service import ScoreService


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_score_repository(db: Session = Depends(get_db)):
    return BaseballPlayerScoreRepository(db)


def get_score_service(
    repository: BaseballPlayerScoreRepository = Depends(get_score_repository),
):
    return ScoreService(repository)
