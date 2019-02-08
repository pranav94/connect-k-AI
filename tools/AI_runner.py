from sys import argv
from tournament import game_main_loop

def get_prefix(ai):
    if ai.endswith('.exe'):
        ai = './'+ai
    elif ai.endswith('.py') or ai.endswith('.pyc') :
        ai = 'python3 '+ai
    elif ai.endswith('.jar'):
        ai = 'java -jar ' + ai
    return ai
if __name__ == '__main__':
    #col/row/k/g/ai 1 path/ai 2 path
    col,row,k,g,ai_1,ai_2 = argv[1:]
    ai_1 = get_prefix(ai_1)
    ai_2 = get_prefix(ai_2)

    ai_1 = ai_1 + " " + str(col)+ " " + str(row) + " " + str(k) + " " + str(g) + " t"
    ai_2 = ai_2 + " " + str(col) + " " + str(row) + " " + str(k) + " " + str(g) + " t"
    col = int(col);row=int(row);k=int(k);g=int(g)
    win_player = game_main_loop(col,row,k,g,ai_1,ai_2,True)
    if win_player == -1:
        print("Tie")
    else:
        print("player",win_player,"wins")