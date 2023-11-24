from sqlalchemy import Column, Integer, String, Date, UniqueConstraint
from sqlalchemy.schema import Index
from app.database.database import Base


class BaseballPlayerScore(Base):
    __tablename__ = 'baseball_player_scores'

    id = Column(Integer, primary_key=True, autoincrement=True)
    player_name = Column(String, nullable=False)
    player_team = Column(String)
    score = Column(Integer, nullable=False)
    match_date = Column(Date, nullable=False)

    # Add unique constraint on player_name and match_date
    __table_args__ = (
        UniqueConstraint(
            'player_name',
            'match_date',
            name='uix_player_name_match_date'
        ),
    )

    # Add a composite index for better query performance
    __table_args__ = (
        Index(
            'ix_player_name_match_date',
            'player_name',
            'match_date'),
        )
