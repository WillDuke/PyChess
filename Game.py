# import os
# import numpy as np
# from abc import abstractmethod
import pygame 
from Piece import Group, Pawn, Knight, Bishop, Rook, Queen, King

class ChessSet:

    def __init__(self):

        self.n_squares = 8
        self.surface_sz = 480
        self.sq_sz = self.surface_sz // self.n_squares
        self.surface_sz = self.n_squares * self.sq_sz
        # self.colors = [(255,248,220), (205,133,63)]

        self.board = [['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
                    ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
                    ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']]

        self.p_names = {'r': (Rook, "black"), 'n': (Knight, "black"),
                       'b': (Bishop, "black"),'q': (Queen, "black"),
                       'k': (King, "black"),'p': (Pawn, "black"),
                       'R': (Rook, "white"), 'N': (Knight, "white"),
                       'B': (Bishop, "white"),'Q': (Queen, "white"),
                       'K': (King, "white"),'P': (Pawn,"white")}

    def get_pieces(self):
        # w_pieces = Group()
        # b_pieces = Group()
        pieces = Group()
        # empty_squares = Group()

        for ycd, col in enumerate(self.board):
            for xcd, square in enumerate(col):
                if square:
                    class_, color = self.p_names[square]
                    piece = class_(color, self.sq_sz)
                    piece.rect.x = xcd * self.sq_sz
                    piece.rect.y = ycd * self.sq_sz
                    piece.pos = (piece.rect.x, piece.rect.y)
                    # print((piece.pos))
                    # if color == "white":
                    #     w_pieces.add(piece)
                    # else: b_pieces.add(piece)
                    pieces.add(piece)
        # return w_pieces, b_pieces
        # print(pieces.get_positions())
        return pieces

### GAME ###

SURFACE_SIZE = 480
BOARD_COLORS = [(255,248,220), (205,133,63)]

class Game:

    def __init__(self, surface_size, board_colors):

        self.board_colors = board_colors
        self.surface_sz = surface_size
        self.n_squares = 8
        self.sq_sz = self.surface_sz // self.n_squares
        self.surface_sz = self.n_squares * self.sq_sz
        self.size = [self.surface_sz, self.surface_sz]
        self.surface = pygame.display.set_mode(self.size)

        self.game_over = False
        self.chess_set = ChessSet()
        # self.w_pieces, self.b_pieces = self.chess_set.get_pieces()
        self.pieces = self.chess_set.get_pieces()
    
    def process_events(self):
        """ Process all of the events. Return a "True" if we need
            to close the window. """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return True
    
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.game_over:
                    self.__init__(SURFACE_SIZE, BOARD_COLORS)
                # if left-mouse clicked, update mouse position
                if event.button == 1:
                    # self.w_pieces.update(mouse = event.pos)
                    # self.b_pieces.update(mouse = event.pos)
                    self.pieces.update(mouse = event.pos)
                
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    # self.w_pieces.update(remove_select = True)
                    # self.b_pieces.update(remove_select = True)
                    self.pieces.update(remove_select = True)
                
            elif event.type == pygame.MOUSEMOTION:
                    # move object
                # self.w_pieces.update(event.pos[0], event.pos[1])
                # self.b_pieces.update(event.pos[0], event.pos[1])
                self.pieces.update(move = event.pos)

        return False
    
    def display_frame(self):
        """ Display everything to the screen for the game. """
        # screen.fill(WHITE)
 
        if self.game_over:
            # font = pygame.font.Font("Serif", 25)
            font = pygame.font.SysFont("serif", 25)
            text = font.render("Game Over, click to restart", True, "BLACK")
            center_x = (self.surface_sz // 2) - (text.get_width() // 2)
            center_y = (self.surface_sz // 2) - (text.get_height() // 2)
            self.surface.blit(text, [center_x, center_y])
 
        if not self.game_over:
            # self.w_pieces.draw(self.surface)
            # self.b_pieces.draw(self.surface)
            self.pieces.draw(self.surface)

        pygame.display.flip()

    def chessboard(self):

        for row in range(self.n_squares):           # Draw each row of the board.
            c_indx = row % 2           # Alternate starting color
            for col in range(self.n_squares):       # Run through cols drawing squares
                the_square = (col*self.sq_sz, row*self.sq_sz, self.sq_sz, self.sq_sz)
                self.surface.fill(self.board_colors[c_indx], the_square)
                # Now flip the color index for the next square
                c_indx = (c_indx + 1) % 2


def main():

    # Initialize Pygame and set up the window
    pygame.init()
 
    pygame.display.set_caption("PyChess")
    # pygame.mouse.set_visible(False)
 
    # Create our objects and set the data
    done = False
    clock = pygame.time.Clock()
 
    # Create an instance of the Game class
    game = Game(SURFACE_SIZE, BOARD_COLORS)
 
    # Main game loop
    while not done:
 
        # Process events (keystrokes, mouse clicks, etc)
        done = game.process_events()

        game.chessboard()
 
        # Update object positions, check for collisions
        # game.run_logic()
 
        # Draw the current frame
        game.display_frame()
 
        # Pause for the next frame
        clock.tick(60)
 
    # Close window and exit
    pygame.quit()
 
if __name__ == "__main__":
    main()

            