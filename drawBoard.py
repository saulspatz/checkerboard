from PIL import Image
from PIL import ImageDraw
from PIL import ImageFile

WIDTH = 6
BORDER = 8
CELL = 60
SIDE = 8*CELL
MARGIN = 120

def drawSolutions(solutions):
    width = 4*MARGIN + 3*SIDE
    height = 5*MARGIN + 4*SIDE
    board = Image.new("RGB", (width, height) )
    board.palette = None
    draw = ImageDraw.Draw(board, mode="RGB")
    draw.rectangle((0, 0, width, height), fill = 'white')
    for idx, soln in enumerate(solutions):
        row = idx // 3
        col = idx % 3
        x = MARGIN * (col+1) + col * SIDE
        y = MARGIN * (row+1) + row * SIDE
        anchor = (x, y)
        drawBoard(draw, soln, anchor)
    board.save("solutions.png")    

def drawBoard(draw, soln, anchor):
    x0, y0 = anchor
    for x in range(0, SIDE, CELL):
        for y in range(0, SIDE, CELL):
            fill = 'white' if (x+y)//CELL % 2 == 0 else '#A0A0A0'
            draw.rectangle ([x0+x,y0+y,x0+x+CELL,y0+y+CELL], fill=fill)
    x1, y1 = x0+SIDE, y0+SIDE
    draw.line([(x0,y0), (x0, y1)] , fill='black', width = BORDER)
    draw.line([(x0, y1), (x1, y1)] , fill='black', width = BORDER)
    draw.line([(x1, y1), (x1, y0)], fill='black', width = BORDER)
    draw.line([(x1, y0), (x0, y0)] , fill='black', width = BORDER)
    
    for y in range(8):
        for x in range(7):
            if soln[x][y] != soln[x+1][y]:
                draw.line([(x0+CELL*(x+1), y0+CELL*y), (x0+CELL*(x+1), y0+CELL*(y+1)) ], 
                          fill = 'black', width = WIDTH)
                
    for x in range(8):
        for y in range(7):
            if soln[x][y] != soln[x][y+1]:
                draw.line([(x0+CELL*x, y0+CELL*(y+1)), (x0+CELL*(x+1), y0+CELL*(y+1)) ], 
                          fill = 'black', width = WIDTH)  
                                
def printBoard(soln, seq):
    # The first list in the solution is actually the first column of the board.
    # We need to transpose the solution to get it printed right.
        
    soln = zip(*soln)
    with open("board%d.txt" % seq, 'w') as fout:
        fout.write('\n'.join([''.join(row) for row in soln]))
        
            
            