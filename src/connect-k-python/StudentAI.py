from time import time
from multiprocessing import Process, Manager

from BoardClasses import Board, Move

OPPONENT = 2
SELF = 1
INF = 2**32


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
        self.available = set()
        if not g:
            for i in range(row):
                for j in range(col):
                    self.available.add((i, j))

    def check_empty_vertical_spots(self, i, j, k):
        """Check if the spot above the consecutive tokens is empty."""
        top = (
            i-k > 0 and self.board[i-k][j] == 0
        )
        bottom = (
            i+1 < self.row and self.board[i+1][j] == 0
        )
        return top or bottom

    def check_empty_horizontal_spots(self, i, j, k):
        """Checks if the spot before and after consecutive tokens is empty and has ground below for next token."""
        if self.g:
            left_empty_and_has_ground = (
                j-k >= 0 and self.board[i][j-k] == 0) and (i == self.row-1 or self.board[i+1][j-k] != 0)
            right_empty_and_has_ground = (
                j+1 < self.col and self.board[i][j+1] == 0) and (i == self.row-1 or self.board[i+1][j+1] != 0)

            return left_empty_and_has_ground or right_empty_and_has_ground

        else:
            return (j-k >= 0 and self.board[i][j-k] == 0) or (j+1 < self.col and self.board[i][j+1] == 0)

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
                if current_count > 0 and self.check_empty_vertical_spots(j, i, current_count):
                    score += heuristic(current_count)

        return score

    def get_diag_len(self, i, j, player):
        """Returns the length of the diagonal at i,j."""
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
                if not self.g and j-1 >= 0 and self.board[i][j-1] == 0:
                    continue
                if j-1 >= 0 and i-1 >= 0 and self.board[i-1][j-1] != 0 and i == 0:
                    continue
                count = self.get_diag_len(i, j, player)

                score += heuristic(count)

        return count

    def get_anti_diag_len(self, i, j, player, g=True):
        """Returns the length of the anti-diagonal at i,j."""
        count = 0
        while (i < self.row and j >= 0):
            if self.board[i][j] == player:
                count += 1
            else:
                break
            i += 1
            j -= 1

        return count

    def anti_diagonal_score(self, player, g=True):
        score = 0
        for i in range(self.row):
            for j in range(self.col):
                if not self.g and j+1 < self.col and self.board[i][j+1] == 0 and j == self.col-1:
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

    def get_moves(self):
        """Returns an list of tuples as all possible moves."""
        moves = []
        if not self.g:
            return self.available
        else:
            for i in range(self.col):
                if (self.check_space(i, 0)):
                    moves.append((0, i))

        return moves

    def minimax(self, state, maxdepth, best_move_dict={}, depth=0, player=SELF, alpha=-INF, beta=INF):
        """
        Calculates the next possible states and calculates the optimal value
        using minimax with alpha beta pruning. If the state is a win state or
        at depth = number of rows, returns a heuristic score instead.
        """
        is_win = state.is_win()
        if is_win == SELF or is_win == -1:
            return INF
        if is_win == OPPONENT:
            return -INF

        if depth == maxdepth:
            return state.heuristic_score(SELF) - state.heuristic_score(OPPONENT)

        best_move = None
        next_player = SELF if player == OPPONENT else OPPONENT
        best_val = -INF if player == SELF else INF

        for r, c in state.get_moves():
            move = Move(c, r)
            if not self.g:
                state.available.remove((r, c))
            if best_move is None:
                best_move = move
            value = self.minimax(
                state=state.make_move(move, player),
                maxdepth=maxdepth,
                best_move_dict=best_move_dict,
                depth=depth + 1, player=next_player, alpha=alpha, beta=beta
            )
            if not self.g:
                state.available.add((r, c))

            if player == SELF:
                if value > best_val:
                    best_val = value
                    best_move = Move(c, r)
                alpha = max(alpha, best_val)
            else:
                if value < best_val:
                    best_val = value
                    best_move = Move(c, r)
                beta = min(beta, best_val)
            if beta <= alpha:
                break

        if depth == 0:
            best_move_dict['result'] = best_move
        return best_val


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

    def iterative_deepening_search(self):
        time_limit = self.row * 4
        started = time_limit + time()
        manager = Manager()
        best_move_dict = manager.dict()

        min_depth = 6
        max_depth = 8
        if not self.g:
            min_depth = 4 if self.col >= 7 else 5
            max_depth = 6 if self.col >= 7 else 7

        # Search at minimum depth first
        self.myboard.minimax(self.myboard, min_depth, best_move_dict)

        # # Deepen search if time is available.
        # # Use processes to return immedeiately after timeout.
        for i in range(min_depth+1, max_depth):
            time_remaining = started - time()
            if time_remaining:
                minimax = Process(
                    target=self.myboard.minimax,
                    args=(self.myboard, i, best_move_dict)
                )
                minimax.start()
                minimax.join(time_remaining)
        return best_move_dict['result']

    def get_move(self, move):
        if move.col != -1:
            if not self.g:
                self.myboard.available.remove((move.row, move.col))
            self.myboard = self.myboard.make_move(move, OPPONENT)

        best_move = self.iterative_deepening_search()
        if not self.g:
            self.myboard.available.remove((best_move.row, best_move.col))
        self.myboard = self.myboard.make_move(best_move, SELF)
        return best_move
