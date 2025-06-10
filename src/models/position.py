from typing import Optional

from src.models.move import Move
from src.models.square import Square
from src.models.pieces import Piece, King, RecursiveControlledSquaresMixin
from src.models import exceptions
from src.models import utils


# State of the board
class Position:
    def __init__(self, pieces_input: list[list[str]] | dict[str, dict[str, set['Piece']]], whose_move: str = None):
        self.whose_move = whose_move
        self.not_turn_to_move = "black" if self.whose_move == "white" else "white"
        # TO DO : Implement castling rights
        # TO DO : Implement en_passant (last piece_who_moved)

        # Construct squares
        self.square_by_name: dict[str, "Square"]
        self.grid: list[list["Square"]]
        self.square_by_name, self.grid = self._build_squares()

        # Construct pieces from the input
        self.pieces: dict[str, dict[str, set[Piece]]] = self.pieces_initialize()
        if isinstance(pieces_input, list):
            self._initialize_pieces_from_list(pieces_input)
        elif isinstance(pieces_input, dict):
            self._initialize_pieces_from_dict(pieces_input)
        else:
            raise ValueError("Invalid input type for Position. Expected List[List[str]] or Dict[str, Dict[str, Set[Piece]]]")

        self.legal_moves_ = None

    def __str__(self):
        board_string = " ——" * 8 + "\n"
        for row in reversed(self.rows):
            board_string += "|"
            for column in self.columns:
                board_string += str(self.square(column + row)) + "|"
            board_string += "\n" + " ——" * 8 + "\n"
        return board_string

    def assert_valid_position(self):
        # Each player must have one king
        if not self._has_two_kings():
            raise exceptions.InvalidNumberOfKingsError()
        # The king of the player not playing must not be in check
        if self._king_in_check(next(iter(self.pieces[self.not_turn_to_move]["King"]))):
            raise exceptions.NonPlayingPlayerKingInCheckError(self.not_turn_to_move)
        # There should be no pawn on the 1st or 8th rank
        if self._has_pawn_on_first_eighth_rank():
            raise exceptions.PawnOnFirstOrEighthRowError()

    def is_valid_position(self):
        try:
            self.assert_valid_position()
        except exceptions.InvalidPositionError as e:
            print(e)
            return False
        else:
            return True

    def _has_two_kings(self) -> bool:
        for color in self.pieces.keys():
            if len(self.pieces[color]["King"]) != 1:
                return False
        return True

    def _king_in_check(self, king: King) -> bool:
        if king.square in self._controlled_squares(king.opposite_color):
            return True
        return False

    def _has_pawn_on_first_eighth_rank(self):
        for color in self.pieces.keys():
            pawn_set = self.pieces[color]["Pawn"]
            for pawn in pawn_set:
                if pawn.square.row in [0, 7]:
                    return True
        return False

    def _controlled_squares(self, color_string: "str") -> set["Square"]:
        return set().union(*(piece.controlled_squares() for piece_set in self.pieces[color_string].values() for piece in piece_set))

    def _explore_checks_and_pins(self) -> [set["Piece"], set["Square"], dict["Piece", set["Square"]]]:
        pinned_pieces_squares_dict = {}
        checking_pieces = set()
        intercepting_squares = set()
        king = next(iter(self.pieces[self.whose_move]["King"]))
        for direction in king.moving_directions():
            squareset1, first_piece = king.square.explore_in_direction(direction)
            if not first_piece:
                continue
            if first_piece.color == king.opposite_color and isinstance(first_piece, RecursiveControlledSquaresMixin) and direction in first_piece.moving_directions():
                checking_pieces.add(first_piece)
                if len(checking_pieces) == 1:
                    intercepting_squares = squareset1
                else:
                    intercepting_squares = set()
            elif first_piece.color == king.color:
                squareset2, second_piece = first_piece.square.explore_in_direction(direction)
                if second_piece and second_piece.color == king.opposite_color and isinstance(second_piece, RecursiveControlledSquaresMixin) and direction in second_piece.moving_directions():
                    pinned_pieces_squares_dict[first_piece] = (squareset1 | squareset2) - {first_piece.square} if direction in first_piece.moving_directions() else set()
        return checking_pieces, intercepting_squares, pinned_pieces_squares_dict

    def compute_legal_moves(self):
        if not self.is_valid_position():
            self.legal_moves_ = {}
        legal_moves = {}
        checking_pieces, intercepting_squares, pinned_pieces = self._explore_checks_and_pins()
        if len(checking_pieces) == 0:
            category = "no check"
        elif len(checking_pieces) == 1:
            category = "simple check"
        else:
            category = "double check"
        for piece in (p for s in self.pieces[self.whose_move].values() for p in s):
            if isinstance(piece, King):
                controlled_squares = self._controlled_squares(piece.opposite_color)
                legal_moves[piece] = piece.moving_squares() - controlled_squares
                continue
            if category == "double check":
                legal_moves[piece] = set()
                continue
            restricted_squares = pinned_pieces[piece] if piece in pinned_pieces.keys() else piece.moving_squares()
            if category == "no check":
                legal_moves[piece] = restricted_squares
            else:  # category == "simple check" -> Intercepting squares
                legal_moves[piece] = restricted_squares & intercepting_squares
        self.legal_moves_ = legal_moves

    def _build_squares(self) -> tuple[dict[str, "Square"], list[list["Square"]]]:
        columns, rows = utils.generate_columns_rows()
        square_by_name: dict[str, Square] = {}
        square_grid: list[list[Square]] = []

        for i, column in enumerate(columns):
            square_grid.append([])
            for row in rows:
                square = Square(column + row, self)
                square_by_name[column + row] = square
                square_grid[i].append(square)

        return square_by_name, square_grid

    @staticmethod
    def pieces_initialize() -> dict[str, dict[str, set[Piece]]]:
        colors = {"white", "black"}
        piece_types = {"King", "Queen", "Rook", "Bishop", "Knight", "Pawn"}

        pieces = {}
        for color in colors:
            pieces[color] = {}
            for piece_type in piece_types:
                pieces[color][piece_type] = set()
        return pieces

    def _initialize_pieces_from_list(self, position_description: list[list[str]]):
        colors = {"white", "black"}
        piece_types = {"King", "Queen", "Rook", "Bishop", "Knight", "Pawn"}
        self.pieces = {}
        for color in colors:
            self.pieces[color] = {}
            for piece_type in piece_types:
                self.pieces[color][piece_type] = set()

        for piece_desc in position_description:
            color, piece_type, square_string = piece_desc
            if not utils.is_valid_color(color):
                raise exceptions.InvalidColorError
            self.place_piece(color, piece_type, square_string)

    def _initialize_pieces_from_dict(self, pieces_input: dict[str, dict[str, set['Piece']]]):
        colors = {"white", "black"}
        piece_types = {"King", "Queen", "Rook", "Bishop", "Knight", "Pawn"}
        if not set(pieces_input.keys()).issubset(colors):
            raise KeyError(f"Unsupported color key(s): {set(pieces_input.keys()) - colors}")
        for color in colors:
            if not set(pieces_input[color].keys()).issubset(piece_types):
                raise KeyError(f"Unsupported piece type(s): {set(pieces_input[color].keys()) - piece_types}")
            for piece_type, piece_set in pieces_input[color].items():
                for piece in piece_set:
                    self.place_piece(piece.color, piece.type, piece.square.name)


    def place_piece(self, color: str, piece_type: str, square_string: "Square") -> "Piece":
        piece = self.square_by_name[square_string].place(color, piece_type)
        self.pieces[color][piece_type].add(piece)
        self.legal_moves_ = None
        return piece

    def remove_piece(self, square_string):
        self.legal_moves_ = None
        return self.square(square_string).remove_piece()


    def square(self, key: str | list | tuple) -> Optional["Square"]:
        # Returns None if the label or indices point at a square not in the grid.
        if isinstance(key, str):
            if not self.square_by_name.get(key, None):
                return None
            col_idx, row_idx = utils.label_to_indices(key)
        elif isinstance(key, (list, tuple)) and len(key) == 2:
            col_idx, row_idx = key
            if not (0 <= col_idx < 8 and 0 <= row_idx < 8):
                return None
        else:
            raise TypeError("Argument must be a string, list or tuple")
        return self.grid[col_idx][row_idx]

    def piece(self, key: str | list | tuple) -> Optional[Piece]:
        square = self.square(key)
        return square.piece if square else None

    @property
    def all_pieces(self):
        all_pieces = set()
        for type_dict in self.pieces.values():
            for piece_set in type_dict.values():
                for piece in piece_set:
                    all_pieces.add(piece)
        return all_pieces

    def make_move(self, move: "Move") -> "Position":
        assert move.is_legal_move(), "Illegal move passed to make_move()"
        new_position = Position(self.pieces, whose_move=self.not_turn_to_move)
        new_position.remove_piece(move.departure_square.name)
        new_position.remove_piece(move.target_square.name)
        new_position.place_piece(move.piece.color, move.piece.type, move.target_square.name)
        return new_position




##    Doesn't belong here : maybe at the Game level
#     def _initial_position(self):
#         for [color, piece, square] in utils.starting_position():
#             self.place_piece(color, piece, square)
