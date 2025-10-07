import pytest
from chess.models.position import Position
from chess.models import utils


@pytest.fixture
def starting_position():
    board = Position(utils.starting_position())
    return board

@pytest.fixture
def emptyboard():
    board = Position([])
    return board

