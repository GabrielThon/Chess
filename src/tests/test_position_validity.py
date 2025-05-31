import pytest
import json
from pathlib import Path
from src.models.position import Position
from src.models.exceptions import InvalidPositionError, InvalidNumberOfKingsError, NonPlayingPlayerKingInCheckError

POSITIONS_PATH = Path(__file__).parent / "test_position_validity.json"
positions = json.loads(POSITIONS_PATH.read_text())
position_ids = [p["name"] for p in positions]

@pytest.mark.parametrize("scenario", positions, ids=position_ids)

def test_pieces_moving_squares(emptyboard, scenario):
    for color, piece_type, square in scenario["position"]:
        emptyboard.place(color, piece_type, square)

    position = Position(emptyboard, scenario["move"])

    expected = scenario["result"]

    if expected == "True":
        # Expect valid result
        assert position.is_valid_position() is True
    else :
        # Expect an exception of the given name
        with pytest.raises(globals()[expected]):
            position.assert_valid_position()


