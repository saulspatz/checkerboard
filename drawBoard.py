from PIL import Image
from PIL import ImageDraw
from PIL import ImageFile

WIDTH = 6
BORDER = 8

def drawBoard(soln, seq):
    board = Image.new("RGB", (640, 640) )
    board.palette = None
    draw = ImageDraw.Draw(board, mode="RGB")
    for x in range(0, 640, 80):
        for y in range(0, 640, 80):
            fill = 'white' if (x+y)//80 % 2 else '#A0A0A0'
            draw.rectangle ([x,y,x+80,y+80], fill=fill)
    draw.line([(0,0), (0, 639)] , fill='black', width = BORDER)
    draw.line([(0, 639), (639, 639)] , fill='black', width = BORDER)
    draw.line([(639, 639), (639, 0)] , fill='black', width = BORDER)
    draw.line([(639, 0), (0, 0)] , fill='black', width = BORDER)
    
    # The y coordinate comes FIRST in the solution
    for y in range(8):
        for x in range(7):
            if soln[y][x] != soln[y][x+1]:
                draw.line([(80*(x+1), 80*y), (80*(x+1), 80*(y+1)) ], fill = 'black', width = WIDTH)
                
    for x in range(8):
        for y in range(7):
            if soln[y][x] != soln[y+1][x]:
                draw.line([(80*x, 80*(y+1)), (80*(x+1), 80*(y+1)) ], fill = 'black', width = WIDTH)  
                
    fn = "board%d.png" % seq
    board.save(fn)
                
def printBoard(soln, seq):
    with open("board%d.txt" % seq, 'w') as fout:
        fout.write('\n'.join([''.join(row) for row in soln]))
        
            
            