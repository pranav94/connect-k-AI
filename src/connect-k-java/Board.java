import java.util.*;
import java.io.*;

public class Board 
{
	public ArrayList<ArrayList<Integer>> board;
	public int col, row, k, g;

	public Board() 
	{
		this.col = 0;
		this.row = 0;
		this.k = 0;
		this.g = 0;
		board = new ArrayList<ArrayList<Integer>>();
	}

	public Board(int col, int row, int k, int g) 
	{
		this.col = col;
		this.row = row;
		this.k = k;
		this.g = g;
		board = new ArrayList<ArrayList<Integer>>();

		for (int i = 0; i < row; i++) 
		{
			ArrayList<Integer> temp = new ArrayList<Integer>();
			for(int j = 0; j < col; j++)
			{
				temp.add(0);
			}
			board.add(temp);
		}
	}

	public Board(final Board b)
	{
		this.col = b.col;
		this.row = b.row;
		this.k = b.k;
		this.g = b.g;
		board = new ArrayList<ArrayList<Integer>>();


		for (int i = 0; i < row; i++) 
		{
			ArrayList<Integer> temp = new ArrayList<Integer>();;
			for(int j = 0; j < col; j++)
			{
				temp.add(b.board.get(i).get(j));
			}

			board.add(temp);
		}
	}

	public boolean IsValidMove(int col, int row, boolean checkSpace)
	{
		if (col >= this.col || col < 0)
		{
			return false;
		}
		if (row >= this.row || row < 0)
		{
			return false;
		}
		if (checkSpace && board.get(row).get(col) != 0)
		{
			return false;
		}
		return true;
	}

	public boolean IsValidMove(Move move)
	{
		if (move.col >= this.col || move.col < 0)
		{
			return false;
		}
		if (move.row >= this.row || move.row < 0)
		{
			return false;
		}
		if (board.get(move.row).get(move.col) != 0)
		{
			return false;
		}
		return true;
	}

	public Board MakeMove(Move move, int player) throws InvalidMoveError
	{
		Board result_board = new Board(this);
		if (player != 1 && player != 2)
		{
			throw new InvalidMoveError();
		}
		if (!IsValidMove(move))
		{
			throw new InvalidMoveError();
		}
		if (this.g == 0)
		{
			result_board.board.get(move.row).set(move.col,player);
		}
		else
		{
			for (int i = row - 1; i >= 0; --i)
			{
				if (result_board.board.get(i).get(move.col) == 0)
				{
					result_board.board.get(i).set(move.col, player);
					break;
				}
			}
		}
		return result_board;
	}

	public int IsWin() 
	{
		final int[] stepCol = { 0, 0, 1, -1, 1, -1, 1, -1};
		final int[] stepRow = { 1, -1, 0, 0, 1, -1, -1, 1};
		final int stepSize = 8;
        boolean tie = true;
		for(int i = 0; i < this.row; ++i )
		{
			for(int j = 0; j < this.col; j++)
			{
				if(this.board.get(i).get(j) == 0)
				{
				    tie = false;
					continue;
				}
				int firstPlayer = board.get(i).get(j);
				for (int stepIndex = 0; stepIndex < stepSize; ++stepIndex)
				{
					boolean win = true;
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
						if (board.get(temp_row).get(temp_col) != firstPlayer)
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

	public void ShowBoard()
	{
		for (int i = 0; i < this.row; ++i)
		{
			System.out.print(i + "|");
			for (int j = 0; j < this.col; ++j)
			{
				System.out.print(String.format("%3d",this.board.get(i).get(j)));
			}
			System.out.print("\n");
		}
		for (int j = 0; j < this.col; ++j)
		{
			System.out.print("----");
		}
		System.out.print("\n");
		System.out.print(String.format("%2s"," "));

		for (int j = 0; j < this.col; ++j)
		{
			System.out.print(String.format("%3d",j));
		}
		System.out.print("\n");
		System.out.print("\n");
	}
}



