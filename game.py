import os
import time

import pygame

from board import Board
from piece import Piece


class Game:
    def __init__(self, board: Board, screen_size: tuple[int, int]):
        self.screen = None
        self.images = None
        self.board = board
        self.screen_size = screen_size
        self.piece_size = (self.screen_size[0] // self.board.get_size()[1],
                           self.screen_size[1] // self.board.get_size()[0])
        self.load_images()

    def run(self) -> None:
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode(self.screen_size)
        pygame.display.set_caption("Minesweeper")
        pygame.display.set_icon(pygame.image.load(
            "assets/images/bomb-at-clicked-block.png"))

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    position = pygame.mouse.get_pos()
                    print(position)
                    right_click = pygame.mouse.get_pressed()[2]
                    self.handle_click(position, right_click)
            self.draw()
            pygame.display.flip()
            if self.board.get_won():
                sound = pygame.mixer.Sound("assets/sounds/win.wav")
                sound.play()
                time.sleep(3)
                running = False
        pygame.quit()

    def draw(self):
        top_left = (0, 30)

        for row in range(self.board.get_size()[0]):
            for col in range(self.board.get_size()[1]):
                piece = self.board.get_piece((row, col))
                image = self.get_image(piece)
                self.screen.blit(image, top_left)
                top_left = top_left[0] + self.piece_size[0], top_left[1]
            top_left = 0, top_left[1] + self.piece_size[1]

    def load_images(self) -> None:
        self.images = {}
        for filename in os.listdir("assets/images"):
            if not filename.endswith("png"):
                continue
            image = pygame.image.load(r"assets/images/" + filename)
            image = pygame.transform.scale(image, self.piece_size)
            self.images[filename.split('.')[0]] = image

    def get_image(self, piece: Piece):
        string = None
        if piece.get_clicked():
            string = "bomb-at-clicked-block" if piece.get_has_bomb() else str(piece.get_num_around())
        else:
            string = "flag" if piece.get_flagged() else "empty-block"

        if self.board.get_lost():
            string = ("bomb-at-clicked-block" if piece.get_has_bomb() else
                      str(piece.get_num_around()) if piece.get_clicked() else
                      "flag" if piece.get_flagged() else "empty-block")
        if self.board.get_won():
            string = "unclicked-bomb" if piece.get_has_bomb() and not piece.get_clicked() else str(
                piece.get_num_around())
        return self.images[string]

    def handle_click(self, position, right_click: bool):
        if self.board.get_lost():
            return
        if position[1] < 30:
            return

        index = ((position[1] // self.piece_size[1]) - 1,
                 position[0] // self.piece_size[0])
        piece = self.board.get_piece(index)
        self.board.handle_click(piece, right_click)
