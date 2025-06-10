import pygame
from src.models.game import Game
from src.views.board_view import BoardView
from src.views.piece_view import PieceView
from src.models.utils import starting_position

WINDOW_SIZE = (400,400)
pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Chessboard")

# board = Position([])
# board.place_piece("white", "Knight", "b1")
# boardview = BoardView(board, screen)

game = Game()
boardview = BoardView(game.current_position, screen)

clock = pygame.time.Clock()
running = True
dragging_piece = None
needs_redraw = True

while running:
    selected_piece = None
    valid_squares = set()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            column = x // boardview.square_width
            row = y // boardview.square_height

            piece = game.current_position.get_piece(clicked_square)
            pass
            # dragging_piece = board.try_pick_piece(event.pos)
            # needs_redraw = True

        elif event.type == pygame.MOUSEBUTTONUP:
            pass
            # if dragging_piece:
            #     board.try_drop_piece(dragging_piece, event.pos)
            #     dragging_piece = None
            #     needs_redraw = True

        elif event.type == pygame.MOUSEMOTION:
            pass
            # if dragging_piece:
            #     dragging_piece.update_position(event.pos)
            #     needs_redraw = True

    if needs_redraw:
        boardview.draw(screen)
        pygame.display.flip()
        needs_redraw = False

    clock.tick(60)

pygame.quit()