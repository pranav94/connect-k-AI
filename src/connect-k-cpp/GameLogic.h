#ifndef GAMELOGIC_H
#define GAMELOGIC_H
#include "AI.h"
#include "Board.h"
#include "StudentAI.h"
#include "ManualAI.h"
#pragma once


class GameLogic
{
private:
	int col, row, k,g; 
	string mode;
	bool debug;
	vector<AI*> aiList;
public:
	GameLogic(int col,int row,int k,int g,string mode,bool debug);
	void Manual();
	void TournamentInterface();
	void Run();
	~GameLogic();
};

#endif //GAMELOGIC_H