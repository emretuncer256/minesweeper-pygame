class Piece:
    def __init__(self, has_bomb: bool):
        self.has_bomb = has_bomb
        self.around = 0
        self.clicked = False
        self.flagged = False
        self.neighbors: list[Piece] = []

    def __str__(self):
        return str(self.has_bomb)

    def get_has_bomb(self) -> bool:
        return self.has_bomb

    def get_clicked(self) -> bool:
        return self.clicked

    def get_flagged(self) -> bool:
        return self.flagged

    def toggle_flag(self):
        self.flagged = not self.flagged

    def set_neighbors(self, neighbors):
        self.neighbors = neighbors
        self.set_num_around()

    def get_neighbors(self):
        return self.neighbors

    def set_num_around(self):
        num = 0
        for neighbor in self.neighbors:
            if neighbor.get_has_bomb():
                num += 1
        self.around = num

    def get_num_around(self):
        return self.around

    def click(self):
        self.clicked = True
