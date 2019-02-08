#ifndef STUDENTAI_H
#define STUDENTAI_H
#include "AI.h"
#pragma once

//The following part should be completed by students.
//Students can modify anything except the class name and exisiting functions and varibles.
class StudentAI :public AI
{
public:
	StudentAI(int col, int row, int k, int g);
	virtual Move GetMove(Move board);
};

#endif //STUDENTAI_H