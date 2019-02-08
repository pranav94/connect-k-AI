#include "GameLogic.h"
GameLogic::GameLogic(int col, int row, int k,int g, string mode,bool debug)
{
	this->col = col;
	this->row = row;
	this->k = k;
	this->g = g;
	this->mode = mode;
	this->debug = debug;
}

void GameLogic::Manual()
{
	int player = 1;
	int winPlayer = 0;
	bool init = true;
	Move move(-1, -1);
	Board board(col, row, k, g);
	while (true)
	{
		move = aiList[player - 1]->GetMove(move);
		try
		{
			board = board.MakeMove(move, player);
		}
		catch (InvalidMoveError)
		{
			cout << "Invalid Move!" << endl;
			winPlayer = player == 1 ? 2 : 1;
			break;
		}
		winPlayer = board.IsWin();
		board.ShowBoard();
		if (winPlayer != 0)
		{
			break;
		}
		player = player == 1 ? 2 : 1;

	}
	if (winPlayer == -1)
	{
	    cout<< "Tie"<<endl;
	}
	else
	{
	    cout << "Player " << winPlayer << " wins!" << endl;
	}

}

void GameLogic::TournamentInterface()
{
	StudentAI ai(col, row, k, g);
	while (true)
	{
		int col, row;
		cin >> col >> row;
		Move result = ai.GetMove(Move(col, row));
		cout << result.col <<" "<< result.row<<" "<< endl;
	}
}

void GameLogic::Run()
{
	if (mode == "m")
	{
		AI* studentai = new StudentAI(col, row, k, g);
		AI* manualai = new ManualAI(col, row, k, g);
		aiList.push_back(manualai);
		aiList.push_back(studentai);

		Manual();
	}
	else if (mode == "t")
	{
		TournamentInterface();
	}
}



GameLogic::~GameLogic()
{
	for (int i = 0; i < aiList.size(); i++)
	{
		delete aiList[i];
	}
}
