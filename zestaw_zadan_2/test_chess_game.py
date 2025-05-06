import unittest
from chess_game import (
    generate_board,
    print_board,
    is_queen_threatening,
    find_threatening_queens,
    pos_to_chess_notation,
    chess_notation_to_pos,
    move_piece,
    remove_queen,
    get_empty_positions,
    print_threats,
    BOARD_SIZE
)

class TestChessFunctions(unittest.TestCase):
    def setUp(self):
        self.test_board = [
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', 'H', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', 'P', '.', '.', '.', '.'],
            ['.', '.', '.', '.', 'H', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', 'H', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.']
        ]
        self.pawn_pos = (3, 3)
        self.queens_pos = [(1, 1), (4, 4), (6, 6)]

    def test_is_queen_threatening(self):
        self.assertTrue(is_queen_threatening((1, 1), self.pawn_pos))
        self.assertTrue(is_queen_threatening((4, 4), self.pawn_pos))
        self.assertTrue(is_queen_threatening((3, 0), self.pawn_pos))
        self.assertTrue(is_queen_threatening((6, 6), self.pawn_pos))
        self.assertTrue(is_queen_threatening((0, 0), self.pawn_pos))
        self.assertFalse(is_queen_threatening((0, 7), self.pawn_pos))

    def test_find_threatening_queens(self):
        threatening = find_threatening_queens(self.pawn_pos, self.queens_pos)
        self.assertEqual(len(threatening), 3)
        self.assertIn((1, 1), threatening)
        self.assertIn((4, 4), threatening)
        self.assertIn((6, 6), threatening)

    def test_pos_conversion(self):
        self.assertEqual(pos_to_chess_notation((0, 0)), 'a8')
        self.assertEqual(pos_to_chess_notation((7, 7)), 'h1')
        self.assertEqual(chess_notation_to_pos('a8'), (0, 0))
        self.assertEqual(chess_notation_to_pos('h1'), (7, 7))
        self.assertIsNone(chess_notation_to_pos('i1'))
        self.assertIsNone(chess_notation_to_pos('a9'))

    def test_move_piece(self):
        new_pos = (2, 2)
        move_piece(self.test_board, self.pawn_pos, new_pos, 'P')
        self.assertEqual(self.test_board[3][3], '.')
        self.assertEqual(self.test_board[2][2], 'P')

    def test_remove_queen(self):
        self.assertTrue(remove_queen(self.test_board, self.queens_pos, (1, 1)))
        self.assertEqual(self.test_board[1][1], '.')
        self.assertNotIn((1, 1), self.queens_pos)
        self.assertFalse(remove_queen(self.test_board, self.queens_pos, (0, 0)))

if __name__ == '__main__':
    unittest.main()
