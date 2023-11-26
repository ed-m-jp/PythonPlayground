# Local application/library specific imports
from app.schemas.score_dto import ScoreDTO


def convert_score_entity_to_dto(model_instance):
    return ScoreDTO.model_validate(model_instance.__dict__)
