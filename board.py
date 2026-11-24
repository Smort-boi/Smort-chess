from dataclasses import dataclass
"""
The Board module handles all the move legality and board state
"""

class Piece:
    """
    Handles all the attributes associated with the Pieces which are stored on the board
    """
    COLOR_MASK = 0b11000
    PIECE_MASK = 0b00111

    none: int = 0b00000  # 0
    king: int = 0b00001  # 1
    pawn: int = 0b00010  # 2
    knight: int = 0b00011  # 3
    bishop: int = 0b00100  # 4
    rook: int = 0b00101  # 5
    queen: int = 0b00110  # 6

    black:int = 0b01000  # 8
    white:int = 0b10000  # 16

    @staticmethod
    def _pre_load_sliding_moves() -> dict[int, dict[int, list[int]]]:
        direction_deltas:dict[int,tuple[int,int]] = {
            -8: (-1,  0), # North
            8: ( 1,  0), # South
            1: ( 0,  1), # East
            -1: ( 0, -1), # West
            -7: (-1,  1), # North-East
            -9: (-1, -1), # North-West
            9: ( 1,  1), # South-East
            7: ( 1, -1), # South-West
        }
        rays:dict[int,dict[int,list[int]]] = {}
        for square in range(64):
            row, col = divmod(square, 8)
            square_rays: dict[int, list] = {}
            for dir_offset, (dir_r, dir_c) in direction_deltas.items():
                ray_squares: list = []
                curr_row, curr_col = row, col

                while True:
                    curr_row += dir_r
                    curr_col += dir_c
                    if not (0 <= curr_row < 8 and 0 <= curr_col < 8):
                        break

                    ray_squares.append(curr_row * 8 + curr_col)
                square_rays[dir_offset] = ray_squares
            rays[square] = square_rays

        return rays

    _SLIDING_MOVES:dict[int, dict[int, list[int]]] = _pre_load_sliding_moves()

    @staticmethod
    def color(piece: int) -> int:
        if piece == 0:
            return 0
        """returns the color of the current piece (piece = self.squares[index])"""
        return piece & Piece.COLOR_MASK

    @staticmethod
    def piece_type(piece: int) -> int:
        """returns the type of the current piece (piece = self.squares[index])"""
        return piece & Piece.PIECE_MASK

    @staticmethod
    def iscolor(piece: int, color: int) -> bool:
        """checks if the current piece is the same as the given color (piece = self.squares[index])"""
        return (piece & Piece.COLOR_MASK) == color


class Board:
    """
    Handles all the data of the board, such as locations, 
    initializing with fen strings and making moves.
    although the legality is passed on to functions outside the class
    """
    def __init__(self) -> None:
        # initializing variables
        self.squares: list[int] = [Piece.none] * 64
        self.turn: int = Piece.none
        self.move_history:list[tuple[int,int,int,int]] = []

    def __str__(self) -> str:
        board_array = []
        for i in range(len(self.squares) - 1, -1, -1):
            square = self.squares[i]
            index = len(self.squares) - i

            board_array.append(f"{square:>2},")
            if index % 8 == 0:
                board_array.append("\n")

        match self.turn:
            case Piece.black:
                turn_str = "Black"
            case Piece.white:
                turn_str = "White"
            case Piece.none :
                turn_str = "This board has not been initiated yet, Use the 'from_fen_to_board' method to initiate"
            case _:
                raise ValueError(f"Unexpected turn value: {self.turn}")

        board_array.append(f"Current turn is {turn_str}")
        return "".join(board_array)

    def toggle_turn(self) -> None:
        self.turn = Piece.black if self.turn == Piece.white else Piece.white

    def from_fen_to_board(self, fen_string: str) -> list[int]:
        piece_type_from_symbol = {
            "k": Piece.king,
            "p": Piece.pawn,
            "n": Piece.knight,
            "b": Piece.bishop,
            "r": Piece.rook,
            "q": Piece.queen,
        }
        try:
            fen_board: str = fen_string.split(" ")[0].strip()
            turn = fen_string.split(" ")[1].strip().lower()
        except IndexError:
            print(f"Invalid fen_string: {fen_string}: missing board state or turn.")
            return self.squares

        self.turn = Piece.black if turn == "b" else Piece.white

        file: int = 0
        rank: int = 7
        for char in fen_board:
            if char == "/":
                file = 0
                rank -= 1
            else:
                if char.isdigit():
                    file += int(char)
                else:
                    piece_color = Piece.white if (char.isupper()) else Piece.black
                    piece_type = piece_type_from_symbol[char.lower()]
                    self.squares[rank * 8 + file] = piece_color | piece_type
                    file += 1
        return self.squares

    @staticmethod
    def _pixels_to_coordinates(coordinates: tuple[int, int], sq_size: int) -> int:
        x = coordinates[0] // sq_size
        y = 7 - (coordinates[1] // sq_size)  # row gets reversed to match the chess board setup. 
        return (y * 8 + x)

    def accumulate_coordinates(self, coordinates: tuple[int, int], sq_size: int) -> None:
        """This code is decent"""
        if not hasattr(self, "start_index") or self.start_index is None:
            start_index = self._pixels_to_coordinates(coordinates=coordinates, sq_size=sq_size)
            if self.squares[start_index] != Piece.none:
                self.start_index = start_index
            return  # First click: just select the start position
        else:
            end_index = self._pixels_to_coordinates(coordinates=coordinates, sq_size=sq_size)
            if Piece.color(self.squares[end_index]) == Piece.color(self.squares[self.start_index]):
                self.start_index = end_index
                return
            # if Piece.color(self.squares[start_index]) != 
                # makes the selected piece different piece of the same color so 
                # people cannot attempt to capture their own piece
            # Execute the move and reset selection
            self.make_move(start_index=self.start_index, end_index=end_index)
            self.start_index = None

    def undo_move(self)->list[int]|None:
        """Undoes the latest move """
        # this requires no legal move checking since the 
        # moves have already made a legal pathway for this function to undo
        if not self.move_history:
            return self.squares

        start_index,end_index,squishing_piece,squished_piece = self.move_history.pop(-1)
        piece = self.squares[end_index]

        self.squares[end_index] = squished_piece
        self.squares[start_index] = piece
        
        self.toggle_turn()
        return self.squares

    def make_move(self, start_index: int, end_index: int) -> list[int] | None:
        """sets the start index piece to Piece.none and the end index piece to the start index piece
        with some added conditional checks"""
        if start_index == end_index: 
            return self.squares # return early if the start and end indecies are the same
 
        # return early if given move is not in the list of legal moves
        if end_index not in self.generate_legal_moves(start_index):            
            return self.squares
        
        start_piece = self.squares[start_index] # caching
        end_piece = self.squares[end_index]


        self.squares[start_index] = Piece.none # start set to none
        self.squares[end_index] = start_piece # end set to the cached piece

        # unmake move if in check
        if self._is_king_in_check():
            self.squares[end_index] = end_piece
            self.squares[start_index] = start_piece
            #-temp-----------------------------------------------------------
            king_color = "white" if self.turn == Piece.white else "black"
            print(f"{king_color} king is in check!")
            #-temp-----------------------------------------------------------
            return self.squares

        self.move_history.append((start_index,end_index,start_piece,end_piece))
        self.toggle_turn()

        return self.squares

    def generate_legal_moves(self, index: int) -> list:
        piece = self.squares[index]
        piece_type = Piece.piece_type(piece=piece)
        piece_color = Piece.color(piece=piece)
        if piece == Piece.none: 
            return []
        if piece_color != self.turn:
            return []

        match piece_type:
            case Piece.knight:
                return get_knight_moves(squares=self.squares, index=index)
            case Piece.pawn:
                return get_pawn_moves(squares=self.squares, index=index)
            case Piece.rook:
                return get_sliding_moves(squares=self.squares,index=index,directions=[-8,8,-1,1])
            case Piece.bishop:
                return get_sliding_moves(squares=self.squares,index=index,directions=[-7,7,-9,9])
            case Piece.queen:
                return get_sliding_moves(squares=self.squares,index=index,directions=[-8,8,-1,1,-7,7,-9,9])
            case Piece.king:
                return get_king_moves(squares=self.squares,index=index)
        return []

    def _is_king_in_check(self) -> bool:
        king_piece = self.turn | Piece.king # reconstructs the king piece
        opponent = self.turn ^ Piece.COLOR_MASK
        index = self.squares.index(king_piece)

        direction_map = {
            -8: [opponent | Piece.rook, opponent | Piece.queen],
            8: [opponent | Piece.rook, opponent | Piece.queen],
            1: [opponent | Piece.rook, opponent | Piece.queen],
            -1: [opponent | Piece.rook, opponent | Piece.queen],
            -7: [opponent | Piece.bishop, opponent | Piece.queen],
            7: [opponent | Piece.bishop, opponent | Piece.queen],
            -9: [opponent | Piece.bishop, opponent | Piece.queen],
            9: [opponent | Piece.bishop, opponent | Piece.queen],
        }
        for direction,valid_piece_type in direction_map.items():
            sliding_moves = get_sliding_moves(self.squares,index,[direction])
            for sliding_move in sliding_moves: 
                if self.squares[sliding_move] in valid_piece_type:
                    return True
        
        for knight_square in get_knight_moves(squares=self.squares,index=index):
            if self.squares[knight_square] == opponent|Piece.knight:
                return True
        
        for pawn_move in get_pawn_moves(squares=self.squares,index=index):
            if self.squares[pawn_move] == opponent|Piece.pawn:
                return True


        return False


def get_knight_moves(squares, index) -> list[int]:
    legal_moves: list[int] = []
    piece: int = squares[index]
    row: int = index // 8
    col: int = index % 8
    # covers all the L shape possibilities
    knight_offsets:list[tuple[int,int]] = [(1,2),(-1,2), (2,1),(-2,1), (2,-1),(-2,-1),(1,-2),(-1,-2),]

    for row_offset,col_offset in knight_offsets:
        offset_row: int = row + row_offset  # applying offsets
        offset_col: int = col + col_offset

        if 0<=offset_row < 8 and 0<=offset_col < 8: # bound checks
            new_index = offset_row * 8 + offset_col
            target_piece = squares[new_index]

            if Piece.color(target_piece) != Piece.color(piece): # checks to make sure the pieces are different colors
                legal_moves.append(new_index)

    return legal_moves

def get_pawn_moves(squares: list[int], index: int) -> list[int]:
    legal_moves: list[int] = []
    piece: int = squares[index]
    row: int = index // 8
    col: int = index % 8

    direction: int = 1 if Piece.iscolor(piece, Piece.white) else -1
    start_row: int = 1 if Piece.iscolor(piece, Piece.white) else 6

    target_rows = [row + direction]

    if row == start_row:
        target_rows.append(row + direction*2)

    for target_row in target_rows:
        if not (0<=target_row<8):
            break

        target_index = target_row * 8 + col

        if squares[target_index] == Piece.none:
            legal_moves.append(target_index)


    capture_row = row + direction

    if 0 <= capture_row < 8:

        for capture_direction in (-1, 1):
            capture_col = col + capture_direction
           
            if 0 <= capture_col < 8:
                capture_index = capture_row * 8 + capture_col

                if squares[capture_index] != Piece.none and Piece.color(squares[capture_index]) != Piece.color(piece):
                    legal_moves.append(capture_index)

    return legal_moves

def get_king_moves(squares: list[int], index: int) -> list[int]:
    legal_moves: list[int] = []
    piece: int = squares[index]
    row: int = index // 8
    col: int = index % 8

    king_offsets:list[tuple[int,int]] = [(0,1),(1,0),(1,1),(1,-1),(-1,1),(0,-1),(-1,0),(-1,-1)]

    for row_offset, col_offset in king_offsets:
        offset_row = row + row_offset
        offset_col = col + col_offset

        if 0<=offset_row < 8 and 0<=offset_col < 8: # bound checks
            new_index = offset_row * 8 + offset_col
            target_piece = squares[new_index]
            
            if Piece.color(target_piece) != Piece.color(piece):
                legal_moves.append(new_index)

    return legal_moves


def get_sliding_moves(squares: list[int], index: int, directions: list[int]) -> list[int]:
    # dict[int,dict[int,list[int]]]
    legal_moves: list[int] = []
    piece: int = squares[index]
    piece_color: int = Piece.color(piece=piece)

    sliding_moves:dict[int,dict[int,list[int]]] = Piece._SLIDING_MOVES

    for direction in directions:
        ray_indices = sliding_moves[index][direction]
        for ray_index in ray_indices:
            target_piece = squares[ray_index]

            if target_piece != Piece.none:
                if Piece.color(piece=target_piece) != piece_color:
                    legal_moves.append(ray_index)
                break
            legal_moves.append(ray_index)

    return legal_moves

def main() -> None:
    board: Board = Board()
    board.from_fen_to_board(fen_string="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR b")
    print(board)


if __name__ == "__main__":
    main()
