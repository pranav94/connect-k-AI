from copy import deepcopy
from random import randint
from BoardClasses import Board, Move

OPPONENT = 2
SELF = 1


def heuristic(k):
    """
    Assigns a heuristic score for a given number of sequential tokens.
    More number of consecutive tokens => Much larger score. Grows quadratively.
    """
    return k * k


class MyBoard(Board):
    """Custom board class to maintain the moves."""

    def __init__(self, col, row, k, g):
        """Board class used to track the moves."""
        Board.__init__(self, col, row, k, g)

    def check_empty_vertical_spots(self, i, j, k):
        """Check if the spot above the consecutive tokens is empty."""
        return (
            j > 0 and i-k > 0 and self.board[i-k][j-1] == 0
        )

    def check_empty_horizontal_spots(self, i, j, k):
        """Checks if the spot before and after consecutive tokens is empty and has ground below for next token."""
        left_empty_and_has_ground = (
            j-k >= 0 and self.board[i][j-k] == 0) and (i == self.row-1 or self.board[i+1][j-k] != 0)
        right_empty_and_has_ground = (
            j+1 < self.col and self.board[i][j+1] == 0) and (i == self.row-1 or self.board[i+1][j+1] != 0)

        return left_empty_and_has_ground or right_empty_and_has_ground

    def horizontal_score(self, player):
        """
        Checks if the player has occupied consecutive horizontal positions with a leading or trailing empty spot.
        More number of positions the user has acquired, more score.
        Example: 10000 => 10 points, 11000 => 100 points, 11100 => 1000 points
        """
        score = 0
        for i in range(self.row):
            current_count = 0
            for j in range(self.col):
                if self.board[i][j] == player:
                    current_count += 1
                else:
                    current_count = 0
                current_count = max(current_count, self.k-1)
                # Check if there is an empty spot before or after this series of counts
                if current_count > 0 and self.check_empty_horizontal_spots(i, j, current_count):
                    score += heuristic(current_count)

        return score

    def vertical_score(self, player):
        """
        Checks if the player has occupied consecutive vertical positions with a leading or trailing empty spot.
        More number of positions the user has acquired, more score.
        Example: 10000 => 10 points, 11000 => 100 points, 11100 => 1000 points
        """
        score = 0
        for i in range(self.col):
            current_count = 0
            for j in range(self.row):
                if self.board[j][i] == player:
                    current_count += 1
                else:
                    current_count = 0
                current_count = max(current_count, self.k)

                # Check if there is an empty spot before or after this series of counts
                if current_count > 0 and self.check_empty_vertical_spots(i, j, current_count):
                    score += heuristic(current_count)

        return score

    def get_diag_len(self, i, j, player):
        count = 0
        while (i < self.row and j < self.col):
            if self.board[i][j] == player:
                count += 1
            else:
                break
            i += 1
            j += 1

        return count

    def diagonal_score(self, player):
        score = 0
        for i in range(self.row):
            for j in range(self.col):
                if j-1 >= 0 and self.board[i][j-1] == 0:
                    continue
                if j-1 >= 0 and i-1 >= 0 and self.board[i-1][j-1] != 0 and i == 0:
                    continue
                count = self.get_diag_len(i, j, player)

                score += heuristic(count)

        return count

    def get_anti_diag_len(self, i, j, player):
        count = 0
        while (i < self.row and j >= 0):
            if self.board[i][j] == player:
                count += 1
            else:
                break
            i += 1
            j -= 1

        return count

    def anti_diagonal_score(self, player):
        score = 0
        for i in range(self.row):
            for j in range(self.col):
                if j+1 < self.col and self.board[i][j+1] == 0 and j == self.col-1:
                    continue
                if j+1 < self.col and i-1 >= 0 and self.board[i-1][j+1] != 0 and i == 0:
                    continue
                count = self.get_diag_len(i, j, player)
                score += heuristic(count)

        return count

    def heuristic_score(self, player):
        """Generates a score for the given player in the current state."""
        return (
            self.vertical_score(player) +
            self.horizontal_score(player) +
            self.diagonal_score(player) +
            self.anti_diagonal_score(player)
        )

    def check_space(self, c, r):
        return True if self.board[r][c] == 0 else False

    def minimax(self, state, depth=0, player=SELF, alpha=float('-inf'), beta=float('inf')):
        """
        Calculates the next possible states and calculates the optimal value
        using minimax with alpha beta pruning. If the state is a win state or
        at depth = number of rows, returns a heuristic score instead.
        """
        if state.is_win():
            if player == OPPONENT:
                return (float('inf'), Move(0, 0))
            return (float('-inf'), Move(0, 0))
        if depth == self.col:
            if player == OPPONENT:
                return (state.heuristic_score(OPPONENT) - state.heuristic_score(SELF), Move(0, 0))
            return (state.heuristic_score(SELF) - state.heuristic_score(OPPONENT), Move(0, 0))

        best_move = 0
        next_player = SELF if player == OPPONENT else OPPONENT
        best_val = float('-inf') if player == SELF else float('inf')
        for c in range(state.col):
            if not state.check_space(c, 0):
                continue
            value, _move = self.minimax(
                state.make_move(Move(c, 0), next_player),
                depth + 1, next_player, alpha, beta
            )
            if player == SELF:
                if value > best_val:
                    best_val = value
                    best_move = c
                alpha = max(alpha, best_move)
            else:
                if value < best_val:
                    best_val = value
                    best_move = c
                beta = min(beta, best_val)
            if beta <= alpha:
                break
        return best_val, Move(best_move, 0)


class StudentAI():
    col = 0
    row = 0
    k = 0
    g = 0

    def __init__(self, col, row, k, g):
        self.g = g
        self.col = col
        self.row = row
        self.k = k
        self.myboard = MyBoard(col, row, k, g)

    def get_move(self, move):
        self.myboard = self.myboard.make_move(move, OPPONENT)

        if self.g == 0:
            return Move(randint(0, self.col-1), randint(0, self.row-1))
        else:
            (_best_val, best_move) = self.myboard.minimax(self.myboard)
            self.myboard = self.myboard.make_move(best_move, SELF)
            return best_move
