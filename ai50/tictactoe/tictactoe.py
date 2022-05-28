"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


class Error(Exception):
    """Base class for exceptions in this module."""

    pass


class InputError(Error):
    """Exception raised for errors in the input.

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    flattened_board = [cell for row in board for cell in row]

    # Initial board state => X's move
    if len(set(flattened_board)) == 1:
        return X

    # Non-initial state conditions
    if flattened_board.count(EMPTY) < 9 and flattened_board.count(
            O) >= flattened_board.count(X):
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = [(i, j) for i in range(len(board)) for j in range(len(board[i]))
               if board[i][j] is EMPTY]
    return set(actions)


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # Make deep copy of board to return
    new_board = copy.deepcopy(board)

    # Only copy player value into space if it is EMPTY
    if board[action[0]][action[1]] is EMPTY:
        new_board[action[0]][action[1]] = player(board)
        return new_board
    else:
        raise InputError(action, "Cell already occupied!")


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    # Reorient boards for non-horizontal wins
    transposed_board = list(zip(*board))
    diagonals = [
        [row[i] for i, row in enumerate(board)],
        [row[-i - 1] for i, row in enumerate(board)],
    ]

    # Horizontal and vertical wins
    for orientation in [board, transposed_board, diagonals]:
        for trio in orientation:
            if not any(cell is EMPTY
                       for cell in trio) and all(cell == trio[0]
                                                 for cell in trio):
                return X if trio[0] == X else O

    # Return None if cat's game or unfinished
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    return winner(board) is not None or actions(board) == set([])


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0


def max_utility(board, alpha=-math.inf, beta=math.inf):
    """
    Returns the maximum utility from a game state
    """
    # Base case
    if terminal(board):
        return utility(board)

    # Recursive case
    optimal_utility = -math.inf
    for move in actions(board):
        move_utility = min_utility(result(board, move), alpha, beta)
        optimal_utility = max(optimal_utility, move_utility)
        if move_utility >= beta:
            return move_utility
        alpha = max(alpha, move_utility)

    return optimal_utility


def min_utility(board, alpha=-math.inf, beta=math.inf):
    """
    Returns the minimum utility from a game state
    """
    # Base case
    if terminal(board):
        return utility(board)

    # Recursive case
    optimal_utility = math.inf
    for move in actions(board):
        move_utility = max_utility(result(board, move), alpha, beta)
        optimal_utility = min(optimal_utility, move_utility)
        if move_utility <= alpha:
            return move_utility
        beta = min(beta, move_utility)

    return optimal_utility


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    if terminal(board):
        return None

    # X's logic
    if player(board) == X:
        optimal_utility = -math.inf
        for move in actions(board):
            # Opponent will be attempting to minimize utilties
            move_utility = min_utility(result(board, move))
            if move_utility > optimal_utility:
                optimal_utility = move_utility
                best_move = move

    # O's logic
    else:
        optimal_utility = math.inf
        for move in actions(board):
            # Opponent will be attempting to maximize utilties
            move_utility = max_utility(result(board, move))
            if move_utility < optimal_utility:
                optimal_utility = move_utility
                best_move = move

    return best_move
