#Usado para printar o tabuleiro colorido no terminal
from colorama import init, Fore

#Define uma classe para manipular textos coloridos
class ColoredText:
    #Cada objeto tem uma cor e um texto
    def __init__(self, text, color) -> None:
        self.color = color
        self.text = text
    #Converte o objeto em uma string
    def __str__(self) -> str:
        return str(self.color + self.text)

#Define a classe mãe para a implementação do jogo
class ChessPiece:
    #Cada peça tem um tipo, uma posicao e uma cor
    #O simbolo é usado para printar o tabuleiro
    def __init__(self, type_, pos, color, symbol):
        self.color = color 
        self.pos = pos
        self.moves = None #possivel posições na qual a peça pode se mover
        self.type = type_
        self.played = False #Verifica se a peça já foi movida

        #Usado para printar o tabuleiro no terminal
        self.str = ColoredText(symbol, self.get_color_text()) 
        self.movestoking = None
        self.findking = False

    def get_moves(self):
        return self.moves

    #Muda a posição de uma peça
    def change(self, new_pos):
        self.played = True
        self.pos = new_pos
    
    #Obtém a peça em uma determinada linha e coluna de matriz de peças
    def check(self, piece_matrix, pos):
        return piece_matrix[pos[0]][pos[1]]
    
    #Verifica se há alguma peça em determinada posição. Se não houver a rotina 
    #apenas adiciona aquela posição nos possíveis movimentos
    #Se houver uma peça, verifica a cor dela e adiciona se for da cor contrária
    #Retorna True se tem alguma peça
    def addmove(self, piece_matrix, pos):
        piece = self.check(piece_matrix, pos)
        if piece != None:
            if piece.color != self.color:
                self.moves.append(pos)
                if piece.type == "King":
                    self.findking = True
            return True
        else:
            self.movestoking.append(pos)
            self.moves.append(pos)
            return False
        
    #Verifica se determinada posição pertence se está contida no tabuleiro 
    # de 8x8 do jogo
    def inboard(self, pos):
        in_ = True
        in_ &= (pos[0] < 8)
        in_ &= (pos[0] > -1)
        in_ &= (pos[1] < 8)
        in_ &= (pos[1] > -1)
        return in_
    
    #Obtém a cor da peça (Usado para printar no terminal)
    def get_color_text(self):
        if self.color == "White":
            return Fore.GREEN
        else:
            return Fore.MAGENTA
    
    #Define um padrão de movimentação de uma peça genérica 
    def way(self, pos, dx, dy, piece_matrix):
        #calcula uma posição considerando a variação esperada dx e dy
        npos = [pos[0]+dx, pos[1]+dy] 
        if self.inboard(npos): #Verifica se essa posição tem no tabuleiro
            if self.addmove(piece_matrix, npos): #Verifica a proxima posicao
                return #Para a recursão se encontrar uma peça
            else:
                #Continua a recursão até encontrar uma peça
                self.way(npos, dx, dy, piece_matrix) 
    
    #Printa o texto (Usado para o terminal)
    def __str__(self) -> str:
        return str(self.str)
    
    def check_block_king(self, piece_matrix):
        for row in piece_matrix:
            for piece in row:
                if piece != None:
                    if piece.type == "King" and piece.color == self.color:
                        king_pos = piece.pos
                        break
        
        piece_matrix_copy = piece_matrix.copy()
        piece_matrix_copy[self.pos[0]][self.pos[1]] = None
        for row in piece_matrix_copy:
            for piece in row:
                if piece != None:
                    if piece.color != self.color:
                        piece.up_move(piece_matrix_copy)
                        #Adiciona as peças nas casas atacadas
                        if king_pos in piece.moves:
                            return True     
        return False
         
#Define uma classe filha de ChessPiece: Rook (Torre)
class Rook(ChessPiece):
    #inicia a classe definindo o tipo como "Rook"
    def __init__(self, pos, color):
        super().__init__("Rook", pos, color, "R")
    
    #Define uma rotina para atualizar as possiveis jogadas da torre 
    def up_move(self, piece_matrix):
        self.moves = [] #Zera as possíveis jogadas
        self.movestoking = []
        self.findking =  False
        if self.check_block_king:
            return
        #define os sentidos do movimento da torre (pra cima, pra baixo, pra esquerda e pra direita)
        moves = [[1, 0], [-1, 0], [0, -1], [0, 1]] 
        for move in moves:
            self.way(self.pos,  move[0],  move[1], piece_matrix)

#Define uma classe filha de ChessPiece: Bishop (Bispo)
class Bishop(ChessPiece):
    #Mesma lógica da torre
    def __init__(self, pos, color):
        super().__init__("Bishop", pos, color, "B")
    
    #Mesma lógica da torre, mas pras diagonais
    def up_move(self, piece_matrix):
        self.moves = []
        self.movestoking = []
        self.findking =  False
        if self.check_block_king:
            return
        moves = [[1, 1], [1, -1], [-1, 1], [-1, -1]]
        for move in moves:
            self.way(self.pos,  move[0],  move[1], piece_matrix)

#Define uma classe filha de ChessPiece: Knight (Cavalo)
class Knight(ChessPiece):
    #Mesma lógica da torre
    def __init__(self, pos, color):
        super().__init__("Knight", pos, color, "N")
    
    #Redefine way porque o cavalo pula casas
    def way(self, dx, dy, piece_matrix):
        npos = [self.pos[0]+dx, self.pos[1]+dy]
        if self.inboard(npos):
            self.addmove(piece_matrix, npos)       
    
    #atualiza os movimentos do cavalo
    def up_move(self, piece_matrix):
        self.moves = []
        self.movestoking = []
        self.findking =  False
        if self.check_block_king:
            return
        #Tenta todas os oito possíveis jogadas do cavalo
        moves = [[1, 2], [-1, 2], [1, -2], [-1, -2], [2, 1], [2,-1], [-2,1], [-2, -1]]
        for move in moves:
            self.way(move[0], move[1], piece_matrix) 

#Define uma classe filha de ChessPiece: Pawn (Peão)
class Pawn(ChessPiece):
    #idem da torre
    def __init__(self, pos, color):
        super().__init__("Pawn", pos, color, "P")
        self.availableenpassant = False

        #Se as peças forem pretas o sentido de "para frente" é ao contrário
        self.invert = 1
        if self.color == "Black": #Se 
            self.invert = -1

        self.posenpassant = [self.pos[0]+self.invert, self.pos[1]]
        self.enpassantmoves = []

    #modifica o método way para o peão
    def way(self, dx, dy, piece_matrix, attack = False):
        pos = [self.pos[0] +dx, self.pos[1]+dy]
        if self.inboard(pos):
            if attack: #Verifica se é um movimento de ataque
                self.attack(piece_matrix, pos)
                return
            self.addmove(piece_matrix, pos)

    #Tenta adicionar um movimento só se a casa estiver vazia
    def addmove(self, piece_matrix, pos):
        piece = self.check(piece_matrix, pos)
        if piece == None:
            self.moves.append(pos)

    #define o movimento de ataque do peao
    def attack(self, piece_matrix, pos):
        piece = self.check(piece_matrix, pos)
        if piece != None:
            if piece.color != self.color:
                self.moves.append(piece.pos)

        #en passant
        posn = [self.pos[0], pos[1]]
        piece = self.check(piece_matrix, pos)
        if piece != None:
            if piece.color != self.color:
                if piece.type == "Pawn":
                    if piece.availableenpassant == True:
                        self.moves.append(piece.posenpassant)
                        self.enpassantmoves.append(piece.posenpassant)

    #Atualiza os movimentos do peão
    def up_move(self, piece_matrix):
        self.moves = []
        self.enpassantmoves = []
        self.movestoking = []
        self.findking =  False
        if self.check_block_king:
            return
        
        #Verifica se é o primeiro movimento
        if not self.played:
            self.way(2*self.invert, 0, piece_matrix)
        
        #Verifica se a casa da frente esta livre
        self.way(1*self.invert, 0, piece_matrix)

        #Verifica as casas possíveis de serem atacadas
        self.way(1*self.invert, 1, piece_matrix ,True)
        self.way(1*self.invert, -1, piece_matrix ,True)

    def change(self, new_pos):
        if self.played == False and abs(new_pos[0] - self.pos[1]) > 1:
            self.availableenpassant = True
        else:
            self.availableenpassant = False

        self.played = True
        self.pos = new_pos

#Define uma classe filha de ChessPiece: King (Rei)
class King(ChessPiece):
    #idem torre
    def __init__(self, pos, color):
        super().__init__("King", pos, color, "K")
        self.castlingmoves = []

    #define o movimento do rei sem recursividade 
    def way(self, dx, dy, piece_matrix):
        pos = [self.pos[0]+dx, self.pos[1]+dy]
        if self.inboard(pos):
            self.addmove(piece_matrix, pos)

    def castling(self, pos, dy, piece_matrix):
        if not self.played:
            npos = [pos[0], pos[1]+dy]
            if self.inboard(pos):
                piece = self.check(piece_matrix, pos)
                if piece == None:
                    self.castling(npos, dy, piece_matrix)
                elif piece.type ==  "Rook":
                    if piece.played == False:
                        self.castlingmoves.append(piece.pos)
                        self.moves.append(piece.pos)
                        return True
        return False

    #atualiza o movimento do rei
    def up_move(self, piece_matrix, attackedplaces):
        self.moves = []
        self.castlingmoves = []
        self.movestoking = []
        self.findking =  False
        if self.check_block_king:
            return

        #Tenta se mover pra cada direção
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if i==0 and j ==0: #menos pra direção nula
                    continue
                else:
                    self.way(i, j, piece_matrix)

        if not self.pos in attackedplaces:
            self.castling(self.pos, 1, piece_matrix)
            self.castling(self.pos, -1, piece_matrix)
        
        #Verifica as casas atacadas pelas peças adiversárias
        for move in self.moves:
            if move in attackedplaces:
                self.moves.remove(move)

#Define uma classe filha de ChessPiece: Queen (Queen)
class Queen(ChessPiece):
    #idem torre
    def __init__(self, pos, color):
        super().__init__("Queen", pos, color, "Q")

    #Atualiza os movimentos da rainha
    def up_move(self, piece_matrix):
        self.moves = []
        self.movestoking = []
        self.findking =  False
        if self.check_block_king:
            return
        for i in [-1, 0, 1]: #tenta cada direção
            for j in [-1, 0, 1]:
                if i==0 and j ==0: #menos a direção 00
                    continue
                else:
                    self.way(self.pos, i, j, piece_matrix)

class ChessGame:
    #inicia a classe
    def __init__(self) -> None:
        init(autoreset=True)
        self.initial_pieces()  
        self.attackedplacesbyblack = []
        self.attackedplacesbywhite = []
        self.turn = "White"
        self.incheck = None
        self.posblackking = None
        self.poswhiteking = None

    #substitui a peça em determinada posição da matriz de peças (Usado para posicionar as peças)
    def replace (self, new_piece, pos_ = None):
        if new_piece != None:
            pos = new_piece.pos
            self.piece_matrix[pos[0]][pos[1]] = new_piece
        else:
            self.piece_matrix[pos_[0], pos_[1]] = None

    def en_passant(self, ipos, fpos):
        piece = self.piece_matrix[ipos[0]][ipos[1]]
        if piece.type ==  "Pawn":
            return fpos in self.piece_matrix[ipos[0]][ipos[1]].enpassantmoves
        return False
       
    def in_available_moves(self, ipos, fpos):
        return fpos in self.piece_matrix[ipos[0]][ipos[1]].moves
    
    def castling(self, ipos, fpos):
        piece = self.piece_matrix[ipos[0]][ipos[1]]
        if piece.type == "King":
            return fpos in self.piece_matrix[ipos[0]][ipos[1]].castlingmoves
        return False
    
    def move_castling (self, ipos, fpos):
        d = fpos[1] - ipos[1]
        fpos_rook = [fpos[0], fpos[1] - (d/abs(d))*2]
        fpos_king = [ipos[0], ipos[1] + d - 1]


        self.piece_matrix[fpos_rook[0]][fpos_rook[1]] = self.piece_matrix[fpos[0]][fpos[1]] #move rook   
        self.piece_matrix[fpos_king[0]][fpos_king[1]] = self.piece_matrix[ipos[0]][ipos[1]] #move king            
                
        self.piece_matrix[fpos_rook[0]][fpos_rook[1]].change(fpos_rook)
        self.piece_matrix[fpos_king[0]][fpos_king[1]].change(fpos_king)

        self.piece_matrix[ipos[0]][ipos[1]] = None
        self.piece_matrix[fpos[0]][fpos[1]] = None

    def move_default (self, ipos, fpos):
        #modifica a MATRIX de posições
        self.piece_matrix[fpos[0]][fpos[1]] = self.piece_matrix[ipos[0]][ipos[1]]

        #modifica a posição da peça na classe
        self.piece_matrix[fpos[0]][fpos[1]].change(fpos)

        #coloca "None" na posiçaõ inicial da peça
        self.piece_matrix[ipos[0]][ipos[1]] = None
        
    def av_promotion(self, ipos, fpos):
        if self.piece_matrix[ipos[0]][ipos[1]].type == "Pawn":
            if fpos[1] == 7 or fpos[1] == 0:
                return True
        return False
    
    def do_promotion(self, ipos, fpos, promotion):
        if promotion == "Bishop":
            new_piece = Bishop(fpos, self.turn)
        elif promotion == "Rook":
            new_piece = Rook(fpos, self.turn)
        elif promotion == "Queen":
            new_piece = Queen(fpos, self.turn)
        elif promotion == "Knight":
            new_piece = Knight(fpos, self.turn)

        self.piece_matrix[fpos[0]][fpos[1]] = new_piece
        self.piece_matrix[ipos[0]][ipos[1]] = None

    #Move uma peça de uma posição inicial para outra
    #Retorna verdadeiro se aquela posição final é possível
    def move (self, ipos, fpos, promotion = None):
        #Verifica se esse movimento é permitido
        if self.in_available_moves(ipos, fpos):
            if self.castling(ipos, fpos):
                self.move_castling(ipos, fpos)
            elif self.av_promotion(ipos, fpos):
                self.do_promotion
            else:
                self.move_default(ipos, fpos)

                if self.en_passant:
                    self.piece_matrix[ipos[0]][fpos[1]] = None

            return True
        return False

    def initial_pieces(self):
        #define a matrix de peças
        self.piece_matrix = [[None for i in range(8)] for j in range(8)]

        #posiciona as peças iniciais
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

    #tenta mover uma peça e atualiza os possíveis movimentos
    def up_move(self, initial_place, final_place, move = True):
        if move: #Tenta mover uma peça
            #Verifica se foi possivel fazer um movimento
            if not self.move(initial_place, final_place):  
                return
            #Inverte o turno do jogador
            if self.turn == "White":
                self.turn = "Black"
            else:
                self.turn = "White"
        
        #Zera as casas atacadas pelos jogadores
        self.attackedplacesbyblack = []
        self.attackedplacesbywhite = []
        
        #atualiza os movimentos de cada peça que não é Rei
        for row in self.piece_matrix:
            for piece in row:
                if piece != None:
                    if piece.type != "King": 
                        piece.up_move(self.piece_matrix)
                        #Adiciona as peças nas casas atacadas
                        a = piece.moves
                        if piece.color == "Black":
                            self.attackedplacesbyblack.extend(a)
                        else:
                            self.attackedplacesbywhite.extend(a)

        #atualiza os movimentos dos reis
        for row in self.piece_matrix:
            for piece in row:
                if piece != None:
                    if piece.type == "King":
                        if piece.color == "Black":
                            self.posblackking = piece.pos
                            piece.up_move(self.piece_matrix, self.attackedplacesbywhite)
                        else:
                            self.poswhiteking = piece.pos
                            piece.up_move(self.piece_matrix, self.attackedplacesbyblack)

        #Zera os possiveis movimentos do jogador que não está jogando
        for row in self.piece_matrix:
            for piece in row:
                if piece != None:
                    if piece.color != self.turn:
                        piece.moves = []

        if self.turn == "White":
            if not self.poswhiteking in self.attackedplacesbyblack:
                return
        else:
            if not self.posblackking in self.attackedplacesbywhite:
                return
        
        moves_to_block = []
        for row in self.piece_matrix:
            for piece in row:
                if piece != None:
                    if piece.color != self.turn:
                        if piece.findking:
                            moves_to_block = piece.movestoking.copy()
                            moves_to_block.append(piece.pos)
                            break

        if len(moves_to_block) != 0:
            self.incheck = self.turn
        else:
            self.incheck = None

        count_moves = 0
        if self.incheck:
            for row in self.piece_matrix:
                for piece in row:
                    if piece != None:
                        if piece.type != "King":
                            if piece.color == self.turn:
                                for move in piece.moves:
                                    if not move in moves_to_block:
                                        piece.moves.remove(move)
                                count_moves += len(piece.moves)
        if count_moves == 0:
            print(f"Loser: {self.turn}")

    #Gera uma matriz de COloredTExt (usado para printar no terminal)
    def generate_matrix(self):
        matrix = [[ColoredText("-", Fore.WHITE) for i in range(8)] for j in range(8)]
        for row in self.piece_matrix:
            for piece in row:
                if piece != None:
                    x = piece.pos[0]
                    y = piece.pos[1]
                    matrix[x][y] = ColoredText(piece.str.text, piece.str.color)
        
        return matrix
    
    #Transforma uma matriz de coloredText em uma string (Tabuleiro no terminal)
    def str_matrix(self, matrix):
        string = Fore.WHITE + "  01234567\n"
        for i in range(7,-1, -1):
            string += Fore.WHITE + str(i) + " "
            for j in range(8):
                piece = matrix[i][j]
                string += str(matrix[i][j])
            string += "\n"
        return string  
    
    #printa o tabuleiro (Tabuleiro no terminal)
    def __str__(self) -> str:
        matrix = self.generate_matrix()
        return self.str_matrix(matrix)
    
    #Modifica a cor das casas em que uma peça pode ser movida
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
    
    def get_piece(self, pos):
        return self.piece_matrix[pos[0]][pos[1]]