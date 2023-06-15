from colorama import init, Fore, Back, Style

class TextColored:
    def __init__(self, text, color) -> None:
        self.color = color
        self.text = text
    def __str__(self) -> str:
        return str(self.color + self.text)

class ChessPiece:
    def __init__(self, type_, pos, color) -> None:
        self.color = color 
        self.pos = pos 
        self.possiblemoves = None
        self.type = type_
        self.played = False
    def change_pos(self, pos):
        self.played = True
        self.pos = pos   
    def checkboard(self, chessboard, pos):
        for piece in chessboard:
            if pos == piece.pos:
                return piece
        return None   
    def addpossiblemove(self, chessboard, pos):
        piece = self.checkboard(chessboard, pos)
        if piece != None:
            if piece.color != self.color:
                self.possiblemoves.append(piece.pos)
            return True
        else:
            self.possiblemoves.append(pos)
            return False
    def inchessboard(self, pos):
        return (pos[0] < 8) and (pos[0] > -1) and (pos[1] < 8) and (pos[1] > -1)
    def get_color_text(self):
        if self.color == "White":
            return Fore.GREEN
        else:
            return Fore.MAGENTA

class Rook(ChessPiece): 
    def __init__(self, pos, color) -> None:
        super().__init__("Rook", pos, color)
        self.str = TextColored("R", self.get_color_text())
    def way(self, pos, dx, dy, chessboard):
        npos = [pos[0]+dx, pos[1]+dy]
        if self.inchessboard(npos):
            if self.addpossiblemove(chessboard, npos):
                return
            else:
                self.way(npos, dx, dy, chessboard)
    def update_pos(self, chessboard):
        self.possiblemoves = []
        self.way(self.pos, 1, 0, chessboard)
        self.way(self.pos, -1, 0, chessboard)
        self.way(self.pos, 0, 1, chessboard)
        self.way(self.pos, 0, -1, chessboard)
    def __str__(self) -> str:
        return str(self.str)

class Bishop(ChessPiece): 
    def __init__(self, pos, color) -> None:
        super().__init__("Bishop", pos, color)
        self.str = TextColored("B", self.get_color_text())

    def __str__(self) -> str:
        return str(self.str)

    def way(self, pos, dx, dy, chessboard):
        npos = [pos[0]+dx, pos[1]+dy]
        if self.inchessboard(npos):
            if self.addpossiblemove(chessboard, npos):
                return
            else:
                self.way(npos, dx, dy, chessboard)

    def update_pos(self, chessboard):
        self.possiblemoves = []
        self.way(self.pos, 1, 1, chessboard)
        self.way(self.pos, 1, -1, chessboard)
        self.way(self.pos, -1, 1, chessboard)
        self.way(self.pos, -1, -1, chessboard)

class Knight(ChessPiece): 
    def __init__(self, pos, color) -> None:
        super().__init__("Knight", pos, color)
        self.str = TextColored("N", self.get_color_text())
    def __str__(self) -> str:
        return str(self.str)
    def way(self, chessboard, dx, dy):
        pos = [self.pos[0]+dx, self.pos[1]+dy]
        if self.inchessboard(pos):
            self.addpossiblemove(chessboard, pos)
    def update_pos(self, chessboard):
        self.possiblemoves = []
        self.way(chessboard, 1, 2)
        self.way(chessboard, -1, 2)
        self.way(chessboard, 1, -2)
        self.way(chessboard, -1, -2)
        self.way(chessboard, 2, 1)
        self.way(chessboard, 2, -1)
        self.way(chessboard, -2, 1)
        self.way(chessboard, -2, -1)
        
class Pawn(ChessPiece): 
    def __init__(self, pos, color) -> None:
        super().__init__("Pawn", pos, color)
        self.str = TextColored("P", self.get_color_text())
    def __str__(self) -> str:
        return str(self.str)
    def way(self, chessboard, dx, dy, isitattack = False):
        pos = [self.pos[0] +dx, self.pos[1]+dy]
        if self.inchessboard(pos):
            if isitattack:
                self.attack(chessboard, pos)
                return
            self.addpossiblemove(chessboard, pos)
    def addpossiblemove(self, chessboard, pos):
        piece = self.checkboard(chessboard, pos)
        if piece == None:
            self.possiblemoves.append(pos)
    def attack(self, chessboard, pos):
        piece = self.checkboard(chessboard, pos)
        if piece != None:
            if piece.color != self.color:
                self.possiblemoves.append(piece.pos)
    def update_pos(self, chessboard):
        self.possiblemoves = []
        if self.played == False:
            self.way(chessboard, 2, 0)
        self.way(chessboard, 1, 0)
        self.way(chessboard, 1, 1, True)
        self.way(chessboard, 1, -1, True)
    def change_pos(self, pos):
        self.played = True
        return super().change_pos(pos)

class King(ChessPiece): 
    def __init__(self, pos, color) -> None:
        super().__init__("King", pos, color)
        self.str = TextColored("K", self.get_color_text())
    def __str__(self) -> str:
        return str(self.str)
    def way(self, chessboard, dx, dy):
        pos = [self.pos[0]+dx, self.pos[1]+dy]
        if self.inchessboard(pos):
            self.addpossiblemove(chessboard, pos)
    def update_pos(self, chessboard, attackedplaces):
        self.possiblemoves = []
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if i==0 and j==0:
                    continue
                else:
                    self.way(chessboard, i, j)
        for move in self.possiblemoves:
            if move in attackedplaces:
                self.possiblemoves.remove(move)

class Queen(ChessPiece): 
    def __init__(self, pos, color) -> None:
        super().__init__("Queen", pos, color) 
        self.str = TextColored("Q", self.get_color_text())

    def __str__(self) -> str:
        return str(self.str)
    def way(self, pos, dx, dy, chessboard):
        npos = [pos[0]+dx, pos[1]+dy]
        if self.inchessboard(npos):
            if self.addpossiblemove(chessboard, npos):
                return
            else:
                self.way(npos, dx, dy, chessboard)
    def update_pos(self, chessboard):
        self.possiblemoves = []
        self.way(self.pos, 1, 0, chessboard)
        self.way(self.pos, -1, 0, chessboard)
        self.way(self.pos, 0, 1, chessboard)
        self.way(self.pos, 0, -1, chessboard)
        self.way(self.pos, 1, 1, chessboard)
        self.way(self.pos, -1, 1, chessboard)
        self.way(self.pos, 1, -1, chessboard)
        self.way(self.pos, -1, -1, chessboard)

class ChessGame:
    def __init__(self) -> None:
        init(autoreset=True)
        self.pieces = self.initial_pieces()
        self.attackedplacesbyblack = []
        self.attackedplacesbywhite = []
        self.checkmate = None
        self.check = None

    def initial_pieces(self):
        p = []
        for i in range(8):
            p.append(Pawn([1, i], "White"))
            p.append(Pawn([6, i], "Black"))
        
        p.append(Rook([0, 0], "White"))
        p.append(Rook([0, 7], "White"))
        p.append(Rook([7, 0], "Black"))
        p.append(Rook([7, 7], "Black"))

        p.append(Knight([0, 1], "White"))
        p.append(Knight([0, 6], "White"))
        p.append(Knight([7, 1], "Black"))
        p.append(Knight([7, 6], "Black"))

        p.append(Bishop([0, 2], "White"))
        p.append(Bishop([0, 5], "White"))
        p.append(Bishop([7, 2], "Black"))
        p.append(Bishop([7, 5], "Black"))

        p.append(Queen([4,3], "White"))
        p.append(Queen([7,3], "Black"))

        p.append(King([0,4], "White"))
        p.append(King([7,4], "Black"))

        return p

    def update_pieces(self, place_initial, place_final):
        self.attackedplacesbyblack = []
        self.attackedplacesbywhite = []
        for piece in self.pieces:
            if piece.type != "King":
                piece.update_pos(self.pieces)
                a = piece.possiblemoves
                if piece.color == "Black":
                    self.attackedplacesbyblack.extend(a)
                else:
                    self.attackedplacesbywhite.extend(a)
        for piece in self.pieces:
            if piece.type == "King":
                if piece.color == "Black":
                    piece.update_pos(self.pieces, self.attackedplacesbywhite)
                else:
                    piece.update_pos(self.pieces, self.attackedplacesbyblack)

        #move piece

        #update non King Pieces
        #get all attacked places
        #update king pieces
        #check checkamte/check
        pass

    def generate_matrix(self):
        matrix = [[TextColored("-", Fore.WHITE) for i in range(8)] for j in range(8)]
        for piece in self.pieces:
            x = piece.pos[0]
            y = piece.pos[1]
            matrix[x][y] = piece.str
        return matrix

    def print_matrix(self, matrix):
        string = Fore.WHITE + "  01234567\n"
        for i in range(7,-1, -1):
            string += Fore.WHITE + str(i) + " "
            for j in range(8):
                string += str(matrix[i][j])
            string += "\n"
        return string

    def __str__(self) -> str:
        matrix = self.generate_matrix()
        return self.print_matrix(matrix)
        
    def search(self, pos):
        for i, piece in enumerate(self.pieces):
            if piece.pos == pos:
                return i
        return -1

    def print_posmove(self, pos):
        matrix = self.generate_matrix()
        result = self.search(pos)
        if result != -1:
            for move in self.pieces[result].possiblemoves:
                px = move[0]
                py = move[1]
                #print(move)
                matrix[px][py].color = Fore.BLUE
        print(self.print_matrix(matrix))

init(autoreset=True)
chess = ChessGame()
print(chess)

chess.update_pieces(0, 0)
chess.print_posmove([4, 3])
#chess.print_posmove([0, 1])

