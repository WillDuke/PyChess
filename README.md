# PyChess

A project to build a working chess game with legal move, check, checkmate, dead position, etc. detection. The idea is to eventually pair this with a language model so that one can play against the model that has learned to play chess purely from the notated games from the FIDE database.

____

## Design

The game itself is built in PyGame. I have subclassed PyGame's `sprite` and `group` classes to make use of their collision and position tracking. The sprite images were freely available from [Wikimedia Commons](https://commons.wikimedia.org/wiki/Category:PNG_chess_pieces/Standard_transparent).

## Progress

- Created the game board 
    - The game board is a matrix on the backend that is used for identifying legal moves
    - defined `Group.get_board_position()` that creates a board from its component Pieces
- Imported sprites for each of the pieces
    - Resized sprites to fit board
- Created classes for each of the piece types that subclass a Piece class which handles updates
    - each class will have its own logic for checking whether a proposed move is possible
- Built logic to update board based on mouse click and drag
    - polls for mouse events and sends `MOUSEBUTTONUP`, `MOUSEBUTTONDOWN`, and `MOUSEMOTION` events to `update`
    - calling `update` on the Group passes the board along with any arguments to each piece
    - each piece can then use the board plus the proposed move to determine whether the move is acceptable
    - on MOUSEBUTTONUP, the piece snaps in if legal, otherwise position is reverted to last position
- Built logic that differentiates rect and board position
    - rect position updates with mouse dragging and makes use of built-in `Sprite` functionality
    - a separate attribute `pos` in each piece updates to a grid position only if the move is determined to be acceptable
- Added logic to "snap-in" pieces to grid if acceptable move

## TO DO

- Fix position attribute with proper getter/setter
    - set the position with a tuple of the pixel position
    - get_position and return a tuple of the board position (// sq_sz)
- Add logic for each piece to determine reachable squares
    - Pawn: No en passant or capturing
    - Knight: No capturing
    - Bishop: No capturing
    - Rook: No capturing
    - Queen: No capturing
    - King: Not Yet Started
- Add logic for capture detection:
    - one idea: need to raise a capture flag when a piece captures another
    - group update can drop any piece that is overlapping with no capture flag
- Add logic for alternating turns
- Add capture detection/handling
    - one method: update in piece determines whether the move for a given piece is available (i.e. in piece.available_moves)
    subclass defines available moves setter
    - each piece also has a method that checks whether the current move puts the opposing king in check
    - this method would have to check the whole board after the update
    - if check = True, raise a flag 
- Add en passant!
- Add check detection
    - if king's position is among all available moves, check!
    - also an option: check e.g. if white's king is in check after their move, move is illegal
        - this accounts for the possibility of leaving the king in check, moving the king into check, or moving another piece such that the king is in check
    - better idea: when looping through the pieces, check whether piece can reach the opposing king regardless of whether the piece is being moved (if so, set flag to TRUE) 
    - each piece also has a method that checks whether the current move puts the player's king in check
- Add checkmate detection
    - if king is threatened after all available moves for each piece, then checkmate
    -  idea: if I remove all possible moves that leave the king in check from the list of available moves and no possible moves remain, then checkmate
    - note: this leaves an issue: currently the board is only checked when one player moves a piece
- Add insufficient material detection
    - e.g. if each side only has a single knight, game cannot be won
- End Game and Reset
    - Detect win/draw/reset

## Feature Creepers

- Righthand panel with:
    - timer (?)
    - captured pieces (?)
    - moves played (?)
    - reset
    - undo move (?)