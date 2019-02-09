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
        self.next_moves = {}

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
            for j in range(self.col):
                current_count = 0
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

    def diagonal_score(self, player):
        # TODO: Write this
        return 0

    def anti_diagonal_score(self, player):
        # TODO: Write this
        return 0

    def heuristic_score(self, player):
        """Generates a score for the current state."""
        return (
            self.vertical_score(player) +
            self.horizontal_score(player) +
            self.diagonal_score(player) +
            self.anti_diagonal_score(player)
        )

    def minimax(self):
        best_move = 0
        best_score = float('-inf')
        for c in range(self.col):
            if self.check_space(c, 0) and not self.is_win():
                next_board_state = self.make_move(Move(c, 0), SELF)
                score = self.min_play(next_board_state, 0)
                if score > best_score:
                    best_move = c
                    best_score = score

        return Move(best_move, 0)

    def min_play(self, state, depth):
        if depth >= 4:
            return state.heuristic_score(SELF) - state.heuristic_score(OPPONENT)

        best_score = float('inf')
        for c in range(state.col):
            if state.check_space(c, 0) and not state.is_win():
                next_board_state = state.make_move(Move(c, 0), OPPONENT)
                score = state.max_play(next_board_state, depth+1)
                best_score = min(best_score, score)

        return best_score

    def max_play(self, state, depth):
        if depth >= 4:
            return state.heuristic_score(SELF) - state.heuristic_score(OPPONENT)

        best_score = float('-inf')
        for c in range(state.col):
            if state.check_space(c, 0) and not state.is_win():
                next_board_state = state.make_move(Move(c, 0), SELF)
                score = state.min_play(next_board_state, depth+1)
                best_score = max(score, best_score)

        return best_score

    def check_space(self, c, r):
        return True if self.board[r][c] == 0 else False


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
            best_move = self.myboard.minimax()()
            self.myboard = self.myboard.make_move(best_move, SELF)
            return best_move
