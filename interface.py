import pygame
import os
import inspect

# Initialize Pygame
pygame.init()

# Define constants
WIDTH = HEIGHT = 512
SQUARE_SIZE = WIDTH // 8
FPS = 60

# Define colors
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

def filepath(path):
    filepath = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    return os.path.join(filepath, path) 

# Load chess piece images
piece_images = {
    'wp': pygame.image.load(filepath(r'imagens/wp.png')),
    'wR': pygame.image.load(filepath(r'imagens/wR.png')),
    'wN': pygame.image.load(filepath(r'imagens/wN.png')),
    'wB': pygame.image.load(filepath(r'imagens/wB.png')),
    'wQ': pygame.image.load(filepath(r'imagens/wQ.png')),
    'wK': pygame.image.load(filepath(r'imagens/wK.png')),
    'bp': pygame.image.load(filepath(r'imagens/bp.png')),
    'bR': pygame.image.load(filepath(r'imagens/bR.png')),
    'bN': pygame.image.load(filepath(r'imagens/bN.png')),
    'bB': pygame.image.load(filepath(r'imagens/bB.png')),
    'bQ': pygame.image.load(filepath(r'imagens/bQ.png')),
    'bK': pygame.image.load(filepath(r'imagens/bK.png'))
}


class ChessGameGUI:
    def __init__(self):
        # Initial state of the chessboard
        self.chess_board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]
        self.whiteToMove = True
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

    def draw_pieces(self):
        for row in range(8):
            for col in range(8):
                piece = self.chess_board[row][col]
                if piece != " ":
                    piece_image = piece_images[piece]
                    piece_rect = piece_image.get_rect()
                    piece_rect.topleft = (col * SQUARE_SIZE, row * SQUARE_SIZE)
                    self.screen.blit(piece_image, piece_rect)
    
    def make_move(self, move):
        self.chess_board[move.startrow][move.startcol] = " "
        self.chess_board[move.endrow][move.endcol] = move.pieceMoved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove

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
                    if len(playerClicks) == 2:
                        move = Move(playerClicks[0], playerClicks[1], self.chess_board)
                        print(move.getChessNotation())
                        self.make_move(move)
                        sqSelected = ()
                        playerClicks = []

            self.draw_board()
            self.draw_pieces()

            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()

class Move():
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
                   "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3,
                   "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startsq, endsq, board):
        self.startrow = startsq[0]
        self.startcol = startsq[1]
        self.endrow = endsq[0]
        self.endcol = endsq[1]
        self.pieceMoved = board[self.startrow][self.startcol]
        self.pieceCaptured = board[self.endrow][self.endcol]
    
    def getChessNotation(self):
        return self.getRankFile(self.startrow, self.startcol) + self.getRankFile(self.endrow, self.endcol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]

if __name__ == '__main__':
    game = ChessGameGUI()
    game.run()
