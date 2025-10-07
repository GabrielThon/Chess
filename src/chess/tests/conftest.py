import pytest
from src.chess.models.position import Position
from src.chess.models import utils


@pytest.fixture
def starting_position():
    board = Position(utils.starting_position())
    return board


