import pygame as p
import FoxGame
p.init()
WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}


def load_images():
    pieces = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ', 'ff']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))

def main():
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    game = FoxGame.Game()
    load_images()
    running = True
    selected_square = ()
    clicks = []
    valid_moves = game.get_valid_moves()
    move_made = False
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                column = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                if selected_square == (row, column):
                    selected_square = ()
                    clicks = []
                else:
                    selected_square = (row, column)
                    clicks.append(selected_square)
                if len(clicks) == 2:
                    move = FoxGame.Move(clicks[0], clicks[1], game.board)
                    if move in valid_moves:
                        game.make_move(move)
                        move_made = True
                        selected_square = ()
                        clicks = []
                    else:
                        clicks = [selected_square]
            if move_made:
                valid_moves = game.get_valid_moves()
                move_made = False

        drawGame(screen, game)
        if game.checkmate:
            if game.whiteToMove is False:
                print("White wins by checkmate!")
            else:
                print("Black wins by checkmate!")
            running = False
        elif game.stalemate:
            print("Draw by stalemate")
            running = False
        clock.tick(MAX_FPS)
        p.display.flip()


def drawGame(screen, game):
    drawBoard(screen)
    drawPieces(screen, game.board)


def drawBoard(screen):
    colors = [p.Color("white"), p.Color("green")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[(r+c) % 2]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

if __name__ == "__main__":
    main()