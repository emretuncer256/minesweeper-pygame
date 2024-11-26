from board import Board
from game import Game

size = (20, 20)
prob = 0.09

board = Board(size, prob)
screen_size = (600, 600)
app = Game(board, screen_size)

print("Game initializing with:")
print(f"Size: {board.get_size()}")
print(f"Mines: {board.num_bombs}")

app.run()
