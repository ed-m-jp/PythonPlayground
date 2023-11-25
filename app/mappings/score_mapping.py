# Local application/library specific imports
from app.schemas.score_dto import ScoreDTO


def convert_score_entity_to_dto(model_instance):
    return ScoreDTO.parse_obj(model_instance.__dict__)
