import java.util.*;
//The following part should be completed by students.
//Students can modify anything except the class name and exisiting functions and varibles.
public class StudentAI extends AI 
{
	public StudentAI(int col, int row, int k, int g) 
	{
		super(col, row, k, g);
	}

	public Move GetMove(Move move) 
	{
		Random ra =new Random();
		if (g == 0){
			return new Move(ra.nextInt(col),ra.nextInt(row));
		}
		else{
			return new Move(ra.nextInt(col),0);
		}

	}
	
}