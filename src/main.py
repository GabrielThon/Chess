import pygame
from src.models.game import Game
from src.models.move import Move
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
# dragging_piece = None
needs_redraw = True
selected_piece = None
valid_squares = set()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if not game.result:
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                column = x // boardview.square_width
                row = boardview.number_of_rows - 1 - (y // boardview.square_height)
                # row = boardview.number_of_rows - 1 - (y // boardview.square_height)
                clicked_square = game.current_position.grid[column][row]

                piece = clicked_square.piece
                if selected_piece is None:
                    # First click: try to select a piece
                    if piece and piece.color == game.current_position.whose_move:
                        selected_piece = piece
                        valid_squares = game.current_position.legal_moves_.get(piece, set())
                        if not valid_squares:
                            print(f"{repr(selected_piece)} cannot move")
                            selected_piece = None
                            continue
                        needs_redraw = True
                else:
                    # Second click: try to make a move
                    if clicked_square in valid_squares:
                        to_square = clicked_square
                        move = Move(game.current_position, selected_piece, to_square)
                        game.apply_move(move)
                        if not game.result:
                            print(f"Now it's {game.current_position.whose_move}'s turn")

                        # Update boardview with new position
                        boardview = BoardView(game.current_position, screen)

                    # Reset selection either way
                    selected_piece = None
                    valid_squares = set()
                    needs_redraw = True

            # dragging_piece = board.try_pick_piece(event.pos)
            # needs_redraw = True

        # elif event.type == pygame.MOUSEBUTTONUP:
        #     pass
        #     # if dragging_piece:
        #     #     board.try_drop_piece(dragging_piece, event.pos)
        #     #     dragging_piece = None
        #     #     needs_redraw = True
        #
        # elif event.type == pygame.MOUSEMOTION:
        #     pass
        #     # if dragging_piece:
        #     #     dragging_piece.update_position(event.pos)
        #     #     needs_redraw = True

    if needs_redraw:
        boardview.draw(screen, highlights=valid_squares)
        pygame.display.flip()
        needs_redraw = False

    clock.tick(60)

pygame.quit()