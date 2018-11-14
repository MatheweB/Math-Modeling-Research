import square

tileSize = None
thresholding = None
threshNum = None

class Process:

    def __init__(self, tiSize, tHold, tNum):
        global tileSize
        global thresholding
        global threshNum
        tileSize = tiSize
        thresholding = tHold
        threshNum = tNum
        
    def makeSquares(self, grid):

        threshListy = []
        if thresholding == True:
            count = 0
            for x in range(0,threshNum+1):
                threshListy.append(count)
                count += 255/threshNum
                
        squareNum = 0
        totalSquares = 0
        addNum = 0
        switch = 0

        for y in range(0, len(grid.photo)//tileSize):
            grid.squares.append([]) #makes a new level in 2D array
            grid.pixelPhoto.append([])
            for x in range(0, len(grid.photo[0])//tileSize):
                for a in range(0,tileSize):
                    for b in range(0,tileSize):
                        squareNum += grid.photo[y*tileSize + a][x*tileSize + b]

                totalSquares += 1
                newSquare = square.Square((totalSquares%2)+addNum, int(squareNum//(tileSize*tileSize)), x*tileSize, y*tileSize, x, y, tileSize, threshListy)
                grid.squares[y].append(newSquare)
                grid.pixelPhoto[y].append(int(squareNum//(tileSize*tileSize)))
                squareNum = 0

            if switch == 0:
                switch = 1
                totalSquares = 1
                addNum = 2
            else:
                switch = 0
                totalSquares = 0
                addNum = 0


    def makeNeighbors(self, grid):
        for y in range (0, len(grid.squares)):
            for x in range(0, len(grid.squares[0])):
                grid.squares[y][x].setNeighbors(grid.squares,x,y)
                grid.squares[y][x].setNeighborsList()
                grid.squares[y][x].setAvgDarkestC()
                grid.squares[y][x].setDiags()
                grid.squares[y][x].setColors()
                grid.squares[y][x].setDirection()
                grid.squares[y][x].setNewVertexPos()
                
                
                
