from typing import Optional

from .directions import Direction
from .move import Move
from .square import Square
from .pieces import Piece, King, RecursiveControlledSquaresMixin, Pawn
from . import exceptions, utils


# State of the position
class Position:
    def __init__(self, pieces_input: list[list[str]] | dict[str, dict[str, set['Piece']]], whose_move: str = None, castling_rights: dict[str, bool] = None, en_passant_target=None):
        self.whose_move = whose_move
        self.not_turn_to_move = "black" if self.whose_move == "white" else "white"
        self.castling_rights = castling_rights or {
            "white_kingside": True,
            "white_queenside": True,
            "black_kingside": True,
            "black_queenside": True
        }
        self.en_passant_target: "Piece" = en_passant_target
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

        self.legal_moves_: dict["Piece", set["Move"]] = None

    def __str__(self):
        columns, rows = utils.generate_columns_rows()
        board_string = " ——" * 8 + "\n"
        for row in reversed(rows):
            board_string += "|"
            for column in columns:
                board_string += str(self.square(column + row)) + "|"
            board_string += "\n" + " ——" * 8 + "\n"
        return board_string

    def assert_valid_position(self):
        # Each player must have one king
        if not self._has_two_kings():
            raise exceptions.InvalidNumberOfKingsError()
        # The king of the player not playing must not be in check
        if self.king_in_check(next(iter(self.pieces[self.not_turn_to_move]["King"]))):
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

    def king_in_check(self, king: King) -> bool:
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
        intercepting_squares = None
        king = next(iter(self.pieces[self.whose_move]["King"]))
        # Handling of Bishop, Rook, Queen checks and pins
        for direction in Direction.diagonals() | Direction.straights():
            squareset1, first_piece = king.square.explore_in_direction(direction)
            if not first_piece:
                continue
            # Checks
            if first_piece.color == king.opposite_color and isinstance(first_piece, RecursiveControlledSquaresMixin) and direction in first_piece.moving_directions():
                checking_pieces.add(first_piece)
                intercepting_squares = squareset1
            # Pins
            elif first_piece.color == king.color:
                squareset2, second_piece = first_piece.square.explore_in_direction(direction)
                if second_piece and second_piece.color == king.opposite_color and isinstance(second_piece, RecursiveControlledSquaresMixin) and direction in second_piece.moving_directions():
                    pinned_pieces_squares_dict[first_piece] = (squareset1 | squareset2) - {first_piece.square} if direction in first_piece.moving_directions() else set()
        # Handling of knight checks
        for direction in Direction.knight_jumps():
            square = king.square.next_square_in_direction(direction)
            if square and square.piece and square.piece.type == "Knight" and square.piece.color == king.opposite_color:
                checking_pieces.add(square.piece)
                intercepting_squares = {square}
        # Handling of pawn checks
        pawn_checking_directions = {"white": {Direction(1, -1), Direction(1, 1)},
                                    "black": {Direction(-1, -1), Direction(-1, 1)}
                                    }
        for direction in pawn_checking_directions[king.color]:
            square = king.square.next_square_in_direction(direction)
            if square and square.piece and square.piece.type == "Pawn" and square.piece.color == king.opposite_color:
                checking_pieces.add(square.piece)
                intercepting_squares = {square}

        # In case of double check, interception is not possible
        if len(checking_pieces) > 1:
            intercepting_squares = None

        return checking_pieces, intercepting_squares, pinned_pieces_squares_dict

    def compute_legal_moves(self) -> dict[Piece, set[Move]]:
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
                opposite_color_controlled_squares = self._controlled_squares(piece.opposite_color)
                accessible_squares = piece.moving_squares() - opposite_color_controlled_squares
                if accessible_squares:
                    legal_moves[piece] = set()
                for square in accessible_squares:
                    legal_moves[piece].add(Move(self, piece, square))
                # Castling moves
                # Rule 1 : Can only be performed if the king is not in check
                if self.king_in_check(piece):
                    continue
                castling_rows = {"white": "1", "black": "8"}
                rank = castling_rows[piece.color]
                # Rule 2 : king and rook have to be on their starting squares and not have moved
                if self.castling_rights.get(f"{piece.color}_kingside"):
                    square_f_file = self.square(f"f{rank}")
                    square_g_file = self.square(f"g{rank}")
                    square_h_file = self.square(f"h{rank}")
                    # Rule 3 : Squares on the path have to be empty and not controlled by opposite color pieces
                    if (
                            not any(square.piece for square in [square_f_file, square_g_file]) and
                            not any(square in opposite_color_controlled_squares for square in [square_f_file, square_g_file])
                    ):
                        legal_moves[piece].add(Move(self, piece, square_g_file, is_castling=True, rook_start=square_h_file, rook_end=square_f_file))
                if self.castling_rights.get(f"{piece.color}_queenside"):
                    square_a_file = self.square(f"a{rank}")
                    square_b_file = self.square(f"b{rank}")
                    square_c_file = self.square(f"c{rank}")
                    square_d_file = self.square(f"d{rank}")
                    if (
                            not any(square.piece for square in [square_b_file, square_c_file, square_d_file]) and
                            not any(square in opposite_color_controlled_squares for square in [square_b_file, square_c_file, square_d_file])
                    ):
                        legal_moves[piece].add(Move(self, piece, square_c_file, is_castling=True, rook_start=square_a_file, rook_end=square_d_file))
                continue
            if category == "double check":
                legal_moves[piece] = set()
                continue
            restricted_squares = pinned_pieces[piece] if piece in pinned_pieces.keys() else piece.moving_squares()
            if category == "no check":
                accessible_squares = restricted_squares
            else:  # category == "simple check" -> Intercepting squares
                accessible_squares = restricted_squares & intercepting_squares
            if accessible_squares:
                legal_moves[piece] = set()
            # Checking en passant
            if self.en_passant_target and isinstance(piece, Pawn):
                # Keys : direction to check where the pawn previously pushed is
                # Values : dict with direction to move for capture depending on color
                en_passant_directions = {Direction(-1, 0):
                                             {"white": Direction(-1, 1),
                                              "black": Direction(-1, -1)
                                              },
                                         Direction(1, 0):
                                             {"white": Direction(1, 1),
                                              "black": Direction(1, -1)
                                              }
                                         }
                for pawn_check_direction, capture_direction_dict in en_passant_directions.items():
                    potential_captured_pawn_square = piece.square.next_square_in_direction(pawn_check_direction)
                    if potential_captured_pawn_square and potential_captured_pawn_square == self.en_passant_target.square:
                        legal_moves[piece].add(Move(self, piece, piece.square.next_square_in_direction(capture_direction_dict[piece.color]), is_en_passant=True))

            for square in accessible_squares:
                # Records two-pawn advances for en passant
                if piece.type == "Pawn" and abs(piece.square.row - square.row) == 2:
                    legal_moves[piece].add(Move(self, piece, square, is_two_pawn_move=True))
                # Promotion of pawns
                elif piece.type == "Pawn" and square.row in [0, 7]:
                    for string in ["Knight", "Bishop", "Rook", "Queen"]:
                        legal_moves[piece].add(Move(self, piece, square, is_promotion=True, promoting_piece_str=string))
                else:
                    legal_moves[piece].add(Move(self, piece, square))

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
                    self.place_piece(piece.color, piece.type, piece.square)

    def place_piece(self, color: str, piece_type: str, square: str | Square) -> Piece:
        if isinstance(square, str):
            square = self.square_by_name[square]
        elif isinstance(square, Square):
            square = self.square_by_name[square.name]
        assert isinstance(square, Square), "Wrong argument type passed in Position.place_piece()"
        piece = square.place(color, piece_type)
        self.pieces[color][piece_type].add(piece)
        self.legal_moves_ = None
        return piece

    def remove_piece(self, square: str | Square):
        if isinstance(square, str):
            square = self.square_by_name[square]
        elif isinstance(square, Square):
            square = self.square_by_name[square.name]
        assert isinstance(square, Square), "Wrong argument type passed in Position.remove_piece()"
        self.legal_moves_ = None
        return square.remove_piece()

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

    def make_move(self, move_or_notation: Move | str, language="English") -> tuple["Position", Move]:
        if isinstance(move_or_notation, Move):
            assert move_or_notation.is_legal_move(), "Illegal move passed to make_move()"
            ###Castling rights update
            updated_castling_rights = self._update_castling_rights(move_or_notation)
            new_position = Position(self.pieces, whose_move=self.not_turn_to_move, castling_rights=updated_castling_rights)
            # Step 1 : Remove the moved piece from its original square
            new_position.remove_piece(move_or_notation.start_square)
            # Step 2 : Remove captured piece if there is one
            if move_or_notation.is_capture():
                if move_or_notation.is_en_passant:
                    new_position.remove_piece(self.en_passant_target.square)
                else:
                    new_position.remove_piece(move_or_notation.end_square)
            # Step 3 : Place a new instance of the moved piece on the end square
            if move_or_notation.is_promotion:
                piece = new_position.place_piece(move_or_notation.piece.color, move_or_notation.promoting_piece_str, move_or_notation.end_square)
            else:
                piece = new_position.place_piece(move_or_notation.piece.color, move_or_notation.piece.type, move_or_notation.end_square)
            if move_or_notation.is_castling:
                new_position.remove_piece(move_or_notation.rook_start)
                new_position.place_piece(move_or_notation.piece.color, "Rook", move_or_notation.rook_end)
            if move_or_notation.is_two_pawn_move:
                new_position.en_passant_target = piece

            move_or_notation.base_notation = move_or_notation.compute_base_notation(language=language)
            # Append + sign if check identified
            if new_position.king_in_check(next(iter(new_position.pieces[new_position.whose_move]["King"]))):
                move_or_notation.is_check = True
            move_or_notation.update_full_notation()
            return new_position, move_or_notation

        if isinstance(move_or_notation, str):
            # Normalize incoming notation (remove + or #)
            normalized_input = move_or_notation.rstrip("+#")

            legal_moves = self.legal_moves_

            for piece, moves in legal_moves.items():
                for move in moves:
                    base_notation = move.compute_base_notation(language)
                    if base_notation == normalized_input:
                        return self.make_move(move, language)

            raise ValueError(f"No legal move matches notation '{move_or_notation}' in {language}")

    def _update_castling_rights(self, move: "Move") -> dict:
        updated_castling_rights = self.castling_rights.copy()
        starting_rook_squares = {"h1": "white_kingside",
                                 "a1": "white_queenside",
                                 "h8": "black_kingside",
                                 "a8": "black_queenside"}
        # Rule 1 : King moves, both kingside and queenside castles are disabled for the corresponding color
        if move.piece.type == "King":
            updated_castling_rights[f"{move.piece.color}_kingside"] = False
            updated_castling_rights[f"{move.piece.color}_queenside"] = False
        # Rule 2 : Rook moves from its starting square, corresponding castle is disabled
        if move.piece.type == "Rook" and move.start_square.name in starting_rook_squares.keys():
            updated_castling_rights[starting_rook_squares[move.start_square.name]] = False
        # Rule 3 : Any piece ends its turn on one of the rook starting squares, corresponding castle is disabled
        if move.end_square.name in starting_rook_squares.keys():
            updated_castling_rights[starting_rook_squares[move.end_square.name]] = False
        return updated_castling_rights
