import java.util.*;

public abstract class AI 
{
	protected int col, row, k, g, player;

	public AI(int col, int row, int k, int g) 
	{
		this.col = col;
		this.row = row;
		this.k = k;
		this.g = g;
	} 

	public abstract Move GetMove(Move board);
}

