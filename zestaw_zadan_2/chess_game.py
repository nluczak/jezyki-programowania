import random
from typing import List, Tuple, Optional, Set


Position = Tuple[int, int]
Board = List[List[str]]
BOARD_SIZE = 8

# k - liczba hetmanów

def generate_board(k: int) -> Tuple[Board, Position, List[Position]]:
    """Generowanie tabeli"""
    if not 0 <= k <= 5:
        raise ValueError("Liczba hetmanów musi być między 0 a 5")

    board = [['.' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    positions = [(i, j) for i in range(BOARD_SIZE) for j in range(BOARD_SIZE)]
    random.shuffle(positions)

    pawn_pos = positions.pop()
    board[pawn_pos[0]][pawn_pos[1]] = 'P'

    queens_pos = []
    for _ in range(k):
        if not positions:
            raise ValueError("Brak dostępnych pozycji")
        queen_pos = positions.pop()
        board[queen_pos[0]][queen_pos[1]] = 'H'
        queens_pos.append(queen_pos)

    return board, pawn_pos, queens_pos


def print_board(board: Board) -> None:
    print("  a b c d e f g h")
    print(" +-----------------+")
    for i, row in enumerate(board):
        print(f"{BOARD_SIZE - i}| {' '.join(row)} |{BOARD_SIZE - i}")
    print(" +-----------------+")
    print("  a b c d e f g h")


def is_queen_threatening(queen_pos: Position, pawn_pos: Position) -> bool:
    q_row, q_col = queen_pos
    p_row, p_col = pawn_pos
    return (q_row == p_row or q_col == p_col or
            abs(q_row - p_row) == abs(q_col - p_col))


def find_threatening_queens(pawn_pos: Position, queens_pos: List[Position]) -> List[Position]:
    return [q for q in queens_pos if is_queen_threatening(q, pawn_pos)]


def pos_to_chess_notation(pos: Position) -> str:
    row, col = pos
    return f"{chr(97 + col)}{BOARD_SIZE - row}"


def chess_notation_to_pos(chess_pos: str) -> Optional[Position]:
    if (len(chess_pos) != 2 or not chess_pos[0].islower()
            or not chess_pos[1].isdigit()):
        return None

    col = ord(chess_pos[0]) - ord('a')
    row = BOARD_SIZE - int(chess_pos[1])

    if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
        return (row, col)
    return None


def move_piece(board: Board, old_pos: Position, new_pos: Position, piece: str) -> Position:
    row, col = old_pos
    board[row][col] = '.'
    new_row, new_col = new_pos
    board[new_row][new_col] = piece
    return new_pos


def remove_queen(board: Board, queens_pos: List[Position], queen_pos: Position) -> bool:
    if queen_pos in queens_pos:
        board[queen_pos[0]][queen_pos[1]] = '.'
        queens_pos.remove(queen_pos)
        return True
    return False


def get_empty_positions(board: Board) -> List[Position]:
    return [(i, j) for i in range(BOARD_SIZE) for j in range(BOARD_SIZE)
            if board[i][j] == '.']


def print_threats(pawn_pos: Position, queens_pos: List[Position]) -> None:
    threatening = find_threatening_queens(pawn_pos, queens_pos)
    if threatening:
        print("Pionek może zostać zbity przez hetmana na pozycjach:")
        for q_pos in threatening:
            print(f"- {pos_to_chess_notation(q_pos)}")
    else:
        print("Pionek nie jest zagrożony przez żadnego hetmana.")


def main():
    try:
        k = int(input("Podaj liczbę hetmanów (0-5): "))
        board, pawn_pos, queens_pos = generate_board(k)

        while True:
            print("\nAktualna plansza:")
            print_board(board)
            print(f"\nPozycja pionka: {pos_to_chess_notation(pawn_pos)}")
            print(f"Pozycje hetmanów: {[pos_to_chess_notation(q) for q in queens_pos]}")

            print_threats(pawn_pos, queens_pos)

            print("\nOpcje:")
            print("1. Wylosuj nową pozycję pionka")
            print("2. Usuń hetmana")
            print("3. Zakończ program")

            choice = input("Wybierz opcję (1-3): ").strip()

            if choice == '1':
                empty_pos = get_empty_positions(board)
                if not empty_pos:
                    print("Brak dostępnych pozycji!")
                    continue
                new_pos = random.choice(empty_pos)
                pawn_pos = move_piece(board, pawn_pos, new_pos, 'P')
                print(f"Nowa pozycja pionka: {pos_to_chess_notation(pawn_pos)}")
            elif choice == '2':
                if not queens_pos:
                    print("Brak hetmanów do usunięcia!")
                    continue
                chess_pos = input("Podaj pozycję hetmana do usunięcia (np. 'a1'): ").lower()
                queen_pos = chess_notation_to_pos(chess_pos)
                if queen_pos is None:
                    print("Nieprawidłowa pozycja")
                elif remove_queen(board, queens_pos, queen_pos):
                    print(f"Usunięto hetmana na {chess_pos}.")
                else:
                    print(f"Na {chess_pos} nie ma hetmana!")
            elif choice == '3':
                print("Koniec programu.")
                break
            else:
                print("Nieprawidłowy wybór!")

    except ValueError as e:
        print(f"Błąd: {e}")

if __name__ == "__main__":
    main()