# Chess

My version of a chess game: includes en-passant, castling, 50 move rule, threefold repetition draw rule.

Can import FEN to start from a specific position.

FEN format starting position: <br>
rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1


## Prerequisites

I used pygame 1.9.6 and Python 3.7

### Instructions

Run main.py to play both sides<br>
```python run.py```<br>

Run main.py with argument of 'ai' to against ai<br>
```python run.py ai```<br>

Run main.py with FEN as command line argument to play from FEN position eg:<br>
```python run.py "r1bqkb1r/pp3ppp/2np1n2/4p1B1/3NP3/2N5/PPP2PPP/R2QKB1R w KQkq e6 1 7"```

Run main.py with both ai and FEN as command line arguments to play from FEN position against computer eg:<br>
```python run.py ai "1k1r4/pp1b1R2/3q2pp/4p3/2B5/4Q3/PPP2B2/2K5 b - -"```

