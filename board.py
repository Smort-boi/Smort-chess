"""
i need a class method that can change the piece position
"""


class Piece:
    none = 0b00000  # 0
    king = 0b00001  # 1
    pawn = 0b00010  # 2
    knight = 0b00011  # 3
    bishop = 0b00100  # 4
    rook = 0b00101  # 5
    queen = 0b00110  # 6

    black = 0b01000  # 8
    white = 0b10000  # 16


class Board:
    def __init__(self) -> None:
        self.squares: list[int] = [Piece.none] * 64
        self.turn: int | None = Piece.none

    def toggle_turn(self) -> None:
        self.turn = Piece.black if self.turn == Piece.white else Piece.white

    def from_fen_to_board(self, fen_string: str) -> list[int]:
        """
        If this function gets any more responsibilties i will split it into 2 or more
        """
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
            turn = fen_string.split(" ")[1].strip()
        except IndexError:
            print(
                "Invalid fen string, the string must contain the board state and the turn, using white as a fallback"
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

    def make_move(self, start_index: int, end_index: int) -> list[int]:
        piece = self.squares[start_index]

        if self.squares[start_index] == self.squares[end_index]:
            return self.squares
        self.squares[start_index] = Piece.none
        self.squares[end_index] = piece

        return self.squares

    def accumulate_coordinates(self, coordinates: tuple[int, int], sq_size: int) -> None:
        """
        This code needs refacoring
        """
        if not hasattr(self, "start_coords") or self.start_coords is None:
            start_x = coordinates[0] // sq_size
            start_y = 7 - (coordinates[1] // sq_size)

            start_index = start_y * 8 + start_x

            if self.squares[start_index] != Piece.none:
                self.start_coords = start_index
            return  # First click: just select the start position
        else:
            end_coords = coordinates

            # Convert pixel positions to grid ranks/files

            end_x = end_coords[0] // sq_size
            end_y = 7 - (end_coords[1] // sq_size)

            # Convert to 0-63 indices
            end_index = end_y * 8 + end_x

            # Execute the move and reset selection
            self.make_move(start_index=self.start_coords, end_index=end_index)
            self.start_coords = None

    def __str__(self) -> str:
        board_array = []
        for index, square in enumerate(self.squares, 1):
            pass
        return "".join(board_array)


def main():
    board: Board = Board()
    board.from_fen_to_board(fen_string="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR b")
    print(board)


if __name__ == "__main__":
    main()
