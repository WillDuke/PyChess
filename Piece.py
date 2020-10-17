# import numpy as np
from itertools import product
from abc import abstractmethod
import pygame

class ChessSet(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

        # setting up the surface
        self.n_squares = 8
        self.surface_sz = 480
        self.sq_sz = self.surface_sz // self.n_squares
        self.surface_sz = self.n_squares * self.sq_sz

        # tracking captured pieces
        self.capture = None
        self.captured = pygame.sprite.Group()

        # track piece history
        self.history = []

        # test whether a piece has just promoted
        self.promotion = None

    def update(self):
        """
        Update the position of the piece by either snapping it in or reverting it,
        depending on the legality of the move.
        """
        board = self.get_positions()

        for sprite in self.sprites():

            # if sprite.color == "white":
            sprite.update(board, self.history)

            # if capture position flag, loop through and remove sprite
            if sprite.capture:
                for cap in self.sprites():
                    if cap.grid_loc == sprite.capture:
                        if cap.color != sprite.color:
                            self.captured.add(cap)
                            self.remove(cap)
                            sprite.capture = None
                            break
        
        # update the promotion attribute
        self.check_promotion()
    
    # def new_update(self):
        
    #     board = self.get_positions()

    #     # loop through pieces 
    #     legal_move = False
    #     for sprite in self.sprites():
    #         # if selected, check if move is legal -> return True
    #         if sprite.selected:

    #             if sprite.isLegal():
    #                 legal_move = True
    #                 # need to get proposed move
            
    #         # get the current king position for check detection
    #         if sprite.color == self.color:
    #             if sprite.__class__.__name__ == "King":
    #                 king_pos = sprite.pos

    #     for sprite in self.sprites():

    #         # loop through opposing pieces
    #         if self.color != sprite.color:
    #             # get the position of the king
    #             if sprite.__class__.__name__ == "King":
    #                 king_pos = sprite.pos 

    #     for sprite in self.sprites():

    #         if self.color == sprite.color:

    #             # if king_pos not in available moves
    #                 # return True


         
    #         # if none has king as available move -> return True
    #     # if both are True:
    #         # check if any of player's pieces can reach the king
    #         # update
    #     # else
    #         # revert
    
    def select(self, mouse):

        for sprite in self.sprites():
            sprite.select(mouse)
    
    def drag(self, mouse):

        on_board = all([0 <= m <= self.surface_sz for m in mouse])

        if on_board:
            for sprite in self.sprites():
                sprite.drag(mouse)

    def get_positions(self):

        board = [[0 for i in range(8)] for i in range(8)]

        for sprite in self.sprites():
            x, y = tuple(i // sprite.sq_sz for i in sprite.pos)
            board[y][x] = " ".join([sprite.color, sprite.ptype])

        return board
    
    def check_promotion(self):
        # refactor with property in pawn
        try:
            pawn_move = self.history[-1]["Name"] == "Pawn"
            pawn_on_last = self.history[-1]["Move"][1] in [0,7]

            if pawn_move and pawn_on_last:
                self.promotion = self.history[-1]["Move"]
            else: 
                self.promotion = None
        except IndexError:
            self.promotion = None
        
    def promote(self, location, chosen_piece):

        # find the pawn at the given location
        pawn_to_remove = [sprite for sprite in self.sprites() if sprite.grid_loc == location]
        print(location)
        print(pawn_to_remove)

        if pawn_to_remove:
            print("Replacing pawn with new piece.")
            self.remove(pawn_to_remove[0])
            promoted_piece = chosen_piece("white", self.sq_sz)
            new_x, new_y = location
            promoted_piece.rect.x, promoted_piece.rect.y = new_x * self.sq_sz, new_y * self.sq_sz
            promoted_piece.pos = (promoted_piece.rect.x, promoted_piece.rect.y)
            self.add(promoted_piece)
    
            updated_history = {
                "Name": promoted_piece.__class__.__name__,
                "Move": promoted_piece.grid_loc,
                "Number": len(self.history),
                "Capture": False,
                "Special": "Promoted to Queen",
            }
    
            self.history[-1] = updated_history
            self.promotion = None
            print(self.history)

    def create(self):

        # eventually need to make this flippable
        # add argument that specifies which color is on
        # the top of the board
        # then user selected color goes on the bottom

        pieces = ChessSet()

        board = [
            ["r", "n", "b", "q", "k", "b", "n", "r"],
            ["p", "p", "p", "p", "p", "p", "p", "p"],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            ["P", "P", "P", "P", "P", "P", "P", "P"],
            ["R", "N", "B", "Q", "K", "B", "N", "R"],
        ]

        p_names = {
            "r": (Rook, "black"),
            "n": (Knight, "black"),
            "b": (Bishop, "black"),
            "q": (Queen, "black"),
            "k": (King, "black"),
            "p": (Pawn, "black"),
            "R": (Rook, "white"),
            "N": (Knight, "white"),
            "B": (Bishop, "white"),
            "Q": (Queen, "white"),
            "K": (King, "white"),
            "P": (Pawn, "white"),
        }

        for ycd, col in enumerate(board):
            for xcd, square in enumerate(col):
                if square:
                    class_, color = p_names[square]
                    piece = class_(color, self.sq_sz)
                    piece.rect.x = xcd * self.sq_sz
                    piece.rect.y = ycd * self.sq_sz
                    piece.pos = (piece.rect.x, piece.rect.y)
                    pieces.add(piece)

        return pieces

class PromotionSet(pygame.sprite.Group):

    def __init__(self, color, sq_sz, pawn_position):

        super().__init__()

        # define list of options
        self.pieces = [Queen, Rook, Bishop, Knight]

        # get promoting pawn position
        pawn_x, _ = pawn_position

        # get positions of each piece
        positions = [(pawn_x * sq_sz, y * sq_sz) for y in range(len(self.pieces))]

        for p, pos in zip(self.pieces, positions):

            piece = p(color, sq_sz)
            piece.rect.x, piece.rect.y = pos

            self.add(piece)
    
    def select(self, mouse):
        selected = False
        for sprite in self.sprites():
            sprite.select(mouse)
            if sprite.selected:
                selected = [x for x in self.pieces
                        if x.__name__ == sprite.__class__.__name__][0]
                break

        return selected

        
class Piece(pygame.sprite.Sprite):
    """Object for each piece"""

    def __init__(self, ptype, color, sq_sz):

        super().__init__()

        sprite_path = "".join(["sprites/", color, "_", ptype, ".png"])
        self.ptype = ptype
        self.color = color
        # get scaled sprite
        self.image = pygame.transform.scale(
            pygame.image.load(sprite_path), (sq_sz, sq_sz)
        )
        self.sq_sz = sq_sz
        # get rect from sprite
        self.rect = self.image.get_rect()

        # position on grid for legal move checking
        self.pos = None
        # define stuff for checking click collision
        self.selected = None
        self.selected_offset_x = None
        self.selected_offset_y = None

        self.capture = None

        self.proposed = None
    
    def snap_to(self):

        if self.selected:
            # snap the position to the closest square
            self.rect.x = (round(self.rect.x / self.sq_sz)) * self.sq_sz
            self.rect.y = (round(self.rect.y / self.sq_sz)) * self.sq_sz
            self.proposed = (self.rect.x, self.rect.y)

    def update(self, board, history):
    
        if self.selected:
            # snap the position to the closest square
            self.rect.x = (round(self.rect.x / self.sq_sz)) * self.sq_sz
            self.rect.y = (round(self.rect.y / self.sq_sz)) * self.sq_sz
            proposed = (self.rect.x, self.rect.y)

            if self.isLegal(board, proposed, history=history):
                # update position of piece on the board
                self.pos = proposed
                # update tracker
                self.update_history(board, history)
                print(history)
            else:
                self.rect.x, self.rect.y = self.pos

            self.selected = False
    
    def select(self, mouse):

        if self.rect.collidepoint(mouse):
            self.selected = True
            # upon selection, centralize
            self.rect.x = mouse[0] - self.sq_sz // 2
            self.rect.y = mouse[1] - self.sq_sz // 2

            # set offset for drag
            self.selected_offset_x = self.rect.x - mouse[0]
            self.selected_offset_y = self.rect.y - mouse[1]

            # print for debug
            print(f"Selected {self.__class__.__name__}")

    def drag(self, move):

        if self.selected:
            self.rect.x = move[0] + self.selected_offset_x
            self.rect.y = move[1] + self.selected_offset_y

    def update_history(self, board, history):

        px, py = self.grid_loc

        capture = board[py][px] or False

        if hasattr(self, "double_on_last"):
            special = self.double_on_last
        else:
            special = False

        move_dict = {
            "Name": self.__class__.__name__,
            "Move": self.grid_loc,
            "Number": len(history) + 1,
            "Capture": capture,
            "Special": special,
        }

        history.append(move_dict)

    @property
    def grid_loc(self):

        return self.pos[0] // self.sq_sz, self.pos[1] // self.sq_sz

    @abstractmethod
    def isLegal(self, board, proposed, **kwargs):
        raise NotImplementedError


class Pawn(Piece):
    def __init__(self, color, sq_sz):
        super().__init__("pawn", color, sq_sz)

        self.firstmove = True

        self.double_on_last = False
        
        # eventually change this to implement board switching
        if self.color == "black":
            self.direct = 1
        elif self.color == "white":
            self.direct = -1
    
    @property
    def promotion(self):
        return self.rect.y in [0,7]

    def isLegal(self, board, proposed, **kwargs):
        # what is the position on the board?
        legal = False

        history = kwargs.get("history")

        # give location of last move if last move was a pawn moving two squares
        if history:
            pawn_last_move = history[-1]["Move"] if history[-1]["Special"] else None
        else:
            pawn_last_move = None

        # get current and proposed grid locations
        prop_x, prop_y = tuple(i // self.sq_sz for i in proposed)
        current_x, current_y = self.grid_loc

        print(prop_x, prop_y)
        print(current_x, current_y)

        # possible forward moves
        moves = []
        single = (current_x, current_y + self.direct)
        double = (current_x, current_y + 2 * self.direct)

        # possible capture moves
        pos_captures = [
            (current_x + 1, current_y + self.direct),
            (current_x - 1, current_y + self.direct),
        ]

        captures = []
        en_passant = []
        for x, y in pos_captures:

            # condition that position is on board
            if 0 <= x <= 7 and 0 <= y <= 7:

                # add to acceptable captures if there is an opposing piece there
                if board[y][x] and (self.color not in str(board[y][x])):
                    captures.append((x, y))

                # if a pawn moved two squares on last move, check for en passant
                elif pawn_last_move:

                    opp_x, opp_y = pawn_last_move

                    ep_location = (opp_x, opp_y + self.direct)
                    # if capture location in captures, remove from captures and
                    # add to en_passant
                    if ep_location in pos_captures:

                        en_passant.append(ep_location)

        # remove a single space move if piece is present
        if not board[single[1]][single[0]]:
            moves.append(single)

            # add to moves the double move if first move and unblocked
            if self.firstmove and not board[double[1]][double[0]]:
                moves.append(double)

        # check for double move
        if (prop_x, prop_y) == double:
            self.double_on_last = True
        else:
            self.double_on_last = False

        # check if in moves and set legal if so
        if (prop_x, prop_y) in moves:
            legal = True
            self.firstmove = False

        # set capture flag if move is a capture
        if (prop_x, prop_y) in captures:
            legal = True
            self.capture = (prop_x, prop_y)

        # set en_passant
        elif (prop_x, prop_y) in en_passant:
            legal = True
            self.capture = pawn_last_move

        return legal

class Knight(Piece):
    """

    gives list of available moves and handles capturing
    """

    def __init__(self, color, sq_sz):
        super().__init__("knight", color, sq_sz)

        # define moves by possible change in grid number
        self.diffs = []
        self.diffs.extend(list(product([1, -1], [2, -2])))
        self.diffs.extend(list(product([2, -2], [1, -1])))

    def isLegal(self, board, proposed, **kwargs):
        legal = False

        # get current and proposed grid locations
        prop_x, prop_y = tuple(i // self.sq_sz for i in proposed)
        current_x, current_y = self.grid_loc

        print(prop_x, prop_y)
        print(current_x, current_y)

        moves = []
        for diff in self.diffs:
            x, y = diff
            p_x = current_x + x
            p_y = current_y + y
            if 0 <= p_x <= 7:
                if 0 <= p_y <= 7:
                    if self.color not in str(board[p_y][p_x]):
                        moves.append((p_x, p_y))

        if (prop_x, prop_y) in moves:
            legal = True
            if board[prop_y][prop_x]:
                self.capture = (prop_x, prop_y)

        return legal


class Bishop(Piece):
    """
    currently limits diagonal move without blocking piece on diagonal
    and checks if proposed move lands on own color piece
    note: doesn't yet handle capturing
    """

    def __init__(self, color, sq_sz):
        super().__init__("bishop", color, sq_sz)

    def isLegal(self, board, proposed, **kwargs):
        legal = False

        # get current and proposed grid locations
        prop_x, prop_y = tuple(i // self.sq_sz for i in proposed)
        current_x, current_y = self.grid_loc

        print(prop_x, prop_y)
        print(current_x, current_y)

        directs = [(1, -1), (-1, 1), (-1, -1), (1, 1)]
        moves = []

        for x, y in directs:
            for d in range(1, 9):
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
            if board[prop_y][prop_x]:
                self.capture = (prop_x, prop_y)

        return legal


class Rook(Piece):
    def __init__(self, color, sq_sz):
        super().__init__("rook", color, sq_sz)

    def isLegal(self, board, proposed, **kwargs):
        legal = False

        # get current and proposed grid locations
        prop_x, prop_y = tuple(i // self.sq_sz for i in proposed)
        current_x, current_y = self.grid_loc

        print(prop_x, prop_y)
        print(current_x, current_y)

        directs = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        moves = []

        for x, y in directs:
            for d in range(1, 9):
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
            if board[prop_y][prop_x]:
                self.capture = (prop_x, prop_y)

        return legal


class Queen(Piece):
    def __init__(self, color, sq_sz):
        super().__init__("queen", color, sq_sz)

    def isLegal(self, board, proposed, **kwargs):
        legal = False

        # get current and proposed grid locations
        prop_x, prop_y = tuple(i // self.sq_sz for i in proposed)
        current_x, current_y = self.grid_loc

        print(prop_x, prop_y)
        print(current_x, current_y)

        directs = [(0, -1), (0, 1), (-1, 0), (1, 0), (1, -1), (-1, 1), (-1, -1), (1, 1)]
        moves = []

        for x, y in directs:
            for d in range(1, 9):
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
            if board[prop_y][prop_x]:
                self.capture = (prop_x, prop_y)

        return legal


class King(Piece):
    def __init__(self, color, sq_sz):
        super().__init__("king", color, sq_sz)

    def isLegal(self, board, proposed, **kwargs):
        legal = False

        # get current and proposed grid locations
        prop_x, prop_y = tuple(i // self.sq_sz for i in proposed)
        current_x, current_y = self.grid_loc

        print(prop_x, prop_y)
        print(current_x, current_y)

        directs = [(0, -1), (0, 1), (-1, 0), (1, 0), (1, -1), (-1, 1), (-1, -1), (1, 1)]
        moves = []

        for x, y in directs:
            p_x = x + current_x
            p_y = y + current_y

            if not (0 <= p_x <= 7 and 0 <= p_y <= 7):
                continue

            elif self.color in str(board[p_y][p_x]):
                continue

            elif board[p_y][p_x]:
                moves.append((p_x, p_y))
                continue

            moves.append((p_x, p_y))

        if (prop_x, prop_y) in moves:
            legal = True
            if board[prop_y][prop_x]:
                self.capture = (prop_x, prop_y)

        return legal