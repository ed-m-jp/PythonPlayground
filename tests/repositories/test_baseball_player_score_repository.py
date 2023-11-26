# test_baseball_player_score_repository.py
import pytest
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.baseball_player_score import BaseballPlayerScore
from app.repositories.baseball_player_score_repository import (
    BaseballPlayerScoreRepository,
)


# Fixture for an in-memory SQLite database
@pytest.fixture(scope="function")
def db_session():
    engine = create_engine("sqlite:///:memory:")
    BaseballPlayerScore.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()
    yield session  # provide the session for the test
    session.close()  # teardown: close the session after the test

# Fixture for the repository
@pytest.fixture(scope="function")
def baseball_player_score_repository(db_session):
    return BaseballPlayerScoreRepository(db_session)


def test_create_baseball_player_score(baseball_player_score_repository):
    # Arrange
    new_score = BaseballPlayerScore(
        player_name="John Doe",
        player_team="Team A",
        score=10,
        match_date=datetime.strptime("2023-01-01", "%Y-%m-%d").date()  # Convert string to date
    )

    # Act
    result = baseball_player_score_repository.create(new_score)

    # Assert
    assert result.is_ok
    assert result.entity.id is not None
    assert result.entity.player_name == "John Doe"
    assert result.entity.player_team == "Team A"
    assert result.entity.score == 10
    assert result.entity.match_date == datetime.strptime("2023-01-01", "%Y-%m-%d").date()


def test_get_by_id(baseball_player_score_repository):
    # Arrange
    new_score = BaseballPlayerScore(
        player_name="Jane Doe",
        player_team="Team B",
        score=15,
        match_date=datetime.strptime("2023-02-01", "%Y-%m-%d").date()
    )
    created_score = baseball_player_score_repository.create(new_score).entity

    # Act
    retrieved_score = baseball_player_score_repository.get_by_id(created_score.id)

    # Assert
    assert retrieved_score.is_ok
    score = retrieved_score.entity
    assert score.id == created_score.id
    assert score.player_name == "Jane Doe"
    assert score.player_team == "Team B"
    assert score.score == 15
    assert score.match_date == datetime.strptime("2023-02-01", "%Y-%m-%d").date()



def test_get_by_id_not_found(baseball_player_score_repository):
    # Arrange
    score_id = 11

    # Act
    retrieved_score = baseball_player_score_repository.get_by_id(score_id)

    # Assert
    assert retrieved_score.is_not_found
    assert retrieved_score.error_message == f"Entity with id {score_id} not found"


def test_delete(baseball_player_score_repository):
    # Arrange
    score_to_delete = BaseballPlayerScore(
        player_name="Mark Smith",
        player_team="Team C",
        score=20,
        match_date=datetime.strptime("2023-03-01", "%Y-%m-%d").date()
    )
    created_score = baseball_player_score_repository.create(score_to_delete).entity

    # Act
    delete_result = baseball_player_score_repository.delete(created_score.id)

    # Assert
    assert delete_result.is_ok
    deleted_score = baseball_player_score_repository.get_by_id(created_score.id)
    assert not deleted_score.is_ok
    assert deleted_score.is_not_found
    assert deleted_score.error_message == f"Entity with id {created_score.id} not found"


def test_update(baseball_player_score_repository):
    # Arrange
    score_to_update = BaseballPlayerScore(
        player_name="Emily Johnson",
        player_team="Team D",
        score=25,
        match_date=datetime.strptime("2023-04-01", "%Y-%m-%d").date()
    )
    created_score = baseball_player_score_repository.create(score_to_update).entity
    update_data = {"score": 30}

    # Act
    update_result = baseball_player_score_repository.update(created_score.id, update_data)

    # Assert
    assert update_result.is_ok
    updated_score = baseball_player_score_repository.get_by_id(created_score.id).entity
    assert updated_score.score == 30
    assert updated_score.score == update_result.entity.score
    assert updated_score.player_name == update_result.entity.player_name
    assert updated_score.player_team == update_result.entity.player_team
    assert updated_score.match_date == update_result.entity.match_date


def test_get_score_from_player_and_date(baseball_player_score_repository):
    # Arrange
    test_score = BaseballPlayerScore(
        player_name="Test Player",
        player_team="Test Team",
        score=100,
        match_date=datetime.strptime("2023-05-01", "%Y-%m-%d").date()
    )
    baseball_player_score_repository.create(test_score)

    # Act
    result = baseball_player_score_repository.get_score_from_player_and_date(
        "Test Player", datetime.strptime("2023-05-01", "%Y-%m-%d").date()
    )

    # Assert
    assert result.is_ok
    assert result.entity.player_name == "Test Player"
    assert result.entity.match_date == datetime.strptime("2023-05-01", "%Y-%m-%d").date()


def test_search_scores(baseball_player_score_repository):
    # Arrange
    scores_to_create = [
        BaseballPlayerScore(
            player_name="Player A",
            player_team="Team X",
            score=40,
            match_date=datetime.strptime("2023-06-01", "%Y-%m-%d").date()
        ),
        BaseballPlayerScore(
            player_name="Player B",
            player_team="Team Y",
            score=60,
            match_date=datetime.strptime("2023-07-01", "%Y-%m-%d").date()
        ),
        BaseballPlayerScore(
            player_name="Player C",
            player_team="Team Z",
            score=70,
            match_date=datetime.strptime("2023-08-01", "%Y-%m-%d").date()
        ),
    ]
    
    for score in scores_to_create:
        baseball_player_score_repository.create(score)

    # Act
    search_result = baseball_player_score_repository.search_scores(
        min_score=50,
        start_date=datetime.strptime("2023-01-01", "%Y-%m-%d").date(),
        end_date=datetime.strptime("2023-12-31", "%Y-%m-%d").date(),
        page=1,
        page_size=10
    )

    # Assert
    assert search_result.is_ok
    assert len(search_result.entity.items) == 2
    assert all(score.score >= 50 for score in search_result.entity.items)
    assert search_result.entity.total_items >= 2
