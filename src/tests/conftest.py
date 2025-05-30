import pytest
from src.models.board import Board

@pytest.fixture
def fullboard():
    board = Board()
    return board

@pytest.fixture
def emptyboard():
    board = Board.create_empty_board()
    return board
