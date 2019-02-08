#include "Board.h"


Board::Board()
{
	this->col = 0;
	this->row = 0;
	this->k = 0;
	this->g = 0;
}
Board::Board(int col, int row,int k, int g)
{
	this->col = col;
	this->row = row;
	this->k = k;
	this->g = g;
	this->board.resize(row);
	for (int i = 0; i < row; ++i)
	{
		this->board[i].resize(col);
	}

	for (int i = 0; i < row; ++i)
	{
		for (int j = 0; j < col; ++j)
		{
			this->board[i][j] = 0;
		}
	}
		
}

Board::Board(const Board& b)
{
	this->col = b.col;
	this->row = b.row;
	this->k = b.k;
	this->g = b.g;
	this->board.resize(row);
	for (int i = 0; i < row; ++i)
	{
		this->board[i].resize(col);
	}

	for (int i = 0; i < row; ++i)
	{
		for (int j = 0; j < col; ++j)
		{
			this->board[i][j] = b.board[i][j];
		}
	}

}

void Board::ShowBoard()
{
	for (int i = 0; i < this->row; ++i)
	{
		cout << i << "|" ;
		for (int j = 0; j < col; ++j)
		{
			cout << setw(3) << this->board[i][j];
		}
		cout << endl;
	}
	for (int j = 0; j < col; ++j)
	{
		cout << "----";
	}
	cout <<  endl;
	cout << setw(2) << " ";
	for (int j = 0; j < col; ++j)
	{
		cout << setw(3) << j;
	}
	cout << endl;
	cout << endl;
}

bool Board::IsValidMove(int col,int row,bool checkSpace)
{
	if (col >= this->col || col < 0)
		return false;
	if (row >= this->row || row < 0)
		return false;
	if (checkSpace && board[row][col] != 0)
	{
		return false;
	}
	return true;
}

bool Board::IsValidMove(Move move)
{
	if (move.col >= this->col || move.col < 0)
		return false;
	if (move.row >= this->row || move.row < 0)
		return false;
	if (board[move.row][move.col] != 0)
	{
		return false;
	}
	return true;
}

Board Board::MakeMove(Move move, int player)
{
	Board result_board(*this);
	if (player != 1 && player != 2)
	{
		throw InvalidMoveError();
	}
	if (!IsValidMove(move))
	{
		throw InvalidMoveError();
	}
	if (this->g == 0)
	{
		result_board.board[move.row][move.col] = player;
	}
	else
	{
		for (int i = row - 1; i >= 0; --i)
		{
			if (result_board.board[i][move.col] == 0)
			{
				result_board.board[i][move.col] = player;
				break;
			}
		}
	}
	return result_board;
}

int Board::IsWin()
{
	const int stepCol[] = { 0,0, 1,-1,1,-1, 1,-1 };
	const int stepRow[] = { 1,-1,0,0, 1,-1,-1, 1 };
	const int stepSize = 8;
	bool tie = true;
	for (int i = 0; i < row; ++i)
	{
		for (int j = 0; j < col; ++j)
		{
			if (board[i][j] == 0)
			{
			    tie = false;
			    continue;
			}

			int firstPlayer = board[i][j];
			for (int stepIndex = 0; stepIndex < stepSize; ++stepIndex)
			{
				bool win = true;
				int temp_row = i;
				int temp_col = j;
				for (int step = 0; step < k - 1; ++step)
				{
					temp_row += stepRow[stepIndex];
					temp_col += stepCol[stepIndex];
					if (!IsValidMove(temp_col, temp_row, false))
					{
						win = false;
						break;
					}
					if (board[temp_row][temp_col] != firstPlayer)
					{
						win = false;
						break;
					}
				}
				if (win)
				{
					return firstPlayer;
				}
			}
		}
	}
	if (tie)
	{
	    return -1;
	}
	return 0;
}
