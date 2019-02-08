from BoardClasses import *
from ManualAI import *
from StudentAI import *

class GameLogic:

    def __init__(self,col,row,k,g,mode,debug):
        self.col = col
        self.row = row
        self.k = k
        self.g = g
        self.mode = mode
        self.debug = debug
        self.ai_list = []

    def Manual(self):
        player = 1
        winPlayer = 0
        move = Move(-1,-1)
        board = Board(self.col,self.row,self.k,self.g)
        while True:
            move = self.ai_list[player-1].get_move(move)
            try:
                board = board.make_move(move,player)
            except InvalidMoveError:
                print("Invalid Move!")
                if player == 1:
                    winPlayer = 2
                else:
                    winPlayer = 1
                break
            winPlayer = board.is_win()
            board.show_board()
            if(winPlayer != 0):
                break
            if player == 1:
                player = 2
            else:
                player = 1
        if winPlayer == -1:
            print("Tie")
        else:
            print('player',winPlayer,'wins')

    def TournamentInterface(self):
        ai = StudentAI(self.col,self.row,self.k,self.g)
        while True:
            col, row = map(lambda x: int(x), input().split(' '))
            result = ai.get_move(Move(col,row))
            print("{} {}".format(result.col,result.row))


    def Run(self):
        if self.mode == 'm':
            self.ai_list.append(ManualAI(self.col, self.row, self.k, self.g))
            self.ai_list.append(StudentAI(self.col,self.row,self.k,self.g))

            self.Manual()
        if self.mode == 't':
            self.TournamentInterface()

