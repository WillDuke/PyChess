import numpy as np
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
                print(f"Set selected for {self.__class__.__name__}")
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

    def isLegal(self, board, proposed):
        # what is the position on the board?
        legal = False
        
        prop_x, prop_y = tuple(i // self.sq_sz for i in proposed)
        print(prop_x, prop_y)
        current_x, current_y = tuple(i // self.sq_sz for i in self.pos)
        print(current_x, current_y)

        # move two spaces for first move
        if current_x == prop_x:
            if abs(current_y - prop_y) == 2:
                if self.firstmove:
                    legal = True
                    
            # move one space for first move
            elif abs(current_y - prop_y) == 1:
                legal = True

        # move diagonally if piece not of own color (capture is separate)
        elif abs(current_x - prop_x) == 1:
            if abs(current_y - prop_y) == 1:
                if board[prop_y][prop_x] and self.color not in board[prop_y][prop_x]:
                    legal = True
        
        if legal:
            self.firstmove = False
        
        return legal

class Knight(Piece):
    """
    currently limits to L-shape move and checks if proposed move lands on white piece
    note: doesn't yet handle capturing
    """
    def __init__(self, color, sq_sz):
        super().__init__("knight", color, sq_sz)
    
    def isLegal(self, board, proposed):
        legal = True

        if not self._reachable(proposed):
            legal = False
        
        if not self._available(board, proposed):
            legal = False
        
        return legal
    
    def _reachable(self, proposed):
        reachable = False

        prop_x, prop_y = tuple(i // self.sq_sz for i in proposed)
        print(prop_x, prop_y)
        current_x, current_y = tuple(i // self.sq_sz for i in self.pos)
        print(current_x, current_y)

        diff_x = abs(prop_x - current_x)
        diff_y = abs(prop_y - current_y)

        if all([diff_x <= 2, diff_y <=2, diff_y + diff_x == 3]):
            reachable = True
        
        return reachable

    def _available(self, board, proposed):
        
        available = True

        prop_x, prop_y = tuple(i // self.sq_sz for i in proposed)
        # current_x, current_y = tuple(i // self.sq_sz for i in self.pos)
        
        if self.color in str(board[prop_y][prop_x]):
            available = False
        
        return available
    

class Bishop(Piece):
    """
    currently limits diagonal move without blocking piece on diagonal
    and checks if proposed move lands on own color piece
    note: doesn't yet handle capturing
    """
    def __init__(self, color, sq_sz):
        super().__init__("bishop", color, sq_sz)

    def isLegal(self, board, proposed):
        legal = True

        if not self._reachable(board, proposed):
            legal = False

        
        if not self._available(board, proposed):
            legal = False
        
        return legal

    def _reachable(self, board, proposed):
        reachable = True

        prop_x, prop_y = tuple(i // self.sq_sz for i in proposed)
        current_x, current_y = tuple(i // self.sq_sz for i in self.pos)

        diff_x = prop_x - current_x
        diff_y = prop_y - current_y

        inter = np.arange(1, abs(diff_x))
        inter = list(zip(inter * np.sign(diff_x) + current_x, 
                        inter * np.sign(diff_y) + current_y))

        if abs(diff_x) != abs(diff_y):
            reachable = False
        
        for pos in inter:
            if board[pos[1]][pos[0]] != 0:
                reachable = False

        return reachable

    def _available(self, board, proposed):
        available = True

        prop_x, prop_y = tuple(i // self.sq_sz for i in proposed)
        # current_x, current_y = tuple(i // self.sq_sz for i in self.pos)
        
        if self.color in str(board[prop_y][prop_x]):
            available = False
        
        return available
    
class Rook(Piece):
    def __init__(self, color, sq_sz):
        super().__init__("rook", color, sq_sz)

    def isLegal(self, board, proposed):
        legal = True

        if not self._reachable(board, proposed):
            legal = False

        
        if not self._available(board, proposed):
            legal = False
        
        return legal
    
    def _reachable(self, board, proposed):
        reachable = True

        prop_x, prop_y = tuple(i // self.sq_sz for i in proposed)
        current_x, current_y = tuple(i // self.sq_sz for i in self.pos)

        # inter = np.arange(1, abs(diff_x))
        # inter = list(zip(inter * np.sign(diff_x) + current_x, 
        #                 inter * np.sign(diff_y) + current_y))

        if prop_x == current_x:
            comp1, comp2 = current_y, prop_y
        else: comp1, comp2 = current_x, prop_x 

        # check that one of the directions is the same (vertical or horiz move)
        if not (prop_x == current_x or prop_y == current_y):
            reachable = False
        
        # find inter
        inter = np.arange(min(comp1, comp2) + 1, 
                        max(comp1, comp2))
        
        for pos in inter:
            if board[pos[1]][pos[0]] != 0:
                reachable = False

        return reachable

    def _available(self, board, proposed):
        available = True

        prop_x, prop_y = tuple(i // self.sq_sz for i in proposed)
        # current_x, current_y = tuple(i // self.sq_sz for i in self.pos)
        
        if self.color in str(board[prop_y][prop_x]):
            available = False
        
        return available
    
class Queen(Piece):
    def __init__(self, color, sq_sz):
        super().__init__("queen", color, sq_sz)
        
    def isLegal(self, board, proposed):
        return True
    
class King(Piece):
    def __init__(self, color, sq_sz):
        super().__init__("king", color, sq_sz)

    def isLegal(self, board, proposed):
        return True