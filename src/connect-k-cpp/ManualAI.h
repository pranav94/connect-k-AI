#ifndef MANUALAI_H
#define MANUALAI_H
#include "AI.h"
#pragma once


class ManualAI : public AI
{
public:
	ManualAI(int col, int row, int k, int g);
	virtual Move GetMove(Move board);
};

#endif //MANUALAI_H