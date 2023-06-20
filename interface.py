import pygame
import classesfile

# Initialize Pygame
pygame.init()

# Define constants
WIDTH = HEIGHT = 512
SQUARE_SIZE = WIDTH // 8
FPS = 60

# Define colors
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

# Load chess piece images
piece_images = {
    'White': {
        'Pawn': pygame.image.load('imagens/wp.png'),
        'Rook': pygame.image.load('imagens/wR.png'),
        'Knight': pygame.image.load('imagens/wN.png'),
        'Bishop': pygame.image.load('imagens/wB.png'),
        'Queen': pygame.image.load('imagens/wQ.png'),
        'King': pygame.image.load('imagens/wK.png'),
    },
    'Black': {
        'Pawn': pygame.image.load('imagens/bp.png'),
        'Rook': pygame.image.load('imagens/bR.png'),
        'Knight': pygame.image.load('imagens/bN.png'),
        'Bishop': pygame.image.load('imagens/bB.png'),
        'Queen': pygame.image.load('imagens/bQ.png'),
        'King': pygame.image.load('imagens/bK.png')
    }
}


class ChessGameGUI:
    def __init__(self, chess):
        # Initial state of the chessboard
        self.chess = chess
        # self.chess_board = [
        #     ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
        #     ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
        #     [" ", " ", " ", " ", " ", " ", " ", " "],
        #     [" ", " ", " ", " ", " ", " ", " ", " "],
        #     [" ", " ", " ", " ", " ", " ", " ", " "],
        #     [" ", " ", " ", " ", " ", " ", " ", " "],
        #     ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
        #     ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        # ]
        # self.whiteToMove = True
        self.moveLog = []

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Chess Game")
        self.clock = pygame.time.Clock()

    def draw_board(self):
        colors = [WHITE, GRAY]

        for row in range(8):
            for col in range(8):
                x, y = col * SQUARE_SIZE, row * SQUARE_SIZE
                color = colors[(row + col) % 2]
                pygame.draw.rect(self.screen, color,
                                 (x, y, SQUARE_SIZE, SQUARE_SIZE))

    def move_highlight(self, sqSelected):
        if sqSelected != ():
            r, c = sqSelected
            # if self.chess_board[r][c][0] == ('w' if self.chess.turn else 'b'):
            piece = self.chess.get_piece([r,c])
            if piece is not None:
                if piece.color == self.chess.turn:
                    s = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE))
                    s.set_alpha(100)
                    s.fill(pygame.Color('blue'))
                    self.screen.blit(s, (c * SQUARE_SIZE, r * SQUARE_SIZE))
                    # s.fill(pygame.color('green'))
                    for m in piece.get_moves():
                        if m[0] == r and m[1] == c:
                            self.screen.blit(s, (m.endCol * SQUARE_SIZE, m.endRow * SQUARE_SIZE))

    def draw_pieces(self):
        for row in range(8):
            for col in range(8):
                piece = self.chess.get_piece([row, col])
                if piece is not None:
                    piece_image = piece_images[piece.color][piece.type]
                    piece_rect = piece_image.get_rect()
                    piece_rect.topleft = (col * SQUARE_SIZE, row * SQUARE_SIZE)
                    self.screen.blit(piece_image, piece_rect)
    
    # def make_move(self, move):
    #     self.chess_board[move.startrow][move.startcol] = " "
    #     self.chess_board[move.endrow][move.endcol] = move.pieceMoved
    #     self.moveLog.append(move)
    #     self.whiteToMove = not self.whiteToMove
    
    # def possible_moves(self, pos):
    #     row, col = pos
    #     piece = self.chess.get_piece([row, col])
    #     if piece.color == self.chess.turn:
    #         return piece.get_moves()
        # turn = self.chess_board[row][col][0]
        # if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
        #     piece_id = self.chess_board[row][col][1]
        #     if piece_id == 'p':
        #         piece = classesfile.Pawn([row, col], self.chess_board[row][col][0])
        #         piece.way(row, col, self.chess_board)
        #         return piece.get_moves()
        #     elif piece_id == 'R':
        #         piece = classesfile.Rook(
        #             [row, col], self.chess_board[row][col][0])
        #         return piece.get_moves()
        #     elif piece_id == 'N':
        #         piece = classesfile.Knight(
        #             [row, col], self.chess_board[row][col][0])
        #         return piece.get_moves()
        #     elif piece_id == 'B':
        #         piece = classesfile.Bishop(
        #             [row, col], self.chess_board[row][col][0])
        #         return piece.get_moves()
        #     elif piece_id == 'Q':
        #         piece = classesfile.Queen(
        #             [row, col], self.chess_board[row][col][0])
        #         return piece.get_moves()
        #     elif piece_id == 'K':
        #         piece = classesfile.King([row, col], [row][col][0])
        #         return piece.get_moves()
        # return []

    # def all_possible_moves(self):
    #     moves = []
    #     for row in range(len(self.chess_board)):
    #         for col in range(len(self.chess_board[row])):
    #             turn = self.chess_board[row][col][0]
    #             if (turn == 'w' and self.whiteToMove) and (turn == 'b' and not self.whiteToMove):
    #                 piece_id = self.chess_board[row][col][1]
    #                 if piece_id == 'p':
    #                     piece = classesfile.Pawn([row, col], [row][col][0])
    #                     return piece.get_moves()
    #                 elif piece_id == 'R':
    #                     piece = classesfile.Rook([row, col], [row][col][0])
    #                     return piece.get_moves()
    #                 elif piece_id == 'N':
    #                     piece = classesfile.Knight([row, col], [row][col][0])
    #                     return piece.get_moves()
    #                 elif piece_id == 'B':
    #                     piece = classesfile.Bishop([row, col], [row][col][0])
    #                     return piece.get_moves()
    #                 elif piece_id == 'Q':
    #                     piece = classesfile.Queen([row, col], [row][col][0])
    #                     return piece.get_moves()
    #                 elif piece_id == 'K':
    #                     piece = classesfile.King([row, col], [row][col][0])
    #                     return piece.get_moves()

    def run(self):
        running = True
        sqSelected = ()
        playerClicks = []

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    location = pygame.mouse.get_pos()
                    col = location[0] // SQUARE_SIZE
                    row = location[1] // SQUARE_SIZE
                    if sqSelected == (row, col):
                        sqSelected = ()
                        playerClicks = []
                    else:
                        sqSelected = (row, col)
                        playerClicks.append(sqSelected)
                        self.move_highlight(sqSelected)
                    if len(playerClicks) == 2:
                        # move = Move(playerClicks[0], playerClicks[1], self.chess.)
                        # print(move.getChessNotation())
                        startrow, startcol = playerClicks[0]
                        endrow, endcol = playerClicks[1]
                        self.chess.up_move([startrow, startcol], [endrow, endcol])
                        sqSelected = ()
                        playerClicks = []

            self.draw_board()
            self.draw_pieces()

            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()

# classe que move a peça de xadrez
# class Move():
#     ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
#                    "5": 3, "6": 2, "7": 1, "8": 0}
#     rowsToRanks = {v: k for k, v in ranksToRows.items()}
#     filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3,
#                    "e": 4, "f": 5, "g": 6, "h": 7}
#     colsToFiles = {v: k for k, v in filesToCols.items()}

#     def __init__(self, startsq, endsq, board):
#         self.startrow = startsq[0]
#         self.startcol = startsq[1]
#         self.endrow = endsq[0]
#         self.endcol = endsq[1]
#         self.pieceMoved = board[self.startrow][self.startcol]
#         self.pieceCaptured = board[self.endrow][self.endcol]
    
#     def getChessNotation(self):
#         return self.getRankFile(self.startrow, self.startcol) + self.getRankFile(self.endrow, self.endcol)

#     def getRankFile(self, r, c):
#         return self.colsToFiles[c] + self.rowsToRanks[r]

# if __name__ == '__main__':
#     game = ChessGameGUI()
#     game.run()
