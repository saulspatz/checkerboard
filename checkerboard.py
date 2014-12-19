'''
checkerboard.py

This program will create the data and call the solver

The board is represented as a square with cells (0,0) to (7, 7), 
(0,) being visualized as the lower left-hand corner so the 
board lies in the first quadrant.  WLOG, cell (0, 0) is white.   

Each piece is described by an id and a list of cell coordiantes.
The cells are those the piece would occupy if placed as far down 
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
gives a 90 degree counter clockwise rotation, and we can do it 3 times.

We need to put the piece in standard position after rotating it, so that it is
as far to the left, an as low down as possible.  That is, we want to subtract the
minimum x value from all coordinates, and we want to subtract the minimum
y value also, but the total subtraction must be even to preserve color.  We just 
follow the same rule as above: subtract the minimum y value, and either the
minimum x value, or one less, depending on parity.
'''
from dancingLinks import solve
from functools import reduce
from collections import defaultdict

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
        #global rowId
        base.sort()                                 # just to be sure
        self.translate(base, id)
        
        # now rotate three times
        for rotate in range(3):
            pos = base
            pos = [(7-y, x) for (x, y) in pos]
            minx = min(pos, key = lambda c: c[0])[0]
            miny = min(pos, key = lambda c: c[1])[1]
            if (miny -minx) % 2 != 0:
                minx -= 1
            base = [(x-minx, y-miny) for (x, y) in pos]
            base.sort()
            if base in self.values():       # skip symmetric positions
                continue
            self.translate(base, id)
    
    def translate(self, base, id):
        #global rowId
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
        for r, c in cells:
            answer[r][c] = symbol
    return answer

def equiv(s, t):
    '''
    s and t are boards, as returned by expand.  Are they equivalent under rotation?
    '''
    # Test 90 degree, 180 degree, 270 degree counterclockwise rotations
    return ( testRotation(s, t, lambda x, y: (7-y, x)) or     
                 testRotation(s, t, lambda x, y: (7-x, 7-y)) or 
                testRotation(s, t, lambda x, y: (y, 7-x)) ) 

def testRotation(s, t, rot):
    '''
    Does the given rotation carry s to t?
    '''
    for x in range(8):
        for y in range(8):
            u, v = rot(x, y)
            if s[x][y] != t[u][v]:
                return False
    return True

# Define the pieces.  The ids are arbitary.        

# Piece 1
#  WBWB
#  B
#  W

p = ('A', [(0,0), (0, 1), (0,2), (1,2), (2, 2), (2,3)])
Y = Positions(*p)

# Piece 2
# WB
# BW
#  _B
#  _W
#  _B

p = ('B', [(0,3), (0,4), (1,0), (1,1), (1,2), (1,3), (1,4)])
Y.update(Positions(*p))

# Piece 3
# _WB
# WBW

p = ('C', [(0,0), (1,0), (2, 0), (1,1), (2,1)])
Y.update(Positions(*p))

# Piece 4
# _WB
# _BWBW

p = ('D', [(1,0),(2,0),(3,0), (4,0), (1,1), (2,1)])
Y.update(Positions(*p))

# Piece 5
# WBW

p = ['E',[(0,0), (1,0), (2,0)]]
Y.update(Positions(*p))

# Piece 6
# _BWB
# ___W
# ___B

p = ['F', [(3,0), (3,1), (1,2), (2,2), (3,2)]]
Y.update(Positions(*p))

# Piece 7
# _BW
# __B
# __W
# __B
# __W

p = ['G', [(2,0), (2,1), (2,2), (2,3), (1,4), (2,4)]]
Y.update(Positions(*p))

# Piece 8
# _BW
# _W
# _B
# _W
# _B

p = ['H', [(1,0), (1,1), (1,2), (1,3), (1,4), (2,4)]]
Y.update(Positions(*p))

# Piece 9
# BW
# W

p = ['I', [(0,0), (0,1), (1,1)]]
Y.update(Positions(*p))

# Piece 10
# ___B
# __BW
# _BW

p = ['J', [(1,0), (2,0), (2,1), (3,1), (3,2)]]
Y.update(Positions(*p))

# Piece 11
# _B
# BW
# W
# B
# W

p = ['K', [(0,0), (0,1), (0, 2), (0, 3), (1,3), (1,4)]]
Y.update(Positions(*p))

# Piece 12
# ____W
# ____B
#_BWBW

p = ['L', [(1,0), (2,0), (3,0), (4, 0), (4,1), (4,2)]]
Y.update(Positions(*p))

X = defaultdict(set)
for row in Y:
    for col in Y[row]:
        X[col].add(row)

solutions = []
for soln in solve(X, Y):
    board = expand(soln)
    for brd in solutions:
        if equiv(board, brd) : break
    else:                           # loop else                      
        solutions.append(board)
    