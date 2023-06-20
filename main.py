from pieces import *
from interface import *

chess = ChessGame()
print("------------------------")
print("------------------------")
print(chess)
chess.up_move(0, 0, False)
#game = ChessGameGUI(chess)
#game.run()

text = "m0000 or p00: "
while True:
    print(chess.turn)
    in_ = str(input(text))
    if in_[0] == "m":
        x1 = int(in_[1])
        y1 = int(in_[2])
        x2 = int(in_[3])
        y2 = int(in_[4])
        chess.up_move([x1, y1], [x2, y2])
        print(chess)
    elif in_[0] == "p":
        x = int(in_[1])
        y = int(in_[2])
        chess.print_pos_move([x,y])
    print("------------------------")
    print("------------------------")

