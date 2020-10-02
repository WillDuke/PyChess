# import numpy as np
from itertools import product
from abc import abstractmethod
import pygame 

class Piece(pygame.sprite.Sprite):
    '''Object for each piece'''
    def __init__(self, ptype, color, sq_sz):

        super().__init__()

        sprite_path = "".join(["sprites/", color, "_", ptype, ".png"])
        self.ptype = ptype
        self.color = color
        # get scaled sprite
        self.image = pygame.transform.scale(
                        pygame.image.load(sprite_path), (sq_sz,sq_sz))
        self.sq_sz = sq_sz
        # get rect from sprite
        self.rect = self.image.get_rect()

        # position on grid for legal move checking
        self.pos = None
        # define stuff for checking click collision
        self.selected = None
        self.selected_offset_x = None
        self.selected_offset_y = None
        
    def update(self, *args, **kwargs):
        
        # look for the available kwargs
        mouse = kwargs.get("mouse")
        remove_select = kwargs.get("remove_select")
        move = kwargs.get("move")
        # if the update is for the mouse position, check 
        # if the piece collides, and if so 
        # set selected to true and specify offset
        if mouse is not None:
            # print("Made it to update!")
            if self.rect.collidepoint(mouse):
                self.selected = True
                self.selected_offset_x = self.rect.x - mouse[0]
                self.selected_offset_y = self.rect.y - mouse[1]
                print(f"Selected {self.__class__.__name__}")
        elif remove_select and self.selected:
            # snap the position to the closest square
            self.rect.x = ((round(self.rect.x/self.sq_sz)) * self.sq_sz)
            self.rect.y = ((round(self.rect.y/self.sq_sz)) * self.sq_sz)
            proposed = (self.rect.x, self.rect.y)

            if self.isLegal(args[0], proposed):
                # update position of piece on the board
                self.pos = proposed

            else:
                self.rect.x, self.rect.y = self.pos
            
            self.selected = False

        if move is not None and self.selected:
            # print(f"Args: {args}")
            self.rect.x = move[0] + self.selected_offset_x
            self.rect.y = move[1] + self.selected_offset_y
            # print(f"New Positions: {self.rect.x}, {self.rect.y}")

    @property
    def grid_loc(self):

        return self.pos[0] // self.sq_sz, self.pos[1] // self.sq_sz

    @abstractmethod
    def isLegal(self, board, proposed):
        raise NotImplementedError

class Group(pygame.sprite.Group):

    """For some reasion this is missing **kwargs in my version, so I added it."""
    def update(self, *args, **kwargs):
        """call the update method of every member sprite
        Group.update(*args): return None
        Calls the update method of every member sprite. All arguments that
        were passed to this method are passed to the Sprite update function.
        """
        board = self.get_positions()

        for sprite in self.sprites():
            sprite.update(board, *args, **kwargs)
    
    def get_positions(self):
        
        board = [[0 for i in range(8)] for i in range(8)]

        for sprite in self.sprites():
            x,y = tuple(i // sprite.sq_sz for i in sprite.pos)
            board[y][x] = " ".join([sprite.color, sprite.ptype])
        
        return board
        
class Pawn(Piece):
    def __init__(self, color, sq_sz):
        super().__init__("pawn", color, sq_sz)

        self.firstmove = True

         # eventually change this to implement board switching
        if self.color == "black":
            self.direct = 1
        elif self.color == "white":
            self.direct = -1

    def isLegal(self, board, proposed):
        # what is the position on the board?
        legal = False
        
        prop_x, prop_y = tuple(i // self.sq_sz for i in proposed)
        print(prop_x, prop_y)
        # current_x, current_y = tuple(i // self.sq_sz for i in self.pos)
        current_x, current_y = self.grid_loc
        print(current_x, current_y)

        # options
        diffs = [(0, self.direct), (0, 2 * self.direct), (1, self.direct), (-1, self.direct)]
        moves = [(current_x + d[0], current_y + d[1]) for d in diffs]
        
        single = moves[0]
        double = moves[1]
        capture = moves[2:]

        # remove any moves that are out of bounds
        # or no piece to capture
        for x,y in capture:

            if not (0 <= x <= 7 and 0 <= y <= 7):
                moves.remove((x,y))
            
            elif (not board[y][x]) or (self.color in str(board[y][x])):
                moves.remove((x,y))
        
        # remove a single space move if piece is present
        if board[single[1]][single[0]]:
            moves.remove(single)
        
        # remove the double move if not first move
        if not self.firstmove:
            moves.remove(double)

        # remove the double move if piece blocking it
        elif board[double[1]][double[0]]:
            moves.remove(double)
        
        if (prop_x, prop_y) in moves:
            legal = True
            self.firstmove = False

        return legal

class Knight(Piece):
    """

    gives list of available moves, but doesn't handle capturing
    """
    def __init__(self, color, sq_sz):
        super().__init__("knight", color, sq_sz)

        # define moves by possible change in grid number
        self.diffs = []
        self.diffs.extend(list(product([1,-1], [2, -2])))
        self.diffs.extend(list(product([2, -2], [1,-1])))

    def isLegal(self, board, proposed):
        legal = False

        prop_x, prop_y = tuple(i // self.sq_sz for i in proposed)
        print(prop_x, prop_y)
        # current_x, current_y = tuple(i // self.sq_sz for i in self.pos)
        current_x, current_y = self.grid_loc
        print(current_x, current_y)

        moves = []
        for diff in self.diffs:
            x,y  = diff
            p_x = current_x + x
            p_y = current_y + y
            if 0 <= p_x <= 7:
                if 0 <= p_y <= 7:
                    if board[p_y][p_x] != self.color:
                        moves.append((p_x, p_y))
        
        if (prop_x, prop_y) in moves:
            legal = True
        
        return legal

class Bishop(Piece):
    """
    currently limits diagonal move without blocking piece on diagonal
    and checks if proposed move lands on own color piece
    note: doesn't yet handle capturing
    """
    def __init__(self, color, sq_sz):
        super().__init__("bishop", color, sq_sz)

    def isLegal(self, board, proposed):
        legal = False

        prop_x, prop_y = tuple(i // self.sq_sz for i in proposed)
        print(prop_x, prop_y)
        current_x, current_y = self.grid_loc
        print(current_x, current_y)

        directs = [(1,-1), (-1,1), (-1,-1), (1,1)]
        moves = []
        
        for x,y in directs:
            for d in range(1,9):
                p_x = d * x + current_x
                p_y = d * y + current_y

                if not (0 <= p_x <= 7 and 0 <= p_y <= 7):
                    break
                
                elif self.color in str(board[p_y][p_x]):
                    break

                elif board[p_y][p_x]:
                    moves.append((p_x, p_y))
                    break

                moves.append((p_x, p_y))

        if (prop_x, prop_y) in moves:
            legal = True

        return legal


    
class Rook(Piece):
    def __init__(self, color, sq_sz):
        super().__init__("rook", color, sq_sz)

    def isLegal(self, board, proposed):
        legal = False

        prop_x, prop_y = tuple(i // self.sq_sz for i in proposed)
        print(prop_x, prop_y)
        current_x, current_y = self.grid_loc
        print(current_x, current_y)

        directs = [(0,-1), (0,1), (-1,0), (1,0)]
        moves = []
        
        for x,y in directs:
            for d in range(1,9):
                p_x = d * x + current_x
                p_y = d * y + current_y

                if not (0 <= p_x <= 7 and 0 <= p_y <= 7):
                    break
                
                elif self.color in str(board[p_y][p_x]):
                    break

                elif board[p_y][p_x]:
                    moves.append((p_x, p_y))
                    break
                
                moves.append((p_x, p_y))

        if (prop_x, prop_y) in moves:
            legal = True
       
        return legal

 
    
class Queen(Piece):
    def __init__(self, color, sq_sz):
        super().__init__("queen", color, sq_sz)
        
    def isLegal(self, board, proposed):
        legal = False

        prop_x, prop_y = tuple(i // self.sq_sz for i in proposed)
        print(prop_x, prop_y)
        current_x, current_y = self.grid_loc
        print(current_x, current_y)

        directs = [(0,-1), (0,1), (-1,0), (1,0),
                    (1,-1), (-1,1), (-1,-1), (1,1)]
        moves = []
        
        for x,y in directs:
            for d in range(1,9):
                p_x = d * x + current_x
                p_y = d * y + current_y

                if not (0 <= p_x <= 7 and 0 <= p_y <= 7):
                    break
                
                elif self.color in str(board[p_y][p_x]):
                    break

                elif board[p_y][p_x]:
                    moves.append((p_x, p_y))
                    break
                
                moves.append((p_x, p_y))

        if (prop_x, prop_y) in moves:
            legal = True
       
        return legal
    
class King(Piece):
    def __init__(self, color, sq_sz):
        super().__init__("king", color, sq_sz)

    def isLegal(self, board, proposed):
        return True