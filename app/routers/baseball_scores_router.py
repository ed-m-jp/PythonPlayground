# Standard library imports
from datetime import date
from typing import Optional

# Third-party imports
from fastapi import APIRouter, Depends, HTTPException, Query, Response, status

# Local application imports
from app.dependencies import get_score_service
from app.schemas.pagination_response import PaginationResponse
from app.schemas.score_create_schema import ScoreCreate
from app.schemas.score_dto import ScoreDTO
from app.schemas.score_update_schema import ScoreUpdate
from app.services.score_service import ScoreService

router = APIRouter()


@router.get(
    "/scores/{score_id}",
    response_model=ScoreDTO,
    summary="Get a score by ID",
    status_code=status.HTTP_200_OK,
    responses={404: {"description": "Score not found"}},
)
def get_score(
    score_id: int,
    score_service: ScoreService = Depends(get_score_service)
):
    """
    Retrieve a specific baseball score by its ID.

    - **score_id**: The unique identifier of the score.
    - **returns**: The created score details.
    """
    get_result = score_service.get_score(score_id)

    if get_result.is_ok:
        return get_result.data
    elif get_result.is_not_found:
        raise_not_found_exception(f"No score for ID [{score_id}] not found.")
    else:
        raise Exception(get_result.error_message)


@router.post(
    "/scores",
    response_model=ScoreDTO,
    status_code=status.HTTP_201_CREATED,
    responses={422: {"description": "Validation Error"}},
)
def create_score(
    score_to_create: ScoreCreate,
    score_service: ScoreService = Depends(get_score_service)
):
    """
    Create a new baseball score.

    - **score**: The score to be created.
    - **returns**: The created score details.
    """
    create_result = score_service.create_score(score_to_create)

    if create_result.is_ok:
        return create_result.data
    elif create_result.is_conflict:
        raise_conflict_exception(
            f"A score for PLAYER NAME [{score_to_create.player_name}] "
            f"and date [{score_to_create.match_date}] already exist."
        )
    else:
        raise Exception(create_result.error_message)


@router.patch(
    "/scores/{score_id}",
    summary="Update a score by ID",
    status_code=status.HTTP_200_OK,
    responses={
        404: {"description": "Score not found"},
        422: {"description": "Validation Error"},
    },
)
def patch_score(
    score_id: int,
    score: ScoreUpdate,
    score_service: ScoreService = Depends(get_score_service)
):
    """
    Update an existing baseball score by its ID.

    - **score_id**: The unique identifier of the score to be updated.
    - **score**: The score data to update.
    - **returns**: Updated score details.
    """
    update_result = score_service.update_score(score_id, score)

    if update_result.is_ok:
        return update_result.data
    elif update_result.is_not_found:
        raise_not_found_exception(f"No score for ID [{score_id}] not found.")
    else:
        raise Exception(update_result.error_message)


@router.delete(
    "/scores/{score_id}",
    summary="Delete a score by ID",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={404: {"description": "Score not found"}},
)
def delete_score(
    score_id: int,
    score_service: ScoreService = Depends(get_score_service)
):
    """
    Delete a specific baseball score by its ID.

    - **score_id**: The unique identifier of the score to be deleted.
    - **returns**: A message indicating successful deletion.
    """
    delete_result = score_service.delete_score(score_id)

    if delete_result.is_ok:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    elif delete_result.is_not_found:
        raise_not_found_exception(f"No score for ID [{score_id}] not found.")
    else:
        raise Exception(delete_result.error_message)


@router.get(
    "/scores",
    response_model=PaginationResponse,
    summary="Search scores",
    status_code=status.HTTP_200_OK,
)
def search_scores(
    min_score: Optional[int] = Query(
        None, ge=0, description="Minimum score filter"
    ),
    start_date: Optional[date] = Query(
        None, description="Start date of the range"
    ),
    end_date: Optional[date] = Query(
        None, description="End date of the range"
    ),
    page: int = Query(
        1, ge=1, description="Page number of the results"
    ),
    page_size: int = Query(
        10, ge=5, le=100, description="Number of results per page"
    ),
    score_service: ScoreService = Depends(get_score_service)
):
    """
    Search for baseball scores based on various criteria.

    - **min_score**: Filter scores with a minimum value.
    - **start_date**: Start date for score range filter.
    - **end_date**: End date for score range filter.
    - **returns**: A list of scores matching the criteria.
    """
    # TODO: this is ok for this small api but for bigger one
    # we would need to implement some caching and restriction
    # to query a large amount of data
    search_result = score_service.search_scores(
        min_score=min_score,
        start_date=start_date,
        end_date=end_date,
        page=page,
        page_size=page_size
    )

    if search_result.is_ok:
        return search_result.data
    else:
        raise Exception(search_result.error_message)


def raise_not_found_exception(detail: str):
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=detail
    )


def raise_conflict_exception(detail: str):
    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail=detail
    )
