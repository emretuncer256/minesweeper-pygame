from random import random
from pygame.mixer import Channel, Sound
from piece import Piece


class Board:
    def __init__(self, size: tuple[int, int], prob: float):
        self.board = None
        self.size = size
        self.prob = prob
        self.lost = False
        self.num_clicked = 0
        self.num_non_bombs = 0
        self.num_bombs = 0
        self.set_board()

    def set_board(self):
        self.board = []
        for row in range(self.size[0]):
            row = []
            for col in range(self.size[1]):
                has_bomb = random() < self.prob
                if not has_bomb:
                    self.num_non_bombs += 1
                piece = Piece(has_bomb)
                row.append(piece)
            self.board.append(row)

        self.num_bombs = (self.size[0] * self.size[1]) - self.num_non_bombs
        self.set_neighbors()

    def set_neighbors(self):
        for row in range(self.size[0]):
            for col in range(self.size[1]):
                piece = self.get_piece((row, col))
                neighbors = self.get_list_of_neighbors((row, col))
                piece.set_neighbors(neighbors)

    def get_list_of_neighbors(self, index: tuple[int, int]) -> list:
        neighbors = []
        for row in range(index[0] - 1, index[0] + 2):
            for col in range(index[1] - 1, index[1] + 2):
                out_of_bounds = row < 0 or row >= self.size[0] or col < 0 or col >= self.size[1]
                same = row == index[0] and col == index[1]
                if same or out_of_bounds:
                    continue
                neighbors.append(self.get_piece((row, col)))
        return neighbors

    def get_size(self) -> tuple[int, int]:
        return self.size

    def get_piece(self, index: tuple[int, int]):
        return self.board[index[0]][index[1]]

    def handle_click(self, piece: Piece, flag: bool):
        if piece.get_clicked() or (not flag and piece.get_flagged()):
            return
        if flag:
            piece.toggle_flag()
            Channel(1).play(Sound("assets/sounds/flag.wav"))
            return

        piece.click()
        Channel(0).play(Sound("assets/sounds/open-block.wav"))
        if piece.get_has_bomb():
            self.lost = True
            Channel(2).play(Sound("assets/sounds/bomb.wav"), maxtime=4000)
            return

        self.num_clicked += 1
        if piece.get_num_around() != 0:
            return
        for neighbor in piece.get_neighbors():
            if not neighbor.get_has_bomb() and not neighbor.get_clicked():
                self.handle_click(neighbor, False)

    def get_lost(self) -> bool:
        return self.lost

    def get_won(self) -> bool:
        return self.num_non_bombs == self.num_clicked
