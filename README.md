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
- Add logic for each piece to determine reachable squares
    - Pawn: In Progress
    - Knight: In Progress
    - Bishop: In Progress
    - Rook: Not Yet Started
    - Queen: Not Yet Started
    - King: Not Yet Started
- Add logic for alternating turns
- Add capture detection/handling
    - Add en passant!
- Add check detection
    - if king's position is among all available moves, check!
- Add checkmate detection
    - if king is threatened after all available moves for each piece, then checkmate
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

info I need to determine legal move:
piece that just moved, position of all other pieces
question: how can I update the position of all of the pieces?
    idea: revert to using one group for all of the pieces
    define a function called get_positions() within group that creates a board 
    and sends that board to the updates of all of the sprites
    each sprite has an is_legal_move() method that can use the board to check
    whether the proposed move is legal
    if it is, update the sprites position, otherwise send it back to its original position
calling update from group will send the latest board position to each sprite 
so the sprites keep track of their position

need a separate position attribute that doesn't when the piece is dragged

note: need to create getter and setter methods for the position:
    set the position with a tuple of the pixel position
    get_position and return a tuple of the board position (// sq_sz)
note: need to raise a capture flag when a piece captures another
group update can drop any piece that is overlapping with no capture flag

how to set up move rules:
I need to set up check detection eventually --
    at that point I will need to know the available squares for all of the opposing pieces
    every piece has a method that provides the available moves given the current board
    piece.reachable(board, move) returns list of available squares
    in update, revert position if square not in reachable
Then, for every move, I loop through the opponents pieces and check whether the proposed (or current)
position is threatened
check detection: prevent the move if move would be put king in check
ensure king is not in check

need to handle capturing!
step 1) update in piece determines whether the move for a given piece is available (i.e. in piece.available_moves)
    subclass defines available moves setter
each piece also has a method that checks whether the current move puts the opposing king in check
    this method would have to check the whole board after the update
    if check = True, raise a flag 
each piece also has a method that checks whether the current move puts the player's king in check
    
step 2) compute the new board for the given move
step 3) determine from the new board whether the king is in check


OK new plan:

spread out the function of update to a set of functions in set class:
 first method: update_sprite
    provides info about 