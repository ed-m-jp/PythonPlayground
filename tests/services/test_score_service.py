# test_score_service.py
import pytest
from unittest.mock import Mock
from datetime import date
from app.services.score_service import ScoreService
from app.domain.pagination_result import PaginationResult
from app.domain.repository_action_result import RepositoryActionResult
from app.models.baseball_player_score import BaseballPlayerScore
from app.repositories.baseball_player_score_repository import (
    BaseballPlayerScoreRepository,
)
from app.schemas.score_create_schema import ScoreCreate
from app.schemas.score_update_schema import ScoreUpdate


@pytest.fixture
def mock_repository():
    return Mock(BaseballPlayerScoreRepository)


@pytest.fixture
def score_service(mock_repository):
    return ScoreService(mock_repository)


def test_create_score_new(score_service, mock_repository):
    # Arrange
    mock_repository.get_score_from_player_and_date.return_value = (
        RepositoryActionResult.not_found("not found")
    )
    new_score_data = {
        "player_name": "John Doe",
        "score": 10,
        "match_date": date.today(),
    }
    new_score = ScoreCreate(**new_score_data)
    mock_score = BaseballPlayerScore(id=1, **new_score.model_dump())
    mock_repository.create.return_value = RepositoryActionResult.ok(mock_score)

    # Act
    result = score_service.create_score(new_score)

    # Assert
    assert result.is_ok
    assert result.data.id == 1


def test_create_score_duplicate(score_service, mock_repository):
    # Arrange
    existing_score = BaseballPlayerScore(
        id=1,
        player_name="John Doe",
        score=10,
        match_date=date.today()
    )
    mock_repository.get_score_from_player_and_date.return_value = (
        RepositoryActionResult.ok(existing_score)
    )
    score_create = ScoreCreate(
        player_name="John Doe",
        score=10,
        match_date=date.today()
    )

    # Act
    result = score_service.create_score(score_create)

    # Assert
    assert result.is_conflict


def test_get_score(score_service, mock_repository):
    # Arrange
    mock_score = BaseballPlayerScore(
        id=1,
        player_name="John Doe",
        score=10,
        match_date=date.today()
    )
    repository_result = RepositoryActionResult.ok(mock_score)
    mock_repository.get_by_id.return_value = repository_result

    # Act
    result = score_service.get_score(mock_score.id)

    # Assert
    assert result.is_ok
    assert result.data.id == 1
    assert result.data.player_name == "John Doe"


def test_update_score(score_service, mock_repository):
    # Arrange
    score_id = 1
    update_data = ScoreUpdate(player_name="Jane Doe")
    updated_score = BaseballPlayerScore(
        id=score_id,
        player_name="Jane Doe",
        score=10,
        match_date=date.today()
    )
    mock_repository.update.return_value = (
        RepositoryActionResult.ok(updated_score)
    )

    # Act
    result = score_service.update_score(score_id, update_data)

    # Assert
    assert result.is_ok
    assert result.data.player_name == "Jane Doe"


def test_update_score_not_found(score_service, mock_repository):
    # Arrange
    score_id = 1
    update_data = ScoreUpdate(player_name="Jane Doe")
    mock_repository.update.return_value = (
        RepositoryActionResult.not_found("not found")
    )

    # Act
    result = score_service.update_score(score_id, update_data)

    # Assert
    assert result.is_not_found
    assert result.error_message == "not found"


def test_delete_score(score_service, mock_repository):
    # Arrange
    score_id = 1
    mock_repository.delete.return_value = RepositoryActionResult.ok(None)

    # Act
    result = score_service.delete_score(score_id)

    # Assert
    assert result.is_ok


def test_delete_score_not_found(score_service, mock_repository):
    # Arrange
    score_id = 1
    mock_repository.delete.return_value = (
        RepositoryActionResult.not_found("not found")
    )

    # Act
    result = score_service.delete_score(score_id)

    # Assert
    assert result.is_not_found
    assert result.error_message == "not found"


def test_search_scores(score_service, mock_repository):
    # Arrange
    mock_scores = [
        BaseballPlayerScore(
            id=1,
            player_name="John Doe",
            score=20,
            match_date=date.today()
        ),
    ]
    pagination_result = PaginationResult(
        items=mock_scores,
        total_items=len(mock_scores)
    )
    mock_repository.search_scores.return_value = RepositoryActionResult.ok(
        pagination_result
    )

    # Act
    result = score_service.search_scores(
        min_score=10,
        player_name=None,
        player_team=None,
        start_date=None,
        end_date=None,
        page=1,
        page_size=10
    )

    # Assert
    assert result.is_ok
    assert len(result.data.items) == len(mock_scores)
    assert result.data.pagination.total_items == len(mock_scores)
    assert result.data.pagination.total_pages == 1
    assert result.data.pagination.current_page == 1
    assert result.data.pagination.page_size == 10
