# Standard library imports
from datetime import date
from typing import Optional

# Related third-party imports
from sqlalchemy.orm import Session

# Local application/library specific imports
from app.domain.pagination_result import PaginationResult
from app.domain.repository_action_result import RepositoryActionResult
from app.models.baseball_player_score import BaseballPlayerScore
from app.repositories.repository_base import RepositoryBase


class BaseballPlayerScoreRepository(RepositoryBase[BaseballPlayerScore]):
    def __init__(self, db: Session):
        super().__init__(db, BaseballPlayerScore)

    def get_score_from_player_and_date(
        self,
        player_name: str,
        match_date: date
    ) -> RepositoryActionResult[BaseballPlayerScore]:
        try:
            score = (
                self.db.query(BaseballPlayerScore)
                .filter(
                    BaseballPlayerScore.player_name == player_name,
                    BaseballPlayerScore.match_date == match_date,
                )
                .first()
            )

            if score:
                return RepositoryActionResult.ok(score)
            else:
                return RepositoryActionResult.not_found(
                    f"Score not found for player ['{player_name}'] "
                    f"on date ['{match_date}']"
                )
        except Exception as e:
            # TODO - Log exception
            return (
                RepositoryActionResult
                .error(exception=e, error_message=str(e))
            )

    def search_scores(
        self,
        player_name: Optional[str],
        player_team: Optional[str],
        min_score: Optional[int],
        start_date: Optional[date],
        end_date: Optional[date],
        page: int,
        page_size: int
    ) -> RepositoryActionResult[PaginationResult]:
        try:
            query = self.db.query(BaseballPlayerScore)

            if player_name is not None:
                query = query.filter(
                    BaseballPlayerScore.player_name == player_name
                )
            if player_team is not None:
                query = query.filter(
                    BaseballPlayerScore.player_team == player_team
                )
            if min_score is not None:
                query = query.filter(
                    BaseballPlayerScore.score >= min_score
                )
            if start_date is not None:
                query = query.filter(
                    BaseballPlayerScore.match_date >= start_date
                )
            if end_date is not None:
                query = query.filter(
                    BaseballPlayerScore.match_date <= end_date
                )

            total_items = query.count()

            scores = (
                query
                .offset((page - 1) * page_size)
                .limit(page_size)
                .all()
            )

            result = PaginationResult(
                items=scores,
                total_items=total_items,
            )
            return RepositoryActionResult.ok(result)
        except Exception as e:
            # TODO - Log exception
            return (
                RepositoryActionResult
                .error(exception=e, error_message=str(e))
            )
