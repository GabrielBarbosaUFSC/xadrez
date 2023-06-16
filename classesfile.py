from colorama import init, Fore

class ColoredText:
    def __init__(self, text, color) -> None:
        self.color = color
        self.text = text
    def __str__(self) -> str:
        return str(self.color + self.text)

class ChessPiece:
    def __init__(self, type_, pos, color, symbol):
        self.color = color
        self.pos = pos
        self.moves = None
        self.type = type_
        self.played = False
        self.str = ColoredText(symbol, self.get_color_text())
    
    def change(self, new_pos):
        self.played = True
        self.pos = new_pos
    
    def check(self, piece_matrix, pos):
        return piece_matrix[pos[0]][pos[1]]
    
    def addmove(self, piece_matrix, pos):
        piece = self.check(piece_matrix, pos)
        if piece != None:
            if piece.color != self.color:
                self.moves.append(pos)
            return True
        else:
            self.moves.append(pos)
            return False
    
    def inboard(self, pos):
        in_ = True
        in_ &= (pos[0] < 8)
        in_ &= (pos[0] > -1)
        in_ &= (pos[1] < 8)
        in_ &= (pos[1] > -1)
        return in_
    
    def get_color_text(self):
        if self.color == "White":
            return Fore.GREEN
        else:
            return Fore.MAGENTA
    
    def way(self, pos, dx, dy, piece_matrix):
        npos = [pos[0]+dx, pos[1]+dy]
        if self.inboard(npos):
            if self.addmove(piece_matrix, npos):
                return
            else:
                self.way(npos, dx, dy, piece_matrix) 
    
    def __str__(self) -> str:
        return str(self.str)

class Rook(ChessPiece):
    def __init__(self, pos, color):
        super().__init__("Rook", pos, color, "R")
    
    def up_move(self, piece_matrix):
        self.moves = []
        moves = [[1, 0], [-1, 0], [0, -1], [0, 1]]
        for move in moves:
            self.way(self.pos,  move[0],  move[1], piece_matrix)

class Bishop(ChessPiece):
    def __init__(self, pos, color):
        super().__init__("Bishop", pos, color, "B")
    
    def up_move(self, piece_matrix):
        self.moves = []
        moves = [[1, 1], [1, -1], [-1, 1], [-1, -1]]
        for move in moves:
            self.way(self.pos,  move[0],  move[1], piece_matrix)

class Knight(ChessPiece):
    def __init__(self, pos, color):
        super().__init__("Knight", pos, color, "N")
    
    def way(self, dx, dy, piece_matrix):
        npos = [self.pos[0]+dx, self.pos[1]+dy]
        if self.inboard(npos):
            self.addmove(piece_matrix, npos)       
    
    def up_move(self, piece_matrix):
        self.moves = []
        moves = [[1, 2], [-1, 2], [1, -2], [-1, -2], [2, 1], [2,-1], [-2,1], [-2, -1]]
        for move in moves:
                self.way(move[0], move[1], piece_matrix) 

class Pawn(ChessPiece):
    def __init__(self, pos, color):
        super().__init__("Pawn", pos, color, "P")

    def way(self, dx, dy, piece_matrix, attack = False):
        pos = [self.pos[0] +dx, self.pos[1]+dy]
        if self.inboard(pos):
            if attack:
                self.attack(piece_matrix, pos)
                return
            self.addmove(piece_matrix, pos)

    def addmove(self, piece_matrix, pos):
        piece = self.check(piece_matrix, pos)
        if piece == None:
            self.moves.append(pos)

    def attack(self, piece_matrix, pos):
        piece = self.check(piece_matrix, pos)
        if piece != None:
            if piece.color != self.color:
                self.moves.append(piece.pos)

    def up_move(self, piece_matrix):
        self.moves = []
        invert = 1
        if self.color != "White":
            invert = -1
        if not self.played:
            self.way(2*invert, 0, piece_matrix)
        self.way(1*invert, 0, piece_matrix)
        self.way(1*invert, 1, piece_matrix ,True)
        self.way(1*invert, -1, piece_matrix ,True)

class King(ChessPiece):
    def __init__(self, pos, color):
        super().__init__("King", pos, color, "K")

    def way(self, dx, dy, piece_matrix):
        pos = [self.pos[0]+dx, self.pos[1]+dy]
        if self.inboard(pos):
            self.addmove(piece_matrix, pos)

    def up_move(self, piece_matrix, attackedplaces):
        self.moves = []
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if i==0 and j ==0:
                    continue
                else:
                    self.way(i, j, piece_matrix)
        for move in self.moves:
            if move in attackedplaces:
                self.moves.remove(move)

class Queen(ChessPiece):
    def __init__(self, pos, color):
        super().__init__("Queen", pos, color, "Q")

    def up_move(self, piece_matrix):
        self.moves = []
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if i==0 and j ==0:
                    continue
                else:
                    self.way(self.pos, i, j, piece_matrix)

class ChessGame:
    def __init__(self) -> None:
        init(autoreset=True)
        self.initial_pieces()  
        self.attackedplacesbyblack = []
        self.attackedplacesbywhite = []
        self.turn = "White"

    def replace (self, new_piece, pos_ = None):
        if new_piece != None:
            pos = new_piece.pos
            self.piece_matrix[pos[0]][pos[1]] = new_piece
        else:
            self.piece_matrix[pos_[0], pos_[1]] = None

    def move (self, ipos, fpos):
        if fpos in self.piece_matrix[ipos[0]][ipos[1]].moves:
            self.piece_matrix[fpos[0]][fpos[1]] = self.piece_matrix[ipos[0]][ipos[1]]
            self.piece_matrix[fpos[0]][fpos[1]].change(fpos)
            self.piece_matrix[ipos[0]][ipos[1]] = None
            return True
        return False

    def initial_pieces(self):
        self.piece_matrix = [[None for i in range(8)] for j in range(8)]

        for i in range(8):
            self.replace(Pawn([1, i], "White"))
            self.replace(Pawn([6, i], "Black"))
        
        self.replace(Rook([0, 0], "White"))
        self.replace(Rook([0, 7], "White"))
        self.replace(Rook([7, 0], "Black"))
        self.replace(Rook([7, 7], "Black"))

        self.replace(Knight([0, 1], "White"))
        self.replace(Knight([0, 6], "White"))
        self.replace(Knight([7, 1], "Black"))
        self.replace(Knight([7, 6], "Black"))

        self.replace(Bishop([0, 2], "White"))
        self.replace(Bishop([0, 5], "White"))
        self.replace(Bishop([7, 2], "Black"))
        self.replace(Bishop([7, 5], "Black"))

        self.replace(Queen([0,3], "White"))
        self.replace(Queen([7,3], "Black"))

        self.replace(King([0,4], "White"))
        self.replace(King([7,4], "Black"))

    def up_move(self, initial_place, final_place, move = True):
        if move:
            if not self.move(initial_place, final_place):
                return
            if self.turn == "White":
                self.turn = "Black"
            else:
                self.turn = "White"
        
        self.attackedplacesbyblack = []
        self.attackedplacesbywhite = []
        
        for row in self.piece_matrix:
            for piece in row:
                if piece != None:
                    if piece.type != "King": 
                        piece.up_move(self.piece_matrix)
                        a = piece.moves
                        if piece.color == "Black":
                            self.attackedplacesbyblack.extend(a)
                        else:
                            self.attackedplacesbywhite.extend(a)
        for row in self.piece_matrix:
            for piece in row:
                if piece != None:
                    if piece.type == "King":
                        if piece.color == "Black":
                            piece.up_move(self.piece_matrix, self.attackedplacesbywhite)
                        else:
                            piece.up_move(self.piece_matrix, self.attackedplacesbyblack)
        for row in self.piece_matrix:
            for piece in row:
                if piece != None:
                    if piece.color != self.turn:
                        piece.moves = []

    def generate_matrix(self):
        matrix = [[ColoredText("-", Fore.WHITE) for i in range(8)] for j in range(8)]
        for row in self.piece_matrix:
            for piece in row:
                if piece != None:
                    x = piece.pos[0]
                    y = piece.pos[1]
                    matrix[x][y] = ColoredText(piece.str.text, piece.str.color)
        
        return matrix
    
    def str_matrix(self, matrix):
        string = Fore.WHITE + "  01234567\n"
        for i in range(7,-1, -1):
            string += Fore.WHITE + str(i) + " "
            for j in range(8):
                piece = matrix[i][j]
                string += str(matrix[i][j])
            string += "\n"
        return string  
    
    def __str__(self) -> str:
        matrix = self.generate_matrix()
        return self.str_matrix(matrix)
    
    def print_pos_move(self, pos):
        if (pos[0] < 0) or (pos[0] > 7):
            return
        if (pos[1] < 0) or (pos[1] > 7):
            return 
        matrix = self.generate_matrix()
        piece = self.piece_matrix[pos[0]][pos[1]]
        if piece != None:
            for move in piece.moves:
                x = move[0]
                y = move[1]
                matrix[x][y].color = Fore.BLUE
        print(self.str_matrix(matrix))

