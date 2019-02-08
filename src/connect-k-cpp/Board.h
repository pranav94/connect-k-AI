#ifndef BOARD_H
#define BOARD_H

#pragma once
#include "Move.h"
#include <vector>
#include <iomanip>
#include <iostream>
using namespace std;
class Board {
public:
	bool IsValidMove(int col,int row,bool checkSpace);
	bool IsValidMove(Move move);
	vector<vector<int> > board;

	int col, row, k, g;
	Board();
	Board(int col, int row,int k, int g);
	Board(const Board& b);
	Board MakeMove(Move move,int player);
	int IsWin();
	void ShowBoard();
};

class InvalidMoveError
{

};

#endif //BOARD_H

