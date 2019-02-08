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

    def __init__(self, col, row, k, g, player, board=None, depth=0):
        """Copy an existing state of the board to generate a new Board object or create a new board.

        Args:
            player (int): The player whose turn it is to play. Either SELF or opponent.
            board (MyBoard): The state of the board to copy.
            depth (int): The depth of this board state from the actual board state. 
                            i.e Number of moves required on the current board state to arrived at this state

        """
        Board.__init__(self, col, row, k, g)

        # If a state has been passed, use this board state to initialize
        if board:
            self.board = deepcopy(board.board)

        self.depth = depth
        self.player = player
        self.next_moves = {}

        # If already won by SELF, then assign a score for this state. Else assign 0.
        self.score = heuristic(k) if self.is_win() == SELF else 0

        # If this state isn't a winning state, calculate scores of all possible next states.
        if self.is_win() == 0:
            self.score = self.calculate_scores()

    def check_empty_vertical_spots(self, i, j, k):
        """Check if the spot above the consecutive tokens is empty."""
        return (
            j > 0 and self.board[i-k][j-1] == 0
        )

    def check_empty_horizontal_spots(self, i, j, k):
        """Checks if the spot before and after consecutive tokens is empty and has ground below for next token."""
        left_empty_and_has_ground = (j-k >= 0 and self.board[i][j-k] == 0) and (i == self.row-1 or self.board[i+1][j-k] != 0)
        right_empty_and_has_ground = (j+1 < self.col and self.board[i][j+1] == 0) and (i == self.row-1 or self.board[i+1][j+1] != 0)

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

    def get_next_state(self, move, player):
        """Make a move and recursively calculate the next moves until depth 4."""
        next_move = self.make_move(move, player)
        return MyBoard(self.col, self.row, self.k, self.g, player, next_move, self.depth+1)

    def calculate_scores(self):
        if self.depth == 4:
            return self.heuristic_score(SELF) - self.heuristic_score(OPPONENT)
        next_player = SELF if self.player == OPPONENT else OPPONENT
        score = 0
        for c in range(self.col):
            if self.check_space(c, 0) and not self.is_win():
                next_board_state = self.get_next_state(Move(c, 0), next_player)
                self.next_moves[c] = next_board_state
                score += next_board_state.score

        return score

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
        self.myboard = MyBoard(col, row, k, g, SELF)

    def get_best_move(self):
        max_score = -float('inf')
        best_move = Move(0, 0)
        for c in self.myboard.next_moves:
            if self.myboard.next_moves[c].score > max_score:
                max_score = self.myboard.next_moves[c].score
                best_move = Move(c, 0)

        return best_move

    def get_move(self, move):
        self.myboard = self.myboard.make_move(move, OPPONENT)
        self.myboard.calculate_scores()

        if self.g == 0:
            return Move(randint(0, self.col-1), randint(0, self.row-1))
        else:
            next_move = self.get_best_move()
            self.myboard = self.myboard.make_move(next_move, SELF)
            return next_move
