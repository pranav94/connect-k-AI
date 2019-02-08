from sys import argv
from BoardClasses import *
from Communicator import Communicator
import time


'''
I know the logic below is kind of messy. It should be improved.
The basic logic is, if an AI causes a raised exception, the other AI will win, so the winning player is:
player = 1 if player == 2 else 2
(player_switch)

If board.is_win() returns a non-zero flag, the main loop will be broken immediately, and the current player will win.
Therefore, in general, if the while loop is broken by raised exception, "player_switch" will be called.
'''

def player_switch(player):
    return 1 if player == 2 else 2

def game_main_loop(col,row,k,g,ai_1,ai_2,debug=False):
    board = Board(col,row,k,g)
    AI_com_list = [Communicator(ai_1,1000),Communicator(ai_2,1000)]
    player = 1
    win_flag = 0
    try:
        AI_com_list[player-1].send("-1 -1".encode())
    except BrokenPipeError:
        print("Player 2 wins!")
        return

    while True:
        try:
            ai_move,std_error = AI_com_list[player-1].recv()
        except TimeoutError:
            player = player_switch(player)
            if (debug):
                print("Time Out!")
            break
        ai_move = ai_move.decode().split("\n")[-1].rstrip()
        if (debug):
            print("Player",player,"says:",ai_move)

        try:
            board = board.make_move(Move(0,0,ai_move),player)
        except InvalidMoveError:
            if (debug):
                print("Invalid Move!")
            player = player_switch(player)
            break
        except Exception as msg:
            if (debug):
                print("Unknown Error with the stderr:")
                print(std_error.decode())
                print("Shell raised the following exception:")
                print(msg)
            player = player_switch(player)
            break
        if (debug):
            board.show_board()
        win_flag = board.is_win()
        if (win_flag != 0):
            break

        player = player_switch(player)
        try:
            AI_com_list[player-1].send(ai_move.encode())
        except BrokenPipeError:
            if (debug):
                print("Player", player, "crashed!")
            player = player_switch(player)
            break

    if win_flag != 0:
        return win_flag
    else:
        return player