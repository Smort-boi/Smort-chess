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
    square = [0 for _ in range(64)]
    square[0] = Piece.bishop | Piece.white


def main():
    board = Board()
    print(board.square)


if __name__ == "__main__":
    main()
