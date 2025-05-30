import pygame
from src.models.board import Board
from src.views.board_view import BoardView
from src.views.piece_view import PieceView

WINDOW_SIZE = (400,400)
pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Chessboard")

# board = Board.create_empty_board()
# knight = board.place("white","Knight", "b1")

board = Board()
boardview = BoardView(board, screen)

clock = pygame.time.Clock()
running = True
dragging_piece = None
needs_redraw = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
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