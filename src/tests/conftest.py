import pytest
from src.models.board import Board


@pytest.fixture
def fullboard():
    board = Board()
    return board


@pytest.fixture
def emptyboard():
    board = Board(empty=True)
    return board

