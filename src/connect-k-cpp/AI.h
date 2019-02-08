#ifndef AI_H
#define AI_H
#include "Move.h"
#include "Board.h"
#pragma once

class AI
{
protected:
	int col, row, k, g, player;
public:

	AI(int col, int row, int k, int g)
	{
		this->col = col;
		this->row = row;
		this->k = k;
		this->g = g;
	}
	virtual Move GetMove(Move board) = 0;
	virtual ~AI(){}
};

#endif //AI_H