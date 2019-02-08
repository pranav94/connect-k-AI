#include "StudentAI.h"
#include <stdlib.h>

//The following part should be completed by students.
//The students can modify anything except the class name and exisiting functions and varibles.
StudentAI::StudentAI(int col,int row,int k,int g)
	:AI(col, row, k, g)
{
	
}

Move StudentAI::GetMove(Move move)
{
	if (this->g == 0)
		return Move(rand() % (col - 1), rand() % (row - 1));
	else
		return Move(rand() % (col - 1), 0);
}

