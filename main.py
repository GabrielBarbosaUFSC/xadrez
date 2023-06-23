from classes import *
from interface import *
chess = ChessGame()
chess.up_move(0, 0, False)
game = ChessGameGUI(chess)
game.run()