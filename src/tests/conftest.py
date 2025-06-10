import pytest
from src.models.position import Position
from src.models import utils


@pytest.fixture
def starting_position():
    board = Position(utils.starting_position())
    return board


