#include "GameLogic.h"
#include <stdlib.h> 

int main(int argc, char *argv[])
{
	if (argc < 6)
	{
		cout << "Invalid Parameters" << endl;
		return 0;
	}
	//mode="m"->manual/"t"->tournament
	int col = atoi(argv[1]);
	int row = atoi(argv[2]);
	int k = atoi(argv[3]);
	int g = atoi(argv[4]);
	string mode = argv[5];
	bool debug = false;
	if (argc == 7 && argv[6] == "-d")
	{
		debug = true;
	}
	
	GameLogic main(col,row,k,g, mode, debug);//col,row,k,g,mode,debug
	main.Run();
	return 0;
}
