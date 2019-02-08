from BoardClasses import Move

class ManualAI():
    def __init__(self,col,row,k,g):
        pass

    def get_move(self,move):
        while True:
            try:
                c,r = map(lambda x:int(x),input("{col} {row}:").split(' '))
            except KeyboardInterrupt:
                raise KeyboardInterrupt
            except:
                print('invalid move')
                continue
            else:
                break
        return Move(c,r)
