#include "ManualAI.h"
#include <iostream>

ManualAI::ManualAI(int col, int row, int k, int g)
	:AI(col, row, k, g)
{

}

Move ManualAI::GetMove(Move move)
{
	int r, c;
	cout << "{col} {row}:";
	cin >> c >> r;
	Move res(c, r);
	return res;
}

