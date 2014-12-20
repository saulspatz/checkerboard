'''
checkerboard.py

This program will create the data and call the solver

The board is represented as a square with cells (0,0) to (7, 7). 
The coordinates are as in computer graphics, so x increases
from left to right, and y increases from top to bottom.  The top
left-hand corner of the board is (0,0).  WLOG cell (0,0) is
white.

Each piece is described by an id and a list of cell coordiantes.
The cells are those the piece would occupy if placed as far up 
and to the left as possible, in one of its orientations.  To translate
the piece, we must add (deltax, deltay) to each cell, but to preserve
cell color, we must have deltax + deltay = 0 (mod ).  
(The problem is small enough that I have no qualms about generate and test. )  
A small complication is that it may be possible to have the  piece rest against
the y-axis or against the x-axis, but not both, because of the colors.  We
will follow the rule that it always rests against the x-axis, and if possible, it
also rests against the y-axis.  Then we can can just take the smallest possible
value of deltax as -1 instead of 0.  Now we can just check whether all resulting 
coords c have 0 <= c < 8 to see  if this is a legal move.

The next thing we have to do for each piece is rotate it.
(x, y) --> (7-y, x)
gives a 90 degree clockwise rotation, and we can do it 3 times.

We need to put the piece in standard position after rotating it, so that it is
as far to the left, and as far up as possible.  That is, we want to subtract the
minimum x value from all coordinates, and we want to subtract the minimum
y value also, but the total subtraction must be even to preserve color.  We just 
follow the same rule as above: subtract the minimum y value, and either the
minimum x value, or one less, depending on parity.
'''
from dancingLinks import solve
from functools import reduce
from collections import defaultdict
from drawBoard import drawSolutions
import os

class Positions(dict):
    rowId =1                                  # static class variable
    def __init__(self, id, base):
        '''
        Given the base position of a piece, construct a dict of rows 
        representing all possible positions of the piece.  The keys
        are the row ids and the values are lists of cell coordinates,
        which also serve as the column ids.  The pieceId is a column
        that will have a 1 for every row in the dict.  (This is how we
        ensure that each piece is used exactly once.)
        '''  
        super().__init__()
        base.sort()                                
        self.translate(base, id)
        
        # now rotate three times
        # Note that the rotation reverses the colors, so when we 
        # translate back to standard position, we must reverse them again.
        for rotate in range(3):
            pos = base
            pos = [(7-y, x) for (x, y) in pos]
            minx = min(pos, key = lambda c: c[0])[0]
            miny = min(pos, key = lambda c: c[1])[1]
            if (miny + minx) % 2 == 0:
                minx -= 1
            base = [(x-minx, y-miny) for (x, y) in pos]
            base.sort()
            if base + [id] in self.values():       # skip symmetric positions
                continue
            self.translate(base, id)
    
    def translate(self, base, id):
        for deltay in range(0, 8):
            start = -1 if deltay % 2 else 0
            for deltax in range(start, 8, 2):
                pos = [(x+deltax, y+deltay) for (x, y) in base]
                
                # get all the individual coordinates
                c = reduce(tuple.__add__, pos)
                
                if 0 <= min(c) <= max(c) < 8:
                    self[Positions.rowId] = pos + [id]
                    Positions.rowId += 1 
                    
def expand(soln):
    '''
    soln is a list of row ids.  Expand it to a checkerboard by replacing
    each cell by the symbol representing the piece that covers it
    '''
    answer = [list(8*'a') for j in range(8)]
    for id in soln:
        row = Y[id]
        cells = row[:-1]
        symbol = row[-1]
        for x, y in cells:
            answer[x][y] = symbol
    return answer

def equiv(s, t):
    '''
    s and t are boards, as returned by expand.  Are they equivalent ?  The only possible
    symmetry is a 180 degree roation, followd by an interchange of A and L
    '''
    for x in range(8):
        for y in range(8):
            a = s[x][y]
            b = t[7-x][7-y]
            if a != b != set((a,b)) != set(('A', 'L')) :
                return False
    return True

def aBeforel(board):
    '''
    Since pieces A and L are identical, we report whether A is encountered
    before L when the board is scanned.
    '''
    for row in board:
        for a in row:
            if a == 'A':
                return True
            if a == 'L':
                return False
            
def transform(board):
    '''
    Because of the equivalence of the A and L pieces, a possible symmetry is
    to rotate the board 180 degrees, then interchange A and L; A will still
    come before L.  Compute the effect of this transformation.
    '''
    answer = [list(8*'a') for j in range(8)]
    for x in range(8):
        for y in range(8):
            answer[x][y] = board[7-x][7-y]
    for x in range(8):
        for y in range(8):
            if answer[x][y] == 'A':
                answer[x][y] = 'L'
            elif answer[x][y] == 'L':
                answer[x][y] == 'A'
                
# Define the pieces.  The ids are arbitary.        

# Piece 1
#  WBWB
#  B
#  W

p = ('A', [(0,0), (1, 0), (2, 0), (3,0), (0,1), (0,2)])
Y = Positions(*p)

# Piece 2
# WB
# BW
#  _B
#  _W
#  _B

p = ('B', [(0,0), (1, 0), (0,1), (1,1), (1,2), (1,3), (1,4)])
Y.update(Positions(*p))

# Piece 3
# __WB
# _WBW

p = ('C', [(2,0), (3,0), (1, 1), (2,1), (3,1)])
Y.update(Positions(*p))

# Piece 4
# WB
# BWBW

p = ('D', [(0,0),(1,0), (0,1),(1,1),(2,1),(3,1)])
Y.update(Positions(*p))

# Piece 5
# WBW

p = ['E',[(0,0), (1,0), (2,0)]]
Y.update(Positions(*p))

# Piece 6
# _BWB
# ___W
# ___B

p = ['F', [(1,0),(2,0),(3,0), (3,1), (3, 2)]]
Y.update(Positions(*p))

# Piece 7
# _BW
# __B
# __W
# __B
# __W

p = ['G', [(1,0),(2,0),(2,1),(2,2),(2,3),(2,4)]]
Y.update(Positions(*p))

# Piece 8
# _BW
# _W
# _B
# _W
# _B

p = ['H', [(1,0), (2,0), (1,1),(1,2),(1,3),(1,4)]]
Y.update(Positions(*p))

# Piece 9
# _BW
# _W

p = ['I', [(1,0), (2,0), (1,1)]]
Y.update(Positions(*p))

# Piece 10
# ___B
# __BW
# _BW

p = ['J', [(3,0), (2,1), (3,1), (1,2), (2,2)]]
Y.update(Positions(*p))

# Piece 11
# _B
# BW
# W
# B
# W

p = ['K', [(1,0),(0,1),(1,1),(0,2),(0,3),(0,4)]]
Y.update(Positions(*p))

# Piece 12
# ____W
# ____B
#_BWBW

p = ['L', [(4,0), (4,1), (1,2), (2,2), (3,2), (4,2)]]
Y.update(Positions(*p))

X = defaultdict(set)
for row in Y:
    for col in Y[row]:
        X[col].add(row)


for f in [f for f in os.listdir('.') if f.startswith('board')]:
    os.remove('./'+f)
    
solutions = []
seq = 1
for soln in solve(X, Y):
    board = expand(soln)
    if not aBeforel(board):
        continue
    for brd in solutions:
        if equiv(board, brd) : break
    else:                           # loop else                      
        solutions.append(board)
        seq += 1
drawSolutions(solutions)
    