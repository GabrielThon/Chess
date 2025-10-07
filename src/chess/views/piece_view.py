from src.chess.models.pieces import Piece
import pygame
from pathlib import Path

class PieceView:
    def __init__(self, piece : Piece):
        self.piece = piece
        image_path = Path(__file__).resolve().parent.parent / "images" / f"{piece.type}_{piece.color}.png"
        self.image = pygame.image.load(image_path).convert_alpha()

    def draw(self, screen, x, y, square_width, square_height, offset_x = 0, offset_y = 0):
        width = square_width - 2 * offset_x
        height = square_height - 2 * offset_y
        image_scaled = pygame.transform.scale(self.image, (width, height))
        screen.blit(image_scaled, (x + offset_x, y + offset_y))