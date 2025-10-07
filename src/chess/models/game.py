from .move import Move
from .position import Position
from . import utils


class Game:
    def __init__(self):
        self.current_position: "Position" = Position(utils.starting_position(), whose_move="white")
        self.current_position.compute_legal_moves()
        self.positions_history : list["Position"] = [self.current_position]
        self.moves_history : list["Move"] = []
        self.result = None

    def apply_move(self, move: Move | str, language="English") -> bool:
        if isinstance(move, Move):
            try:
                new_position = self.current_position.make_move(move, language=language)[0]
            except AssertionError:
                print("Illegal move attempted!")
                return False
        elif isinstance(move, str):
            try:
                new_position, move = self.current_position.make_move(move, language=language)
            except ValueError:
                print("Notation doesn't refer to a legal move in the current position")
                return False
        else:
            raise TypeError("move must be a Move or a string")

        self.moves_history.append(move)
        self.positions_history.append(new_position)
        self.current_position = new_position
        self._check_game_end_conditions()
        #Replace + by # in base_notation if it's a mate
        if self.result and "Checkmate" in self.result:
            move.is_checkmate = True
            move.update_full_notation()
        print(move.full_notation)
        return True




    def _check_game_end_conditions(self):
        position = self.current_position
        position.compute_legal_moves()
        if all(not moves for moves in position.legal_moves_.values()):
            # Checkmate
            if position.king_in_check(next(iter(position.pieces[position.whose_move]["King"]))):
                self.result = f"Checkmate ! {position.not_turn_to_move.capitalize()} won."
            #Stalemate
            else:
                self.result = f"Stalemate !"
            print(self.result)
        #TO DO : repetitions, no push pawn and capture ?

if __name__ == "__main__":
    game = Game()
    game.apply_move("Nc3")
    game.apply_move("Cf6", language="French")