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
- Completed movement logic for all pieces for all "regular" moves (i.e. no en passant, check detection, or castling)
- Add capture handling -- `ChessSet` polls pieces for a capture flag and removes any pieces listed from the group
- Refactor so that factory method is part of `ChessSet` group rather than a separate class
- Added `history` attribute to `ChessSet`
    - tracks moves and records information about them 
- Added en passant
    - pawn receives history attribute from `ChessSet` class via update and checks whether an adjacent pawn moved two squares on its last move

## TO DO

- Add logic for each piece to determine reachable squares
    - Pawn: No promotion
    - Knight: Done
    - Bishop: Done
    - Rook: Done
    - Queen: Done
    - King: No castling, no check
- Add promotion
- Add castling
- Add check detection
    - if king's position is among all available moves, check!
    - also an option: check e.g. if white's king is in check after their move, move is illegal
        - this accounts for the possibility of leaving the king in check, moving the king into check, or moving another piece such that the king is in check
    - better idea: when looping through the pieces, check whether piece can reach the opposing king regardless of whether the piece is being moved (if so, set flag to TRUE) 
    - each piece also has a method that checks whether the current move puts the player's king in check
    - alternatively, I could move the process into the ChessSet.update method
        - first, loop through each piece and return True if selected piece can legally move to that position (ignoring check)
        - second, loop through all of the opposing pieces and return True if none of them can reach the king
        - if both are true, update the position
        - otherwise, revert
        - in this case, I would need to move the call to update history into update so that moves are only added if both checks are satisfied
        - third, get available moves for given piece and check if king's position is among them -- if so set check flag to True
- Add checkmate detection
    - if king is threatened after all available moves for each piece, then checkmate
    -  idea: if I remove all possible moves that leave the king in check from the list of available moves and no possible moves remain, then checkmate
    - note: this leaves an issue: currently the board is only checked when one player moves a piece
    - alternatively (continuing from above), if the check flag is thrown:
        - loop through all of kings moves -- are there any where it is not in check?
        - loop through every piece, check for each way of stopping the check
            - can I take the piece that is attacking the king?
            - can I put a piece between the attacking piece and the king?
- Add insufficient material detection
    - e.g. if each side only has a single knight, game cannot be won
- Add logic for alternating turns
- Add game menu
- End Game and Reset
    - Detect win/draw/reset

## Feature Creepers

- Righthand panel with:
    - timer (?)
    - captured pieces (?)
    - moves played (?)
    - reset
    - undo move (?)