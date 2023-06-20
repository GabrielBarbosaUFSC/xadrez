import pygame
import pieces
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
    'White': {
        'Pawn': pygame.image.load(filepath('imagens/wp.png')),
        'Rook': pygame.image.load(filepath('imagens/wR.png')),
        'Knight': pygame.image.load(filepath('imagens/wN.png')),
        'Bishop': pygame.image.load(filepath('imagens/wB.png')),
        'Queen': pygame.image.load(filepath('imagens/wQ.png')),
        'King': pygame.image.load(filepath('imagens/wK.png')),
    },
    'Black': {
        'Pawn': pygame.image.load(filepath('imagens/bp.png')),
        'Rook': pygame.image.load(filepath('imagens/bR.png')),
        'Knight': pygame.image.load(filepath('imagens/bN.png')),
        'Bishop': pygame.image.load(filepath('imagens/bB.png')),
        'Queen': pygame.image.load(filepath('imagens/bQ.png')),
        'King': pygame.image.load(filepath('imagens/bK.png'))
    }
}


class ChessGameGUI:
    def __init__(self, chess):
        # Initial state of the chessboard
        self.chess = chess
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
            piece = self.chess.get_piece([r,c])
            if piece is not None:
                if piece.color == self.chess.turn:
                    s = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE))
                    s.set_alpha(100)
                    s.fill(pygame.Color('blue'))
                    self.screen.blit(s, (c * SQUARE_SIZE, r * SQUARE_SIZE))
                    s.fill(pygame.Color('green'))
                    for m in piece.get_moves():
                        self.screen.blit(s, (m[1] * SQUARE_SIZE, m[0] * SQUARE_SIZE))

    def draw_pieces(self):
        for row in range(8):
            for col in range(8):
                piece = self.chess.get_piece([row, col])
                if piece is not None:
                    piece_image = piece_images[piece.color][piece.type]
                    piece_rect = piece_image.get_rect()
                    piece_rect.topleft = (col * SQUARE_SIZE, row * SQUARE_SIZE)
                    self.screen.blit(piece_image, piece_rect)
    
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
                    if len(playerClicks) == 1:
                        piece = self.chess.get_piece(playerClicks[0])
                        if piece is None:
                            sqSelected = ()
                            playerClicks = []
                    if len(playerClicks) == 2:
                        startrow, startcol = playerClicks[0]
                        endrow, endcol = playerClicks[1]
                        self.chess.up_move([startrow, startcol], [endrow, endcol])
                        sqSelected = ()
                        playerClicks = []

            self.draw_board()
            self.move_highlight(sqSelected)
            self.draw_pieces()

            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()
