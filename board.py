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

    white = 0b10000  # 8
    black = 0b01000  # 16


class Board:
    def __init__(self) -> None:
        self.squares = [0] * 64
        self.turn = Piece.white

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

        fen_board: str = fen_string.split(" ")[0]
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

        print(f"the start index {start_index} had the value of {piece}")
        print(f"the end index {end_index} had the value of {self.squares[end_index]} \n")

        if self.squares[start_index] == 0:
            return self.squares
        if self.squares[start_index] == self.squares[end_index]:
            return self.squares
        self.squares[start_index] = Piece.none
        self.squares[end_index] = piece

        return self.squares

    def accumulate_coordinates( self, coordinates: tuple[int, int], sq_size: int) -> None:
        if not hasattr(self, "start_coords") or self.start_coords is None:
            self.start_coords = coordinates
            return # First click: just select the start position
        else:
            end_coords = coordinates

            # Convert pixel positions to grid ranks/files
            start_x = self.start_coords[0] // sq_size
            start_y = 7 - (self.start_coords[1] // sq_size)

            end_x = end_coords[0] // sq_size
            end_y = 7 - (end_coords[1] // sq_size)

            # Convert to 0-63 indices
            start_index = start_y * 8 + start_x
            end_index = end_y * 8 + end_x
            if self.squares[start_index] == 0:
                self.start_coords = None
                return self.start_coords
            
            print(self.squares[start_index])
            print(self.squares[end_index])
            # Execute the move and reset selection
            self.make_move(start_index=start_index, end_index=end_index)
            self.start_coords = None

    def __str__(self) -> str:
        board_array = []

        for i, square in enumerate(self.squares,1 ):
            board_array.append(f"{square:>2}")

            if i % 8 == 0:
                board_array.append("\n")
            else:
                board_array.append(", ")

        return "".join(board_array)


def main():
    board: Board = Board()
    board.from_fen_to_board(fen_string="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR")
    print(board)


if __name__ == "__main__":
    main()
