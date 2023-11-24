from app.repositories.baseball_player_score_repository import (
    BaseballPlayerScoreRepository,
)
from app.schemas.score_create_schema import ScoreCreate
from app.schemas.score_update_schema import ScoreUpdate
from app.schemas.score_dto import ScoreDTO
from app.schemas.pagination_response import Pagination, PaginationResponse
from app.models.baseball_player_score import BaseballPlayerScore
from app.domain.service_result import ServiceResult
from app.mappings.score_mapping import convert_score_entity_to_dto
from app.helper.pagination_helper import calculate_total_pages
from datetime import date
from typing import Optional


class ScoreService:
    def __init__(self, repository: BaseballPlayerScoreRepository):
        self.repository = repository

    def create_score(
        self,
        score: ScoreCreate
    ) -> ServiceResult[ScoreDTO]:
        # check for duplicate
        check_result = self.repository.get_score_from_player_and_date(
            score.player_name,
            score.match_date
        )
        if check_result.is_ok:
            return ServiceResult.conflict(
                data=convert_score_entity_to_dto(check_result.entity),
                error_message="Score already exists for player and date"
            )
        elif check_result.is_error:
            return ServiceResult.error(
                exception=check_result.exception,
                error_message=check_result.error_message
            )

        # map score DTO to model.
        score_model = BaseballPlayerScore(**score.dict())

        create_result = self.repository.create(score_model)
        return ServiceResult.from_repository_action_result(
            create_result,
            convert_score_entity_to_dto
        )

    def get_score(self, score_id: int) -> ServiceResult[ScoreDTO]:
        get_result = self.repository.get_by_id(score_id)
        return ServiceResult.from_repository_action_result(
            get_result,
            convert_score_entity_to_dto
        )

    def update_score(
        self,
        score_id: int,
        score: ScoreUpdate
    ) -> ServiceResult[ScoreDTO]:
        # Convert Pydantic model to dictionary, excluding unset fields
        score_data = score.dict(exclude_unset=True)

        update_result = self.repository.update(score_id, score_data)
        return ServiceResult.from_repository_action_result(
            update_result,
            convert_score_entity_to_dto
        )

    def delete_score(self, score_id: int) -> ServiceResult[None]:
        delete_result = self.repository.delete(score_id)
        return ServiceResult.from_repository_action_result(
            delete_result,
            convert_score_entity_to_dto
        )

    def search_scores(
        self,
        min_score: Optional[int],
        start_date: Optional[date],
        end_date: Optional[date],
        page: int,
        page_size: int
    ) -> ServiceResult[PaginationResponse]:
        search_result = self.repository.search_scores(
            min_score=min_score,
            start_date=start_date,
            end_date=end_date,
            page=page,
            page_size=page_size
        )
        if search_result.is_ok:
            pagination = Pagination(
                total_items=search_result.entity.total_items,
                total_pages=calculate_total_pages(
                    search_result.entity.total_items,
                    page_size
                ),
                current_page=page,
                page_size=page_size
            )
            paginated_result = PaginationResponse(
                items=[
                    convert_score_entity_to_dto(score)
                    for score in search_result.entity.items
                ],
                pagination=pagination
            )
            return ServiceResult.ok(paginated_result)
        else:
            error_message = (
                str(search_result.exception)
                or search_result.error_message
                or "An error occurred please try again later."
            )
            return ServiceResult.error(error_message=error_message)

        return ServiceResult.from_repository_action_result(
            search_result,
            convert_score_entity_to_dto
        )
