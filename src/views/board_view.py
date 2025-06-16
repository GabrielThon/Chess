from typing import TYPE_CHECKING

from src.models.pieces import Queen, Rook, Bishop, Knight
from src.models.position import Position
import pygame

from src.views.piece_view import PieceView

if TYPE_CHECKING:
    from src.models.square import Square


class BoardView:
    def __init__(self, position: Position, screen):
        self.position = position
        self.screen = screen
        self.piece_views = {}
        self._create_piece_views()

    def _create_piece_views(self):
        for piece in self.position.all_pieces:
            piece_view = PieceView(piece)
            self.piece_views[piece.square.name] = piece_view

    @property
    def number_of_columns(self):
        return len(self.position.grid)

    @property
    def number_of_rows(self):
        return len(self.position.grid[0])

    @property
    def square_width(self):
        return self.screen.get_size()[0] // self.number_of_columns

    @property
    def square_height(self):
        return self.screen.get_size()[1] // self.number_of_rows

    def draw(self, screen, white=(255, 255, 255), grey=(180, 180, 180), highlights=None):
        for row in range(self.number_of_rows):
            for column in range(self.number_of_columns):
                square = self.position.grid[column][row]
                color = white if (row + column) % 2 == 0 else grey
                if highlights and square in highlights:
                    color = (100, 255, 100)  # light green highlight
                pygame.draw.rect(screen, color, (column * self.square_width, (self.number_of_rows - 1 - row) * self.square_height, self.square_width, self.square_height))

        for piece_view in self.piece_views.values():
            piece = piece_view.piece
            x, y = self.get_square_coordinates(piece.square)
            piece_view.draw(self.screen, x, y, self.square_width, self.square_height)

            # offset_x = self.square_width * 0.1
            # offset_y = self.square_height * 0.1
            # piece_view.draw(self.screen, x, y, self.square_width, self.square_height, offset_x=offset_x, offset_y=offset_y)

    def get_square_from_pixel(self, x, y) -> "Square":
        column = x // self.square_width
        row = self.number_of_rows - 1 - (y // self.square_height)
        return self.position.grid[column][row]

    def get_square_coordinates(self, square: "Square") -> tuple[int, int]:
        return square.column * self.square_width, (self.number_of_rows - square.row - 1) * self.square_height

    def show_promotion_menu(self, square) -> str:
        piece_views = [PieceView(Queen(self.position.whose_move)),
                       PieceView(Rook(self.position.whose_move)),
                       PieceView(Bishop(self.position.whose_move)),
                       PieceView(Knight(self.position.whose_move))]
        rects = []
        x, y = self.get_square_coordinates(square)
        color = (100, 255, 100)
        for i, piece_view in enumerate(piece_views):
            rect = pygame.Rect(x + i * self.square_width, y, self.square_width, self.square_height)
            pygame.draw.rect(self.screen, color, rect)
            piece_view.draw(self.screen, x + i * self.square_width, y, self.square_width, self.square_height)
            rects.append((rect, piece_view.piece.type))

            pygame.display.update()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = pygame.mouse.get_pos()
                    for rect, piece_type in rects:
                        if rect.collidepoint((mx, my)):
                            return piece_type
