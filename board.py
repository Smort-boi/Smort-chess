"""
i need a class method that can change the piece position
"""


class Piece:
    none = 0b00000
    king = 0b00001
    pawn = 0b00010
    knight = 0b00011
    bishop = 0b00100
    rook = 0b00101
    queen = 0b00110

    white = 0b01000
    black = 0b10000


class Board:
    def __init__(self) -> None:
        pass

    def from_fen_to_board(self, fen_string: str):  # -> list
        square = [0] * 64
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
                    square[rank * 8 + file] = piece_color | piece_type
                    file += 1
        return square


def main():
    board: Board = Board()
    print(
        board.from_fen_to_board(
            fen_string="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"
        )
    )


if __name__ == "__main__":
    main()
