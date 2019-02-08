from GameLogic import GameLogic
import sys

if __name__ == "__main__":
    if len(sys.argv) < 6:
        print("Invalid Parameters")
        sys.exit(-1)

    col = int(sys.argv[1])
    row = int(sys.argv[2])
    k = int(sys.argv[3])
    g = int(sys.argv[4])
    mode = sys.argv[5]
    debug = False
    if len(sys.argv) == 7 and sys.argv[6] == "-d":
        debug = True

    main = GameLogic(col,row,k,g,mode,debug)
    main.Run()
