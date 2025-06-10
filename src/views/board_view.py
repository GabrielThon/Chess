from src.models.position import Position
import pygame

from src.views.piece_view import PieceView


class BoardView:
    def __init__(self, board : Position, screen):
        self.board = board
        self.screen = screen
        self.piece_views = {}
        self._create_piece_views()

    def _create_piece_views(self):
        for piece in self.board.all_pieces:
            piece_view = PieceView(piece)
            self.piece_views[piece.square.name] = piece_view

    @property
    def number_of_columns(self):
        return len(self.board.grid)

    @property
    def number_of_rows(self):
        return len(self.board.grid[0])

    @property
    def square_width(self):
        return self.screen.get_size()[0] // self.number_of_columns

    @property
    def square_height(self):
        return self.screen.get_size()[1] // self.number_of_rows

    def draw(self, screen, white = (255, 255, 255), grey = (180, 180, 180), highlights=None):
        for row in range(self.number_of_rows):
            for column in range(self.number_of_columns):
                square = self.board.grid[column][row]
                color = white if (row + column) % 2 == 0 else grey
                if highlights and square in highlights:
                    color = (100, 255, 100)  # light green highlight
                pygame.draw.rect(screen, color, (column * self.square_width, (self.number_of_rows - 1 - row) * self.square_height, self.square_width, self.square_height))

        for piece_view in self.piece_views.values():
            piece = piece_view.piece
            x = piece.square.column * self.square_width
            y = (self.number_of_rows - piece.square.row - 1) * self.square_height
            piece_view.draw(self.screen, x, y, self.square_width, self.square_height)

            # offset_x = self.square_width * 0.1
            # offset_y = self.square_height * 0.1
            # piece_view.draw(self.screen, x, y, self.square_width, self.square_height, offset_x=offset_x, offset_y=offset_y)


