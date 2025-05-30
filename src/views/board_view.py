from src.models.board import Board
import pygame

from src.views.piece_view import PieceView


class BoardView:
    def __init__(self, board : Board, screen):
        self.board = board
        self.screen = screen
        self.piece_views = {}
        self._create_piece_views()

    def _create_piece_views(self):
        for piece in self.board.all_pieces.values():
            piece_view = PieceView(piece)
            self.piece_views[piece.current_square.name] = piece_view

    @property
    def number_of_columns(self):
        return len(self.board.columns)

    @property
    def number_of_rows(self):
        return len(self.board.rows)

    @property
    def square_width(self):
        return self.screen.get_size()[0] // self.number_of_columns

    @property
    def square_height(self):
        return self.screen.get_size()[1] // self.number_of_rows

    def draw(self, screen, white = (255, 255, 255), grey = (180, 180, 180)):
        for row in range(self.number_of_rows):
            for column in range(self.number_of_columns):
                color = white if (row + column) % 2 == 0 else grey
                pygame.draw.rect(screen, color, (column * self.square_width, row * self.square_height, self.square_width, self.square_height))

        for piece_view in self.piece_views.values():
            piece = piece_view.piece
            x = piece.current_square.column * self.square_width
            y = (self.number_of_rows - piece.current_square.row - 1) * self.square_height
            piece_view.draw(self.screen, x, y, self.square_width, self.square_height)

            # offset_x = self.square_width * 0.1
            # offset_y = self.square_height * 0.1
            # piece_view.draw(self.screen, x, y, self.square_width, self.square_height, offset_x=offset_x, offset_y=offset_y)


