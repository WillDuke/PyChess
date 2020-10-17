# import os
# import numpy as np
# from abc import abstractmethod
import pygame
from Piece import ChessSet, PromotionSet

### GAME ###
FPS = 60.0
SURFACE_SIZE = 480
BOARD_COLORS = [(255, 248, 220), (205, 133, 63)]


class Game:
    def __init__(self, surface_size, board_colors):

        self.board_colors = board_colors
        self.surface_sz = surface_size
        self.n_squares = 8
        self.sq_sz = self.surface_sz // self.n_squares
        self.surface_sz = self.n_squares * self.sq_sz
        # self.size = [self.surface_sz, self.surface_sz]
        self.size = [self.surface_sz + 180, self.surface_sz]
        self.surface = pygame.display.set_mode(self.size)

        self.game_over = False
        self.chess_set = ChessSet()
        self.pieces = self.chess_set.create()

    def process_events(self):
        """Process all of the events. Return a "True" if we need
        to close the window."""
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
                    # self.pieces.update(mouse=event.pos)
                    self.pieces.select(event.pos)

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.pieces.update()

            elif event.type == pygame.MOUSEMOTION:
                self.pieces.drag(event.pos)

        return False

    def promotion_set(self, pawn_pos):
        
        print("Got inside if statement!")
        promotion_set = PromotionSet("white", self.sq_sz, pawn_pos)
        print(promotion_set)

        return promotion_set


    def draw_promotion(self, promotion_set):
        """draw the options for selecting a piece to promote to"""

        self.chessboard()
        self.game_info()
        self.pieces.draw(self.surface)
        promotion_set.draw(self.surface)

        pygame.display.flip()

    def process_promotion(self, promotion_set):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                # if left-mouse clicked, update mouse position
                if event.button == 1:
                    print("testing!")
                    selected = promotion_set.select(event.pos)
                    if selected:
                        print(f"Promoted to {selected.__name__}")
                        return selected
        
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
            self.chessboard()
            self.game_info()
            self.pieces.draw(self.surface)

        pygame.display.flip()

    def chessboard(self):

        for row in range(self.n_squares):  # Draw each row of the board.
            c_indx = row % 2  # Alternate starting color
            for col in range(self.n_squares):  # Run through cols drawing squares
                the_square = (
                    col * self.sq_sz,
                    row * self.sq_sz,
                    self.sq_sz,
                    self.sq_sz,
                )
                self.surface.fill(self.board_colors[c_indx], the_square)
                # Now flip the color index for the next square
                c_indx = (c_indx + 1) % 2
    
    def game_info(self):

        self.surface.fill((100,100,100), (480, 0, 180, 480))
        self.surface.fill((0,0,0), (500, 20, 140, 400))


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

        # Update object positions, check for collisions
        # game.run_logic()

        # get the location of a promotion
        promote_loc = game.pieces.promotion
        if promote_loc:
            
            # create a promotion set based on the promotion pos
            promotion_set = game.promotion_set(promote_loc)

            # while the play has not chosen an option, draw promotion set
            chosen = False
            while not chosen:

                # draw the piece options
                game.draw_promotion(promotion_set)

                # check if a piece is selected
                chosen_piece = game.process_promotion(promotion_set) 
                
                # if selected, tell game to replace that piece 
                if chosen_piece:
                    print(chosen_piece)
                    # tell pieces to replace the piece at promote_loc with chosen_piece
                    # also updates the history to reflect this change
                    game.pieces.promote(promote_loc, chosen_piece)
                    # tell pieces to update the history to reflect the change
                    
                    chosen = True

                    

                
        # Draw the current frame
        game.display_frame()

        
            # while inp != "quit":

            #     inp = input("Write something:")

        # Pause for the next frame
        clock.tick(FPS)

    # Close window and exit
    pygame.quit()


if __name__ == "__main__":
    main()

