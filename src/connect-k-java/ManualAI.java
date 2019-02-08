import java.util.*;
import java.io.*;

public class ManualAI extends AI 
{
	public ManualAI(int col, int row, int k, int g) 
	{
		super(col, row, k, g);
	}

	public Move GetMove(Move move) 
	{
		Scanner reader = new Scanner(System.in);
		int c, r;
		System.out.print("col, row: ");
		c = reader.nextInt();
		r = reader.nextInt();
		Move res = new Move(c, r);
		return res;
	}

}