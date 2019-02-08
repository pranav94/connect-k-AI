import java.util.*;
import java.lang.*;
import java.io.*;

public class Main {
    public static void main(String[] args) 
    {
    	if(args.length < 5)
    	{
    		System.out.println("Invalid Parameters");
    		System.exit(0);
    	}

    	int col = Integer.parseInt(args[0]);
		int row = Integer.parseInt(args[1]);
		int k = Integer.parseInt(args[2]);
		int g = Integer.parseInt(args[3]);
		String mode = args[4];
		boolean debug = false;

		if (args.length == 6 && args[5].equals("-d") )
		{
			debug = true;
		}

		GameLogic main = new GameLogic(col, row, k,g, mode, debug);
		main.Run();
    }
}