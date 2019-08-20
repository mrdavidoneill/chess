import sys, os
thisdir = os.path.dirname(__file__)
srcdir = 'chess'
sys.path.insert(0, os.path.abspath(os.path.join(thisdir, srcdir)))

from chess.controller import GameLoop

if __name__ == "__main__":
    ai = None
    fen = None
    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            if arg.lower() == "ai":
                ai = True
            else:
                fen = arg

    GameLoop(ai=ai, fen=fen)
