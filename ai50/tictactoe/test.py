from tictactoe import *
import unittest

board_empty = [[EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY],
               [EMPTY, EMPTY, EMPTY]]
board1 = [[EMPTY, EMPTY, EMPTY], [EMPTY, X, EMPTY], [EMPTY, EMPTY, EMPTY]]
board2 = [[EMPTY, EMPTY, O], [EMPTY, X, EMPTY], [EMPTY, EMPTY, EMPTY]]
board3 = [[EMPTY, X, O], [EMPTY, X, EMPTY], [EMPTY, EMPTY, EMPTY]]
board_full = [[X, X, O], [O, X, X], [X, O, O]]
board_X_win = [[X, X, O], [O, X, X], [O, X, O]]
board_O_win = [[O, EMPTY, EMPTY], [O, X, X], [O, X, EMPTY]]


class Test(unittest.TestCase):
    def test_player(self):
        self.assertEqual(player(board_empty), X)
        self.assertEqual(player(board1), O)
        self.assertEqual(player(board2), X)

    def test_board_cell_taken(self):
        self.assertRaises(InputError, result, board_full, (1, 1))

    def test_actions(self):
        self.assertEqual(actions(board3),
                         set([(0, 0), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)]))
        self.assertEqual(actions(board_full), set([]))

    def test_results(self):
        self.assertEqual(
            result(board3, (1, 0)),
            [[EMPTY, "X", "O"], ["O", "X", EMPTY], [EMPTY, EMPTY, EMPTY]],
        )

    def test_winner(self):
        self.assertEqual(winner(board_full), EMPTY)
        self.assertEqual(winner(board_empty), EMPTY)
        self.assertEqual(winner(board_X_win), X)
        self.assertEqual(winner(board_O_win), O)

    def test_terminal(self):
        self.assertTrue(terminal(board_X_win))
        self.assertTrue(terminal(board_O_win))
        self.assertTrue(terminal(board_full))
        self.assertFalse(terminal(board_empty))
        self.assertFalse(terminal(board3))

    def test_utility(self):
        self.assertEqual(utility(board_X_win), 1)
        self.assertEqual(utility(board_O_win), -1)
        self.assertEqual(utility(board_empty), 0)
        self.assertEqual(utility(board_full), 0)
        self.assertEqual(utility(board3), 0)

    def test_minimax(self):
        self.assertEqual(minimax(board_full), None)
        self.assertEqual(minimax(board_X_win), None)
        self.assertEqual(minimax(board_O_win), None)


if __name__ == "__main__":
    unittest.main()
