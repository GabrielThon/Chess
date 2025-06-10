from src.models.move import Move
from src.models.position import Position
from src.models import utils

class Game:
    def __init__(self):
        self.current_position: "Position" = Position(utils.starting_position(), whose_move="white")
        self.positions_history : list["Position"] = [self.current_position]
        self.moves_history : list["Move"] = []

    def apply_move(self, move: Move) -> bool:
        if not move.is_legal_move():
            return False
        new_position = self.current_position.make_move(move)
        self.moves_history.append(move)
        self.positions_history.append(new_position)
        self.current_position = new_position
        self._check_game_end_conditions()
        return True

    def _check_game_end_conditions(self):
        # Checkmate, stalemate, repetition, etc.
        pass