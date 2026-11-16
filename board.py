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
                square_rays:dict[int,list] = {}

                for dir_offset, (dir_r, dir_c) in direction_deltas.items():
                    ray_squares:list = []
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
                # makes the selected piece different piece of the same color so 
                # people cannot attempt to capture their own piece
            # Execute the move and reset selection
            self.make_move(start_index=self.start_index, end_index=end_index)
            self.start_index = None

    def make_move(self, start_index: int, end_index: int) -> list[int]:
        """sets the start index piece to Piece.none and the end index piece to the start index piece
        with some added conditional checks"""
        piece = self.squares[start_index]
        if self.squares[start_index] == self.squares[end_index]: 
            print("couldnt make a move")
            return self.squares # return early if the start and end indecies are the same

        if end_index in self.generate_legal_moves(start_index): # checks if the piece is in legal_moves
            self.squares[start_index] = Piece.none # sets the start to none
            self.squares[end_index] = piece # sets the end to the start
        return self.squares

    def generate_legal_moves(self, index: int) -> list:
        piece = self.squares[index]
        if piece == Piece.none: 
            return []

        piece_type = Piece.piece_type(piece=piece)
        piece_color = Piece.color(piece=piece)
        
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
                raise NotImplementedError
        return []


def get_knight_moves(squares, index) -> list[int]:
    legal_moves = []
    piece = squares[index]
    row = index // 8
    col = index % 8
    # covers all the L shape possibilities
    knight_offsets = [(1,2),(-1,2), (2,1),(-2,1), (2,-1),(-2,-1),(1,-2),(-1,-2),]

    for row_offset,col_offset in knight_offsets:
        offset_row = row + row_offset # applying offsets
        offset_col = col + col_offset
        if 0<=offset_row < 8 and 0<=offset_col < 8: # bound checks
            new_index = offset_row * 8 + offset_col
            target_piece = squares[new_index]
            if Piece.color(target_piece) != Piece.color(piece): # checks to make sure the pieces are different colors
                legal_moves.append(new_index)

    return legal_moves

def get_pawn_moves(squares: list[int], index: int) -> list[int]:
    legal_moves = []
    piece = squares[index]
    row = index // 8
    col = index % 8
    direction = 1 if Piece.iscolor(piece,Piece.white) else -1
    start_row = 1 if Piece.iscolor(piece,Piece.white) else 6

    one_step_row = row + direction
    if 0 <= one_step_row < 8:
        new_index = one_step_row * 8 + col
        if squares[new_index] == Piece.none:
            legal_moves.append(new_index)
            if row == start_row:
                two_step_row = row + direction + direction
                if 0 <= two_step_row < 8:
                    new_index_two = two_step_row * 8 + col
                    if squares[new_index_two] == Piece.none:
                        legal_moves.append(new_index_two)


    capture_row = row + direction
    if 0 <= capture_row < 8:
        for capture_direction in (-1, 1):
            capture_col = col + capture_direction
            if 0 <= capture_col < 8:
                capture_index = capture_row * 8 + capture_col
                if squares[capture_index] != Piece.none and Piece.color(squares[capture_index]) != Piece.color(piece):
                    legal_moves.append(capture_index)

    return legal_moves


def get_sliding_moves(squares: list[int], index: int, directions: list[int]) -> list[int]:
    # dict[int,dict[int,list[int]]]
    legal_moves: list = []
    piece: int = squares[index]
    piece_color: int = Piece.color(piece=piece)
    
    sliding_moves = Piece._SLIDING_MOVES
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
