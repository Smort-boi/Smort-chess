"""
"""


class Piece:
    COLOR_MASK = 0b11000
    PIECE_MASK = 0b00111

    none = 0b00000  # 0
    king = 0b00001  # 1
    pawn = 0b00010  # 2
    knight = 0b00011  # 3
    bishop = 0b00100  # 4
    rook = 0b00101  # 5
    queen = 0b00110  # 6

    black = 0b01000  # 8
    white = 0b10000  # 16

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
        return ((piece & Piece.COLOR_MASK) == color)


class Board:
    def __init__(self) -> None:
        # initializing variables
        self.squares: list[int] = [Piece.none] * 64
        self.turn: int = Piece.none

    def __str__(self) -> str:
        board_array = []
        for index, square in enumerate(self.squares, 1):
            board_array.append(f"{square:>2},")
            if index % 8 == 0:
                board_array.append("\n")

        match self.turn:
            case Piece.black:
                turn_str = "Black"
            case Piece.white:
                turn_str = "White"
            case Piece.none | _:
                turn_str = "This board has not been initiated yet, Use the 'from_fen_to_board' method to initiate"

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
            "q": Piece.queen
        }
        try:
            fen_board: str = fen_string.split(" ")[0].strip()
            turn = fen_string.split(" ")[1].strip().lower()
        except IndexError:
            print(
                f"Invalid fen_string: {fen_string}: missing board state or turn."
            )
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
        y = 7 - (coordinates[1] // sq_size)
        return y * 8 + x

    def accumulate_coordinates(self, coordinates: tuple[int, int], sq_size: int) -> None:
        """
        this code is satisfactory
        """
        if not hasattr(self, "start_index") or self.start_index is None:
            start_index = self._pixels_to_coordinates(coordinates=coordinates, sq_size=sq_size)
            if self.squares[start_index] != Piece.none:
                self.start_index = start_index
            return  # First click: just select the start position
        else:
            end_index = self._pixels_to_coordinates(coordinates=coordinates, sq_size=sq_size)
            # Execute the move and reset selection
            self.make_move(start_index=self.start_index, end_index=end_index)
            self.start_index = None

    def make_move(self, start_index: int, end_index: int) -> list[int]:

        piece = self.squares[start_index]

        if self.squares[start_index] == self.squares[end_index]:
            return self.squares
        if end_index in self.generate_legal_moves(start_index):
            self.squares[start_index] = Piece.none
            self.squares[end_index] = piece
        # return self.squares
        return self.squares

    def generate_legal_moves(self, index: int) -> list:
        piece = self.squares[index]
        if piece is Piece.none:
            return []

        piece_type = Piece.piece_type(piece=piece)
        piece_color = Piece.color(piece=piece)

        if piece_type == Piece.knight:
            return self.get_knight_moves(index)
        elif piece_type == Piece.pawn:
            return self.get_pawn_moves(index)

        return []

    def get_knight_moves(self, index) -> list[int]:
        row = index // 8
        col = index % 8
        legal_moves = []

        current_piece = self.squares[index]
        current_color = Piece.color(current_piece)  # Extracts the color bits (black or white)

        # All 8 possible L-shaped (row_offset, col_offset) jumps for a knight
        knight_offsets = [
            (-2, -1), (-2, 1),
            (-1, -2), (-1, 2),
            (1, -2), (1, 2),
            (2, -1), (2, 1),
        ]

        for r_off, c_off in knight_offsets:
            new_row = row + r_off
            new_col = col + c_off

            # 1. Check if the destination is within board bounds (0 to 7)
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                target_index = new_row * 8 + new_col
                target_piece = self.squares[target_index]

                # 2. Check if square is empty
                if target_piece == Piece.none:
                    legal_moves.append(target_index)
                else:
                    # 3. Check if it's an enemy piece (different color)
                    if not Piece.iscolor(piece=target_piece,color=current_color):
                        legal_moves.append(target_index)

        return legal_moves

    def get_pawn_moves(self,index):
        raise NotImplementedError("the pawn moves are not implemented yet")
        row = index // 8
        col = index % 8
        legal_moves = []

        current_piece = self.squares[index]
        current_color = Piece.color(current_piece)  # Extracts the color bits (black or white)

        return legal_moves

def main():
    board: Board = Board()
    board.from_fen_to_board(fen_string="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR b")
    print(board)


if __name__ == "__main__":
    main()
