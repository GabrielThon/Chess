import pygame
from src.chess.models.game import Game
from src.chess.views.board_view import BoardView

WINDOW_SIZE = (400,400)
pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Chessboard")

# position = Position([])
# position.place_piece("white", "Knight", "b1")
# boardview = BoardView(position, screen)

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
                clicked_square = game.current_position.grid[column][row]

                piece = clicked_square.piece
                if selected_piece is None:
                    # First click: try to select a piece
                    if piece and piece.color == game.current_position.whose_move:
                        selected_piece = piece
                        valid_moves = game.current_position.legal_moves_.get(piece, set())
                        valid_squares = {valid_move.end_square for valid_move in valid_moves}
                        if not valid_moves:
                            print(f"{repr(selected_piece)} cannot move")
                            selected_piece = None
                            continue
                        needs_redraw = True
                else:
                    # Second click: try to make a move
                    if clicked_square in valid_squares:
                        valid_moves = game.current_position.legal_moves_.get(selected_piece, set())
                        corresponding_moves = {valid_move for valid_move in valid_moves if valid_move.end_square == clicked_square}
                        if len(corresponding_moves) == 1:
                            apply_move = game.apply_move(next(iter(corresponding_moves)))
                        else: # Promotion handling
                            promotion_choice = boardview.show_promotion_menu(clicked_square)
                            move = {move for move in corresponding_moves if move.promoting_piece_str == promotion_choice}
                            apply_move = game.apply_move(next(iter(move)))
                        if not game.result:
                            print(f"Now it's {game.current_position.whose_move}'s turn")

                        # Update boardview with new position
                        boardview = BoardView(game.current_position, screen)

                    # Reset selection either way
                    selected_piece = None
                    valid_squares = set()
                    needs_redraw = True

            # dragging_piece = position.try_pick_piece(event.pos)
            # needs_redraw = True

        # elif event.type == pygame.MOUSEBUTTONUP:
        #     pass
        #     # if dragging_piece:
        #     #     position.try_drop_piece(dragging_piece, event.pos)
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