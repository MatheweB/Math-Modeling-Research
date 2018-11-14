tileSize = None #defines the square size of a given tile
import math

class Square:
    def __init__(self, c, avgColor, x, y, gridx, gridy, tSize, threshListy):

        global tileSize
        tileSize = tSize
        
        self.c = c #1 black, 0 white, 2 white, 3 black
        
        self.avgColor = avgColor #the average pixel color of the square
        #Keep track of the square dimensions & location on the Map
        #
        #top left
        self.x = x
        self.y = y
        
        #
        self.xEnd = x + tileSize
        self.yEnd = y + tileSize
        #
        #Location of Dot
        self.dotX = x + (tileSize/2)
        self.dotY = y + (tileSize/2)

        #Neighbors (to know where the slider goes)
        self.N = None
        self.E = None
        self.S = None
        self.W = None
        self.NE = None
        self.NW = None
        self.SW = None
        self.SE = None

        self.neighbors = []

        #Darkest neighbor
        self.avgDarkestC = None

        self.gridx = gridx
        self.gridy = gridy

        self.done = False

        self.diagColors = [None for x in range (0,4)]

        self.moveDirection = None

        self.newVertexPos = None

        self.greyColor = None

        self.squareColors = None

        self.threshList = threshListy

    def setThreshList(self, listy):
        self.threshList = listy
        

    def getBestThresh(self, colorNum):

        start = 0
        end = 0
        for x in range(0,len(self.threshList)-1):
            start = self.threshList[x]
            end = self.threshList[x+1]
            if colorNum >= start and colorNum <= end:
                return end

    def getColorString(self, color):
        if color == 1:
            return "b1"
        if color == 3:
            return "b2"
        if color == 0:
            return "w1"
        else:
            return "w2"
        
        
    def setColors(self):
            
        if self.W == None:
            self.squareColors = [self.getColorString(self.c), None]
            

        elif self.E == None:
            self.squareColors = [None, self.getColorString(self.W.c)]

        else:
            self.squareColors = [self.getColorString(self.c), self.getColorString(self.E.c)]


        

    def setNewVertexPos(self):

        quadrantX = tileSize/2
        quadrantY = tileSize/2

        #hypoteneuse = math.sqrt(quadrantX**2 + quadrantY**2)

        #scaleSize = hypoteneuse/255

        #scaledHypLenX = self.moveDirection[1][0] * scaleSize
        #scaledHypLenY = self.moveDirection[1][1] * scaleSize

        scaledHypLenX = self.moveDirection[2]
        scaledHypLenY = self.moveDirection[3]

        if scaledHypLenX < 30:
            scaledHypLenX = 30
        if scaledHypLenY < 30:
            scaledHypLenY  = 30

        if scaledHypLenX > 190:
            scaledHypLenX = 190
        if scaledHypLenY > 190:
            scaledHypLenY  = 190
            
        xAdd = scaledHypLenX*((tileSize/2)/255)
        yAdd = scaledHypLenY*((tileSize/2)/255)

        
        #xAdd = math.sqrt(scaledHypLen) / math.sqrt(2)
        #yAdd = math.sqrt(scaledHypLen) / math.sqrt(2)


        if self.moveDirection[0] == "NE":
            yMult = -1
            xMult = 1

        elif self.moveDirection[0] == "SE":
            yMult = 1
            xMult = 1

        elif self.moveDirection[0] == "SW":
            yMult = 1
            xMult = -1

        elif self.moveDirection[0] == "NW":
            yMult = -1
            xMult = -1

        #newX = 

        self.newVertexPos = [round(self.dotX + (xMult*xAdd),2), round(self.dotY + (yMult*yAdd),2)] #[newX,newY]
        

    def setDiags(self):
        if self.NE != None:
            self.diagColors[0] = self.NE

        if self.SE != None:
            self.diagColors[1] = self.SE

        if self.SW != None:
            self.diagColors[2] = self.SW

        if self.NW != None:
            self.diagColors[3] = self.NW

    def getAvgColor(self, col1, neighbor):

        count = 1
        summ = col1
        if neighbor != None:
            count += 1
            summ += neighbor.avgColor

        return summ/count
    

    def setDirection(self):

        neighborList = [self.N, self.E, self.S, self.W]
        mySum = self.avgColor
        count = 1

        for neighbor in neighborList:
            try:
                mySum += neighbor.avgColor
                count += 1
            except:
                continue

        avgColor = mySum/count

        
        if avgColor >= 255/2:
            if self.squareColors[0] == "w1":
                
                xMove = self.getAvgColor(self.avgColor, self.W)
                yMove = self.getAvgColor(self.avgColor, self.N)

            elif self.squareColors[0] == "b1":
                xMove = self.getAvgColor(self.avgColor, self.E)
                yMove = self.getAvgColor(self.avgColor, self.N)

            elif self.squareColors[0] == "w2":
                xMove = self.getAvgColor(self.avgColor, self.E)
                yMove = self.getAvgColor(self.avgColor, self.S)
                
            elif self.squareColors[0] == "b2":
                xMove = self.getAvgColor(self.avgColor, self.W)
                yMove = self.getAvgColor(self.avgColor, self.S)
                
            elif self.squareColors[1] == "w1":
                xMove = self.getAvgColor(self.avgColor, self.E)
                yMove = self.getAvgColor(self.avgColor, self.N)
                
            elif self.squareColors[1] == "b1":
                xMove = self.getAvgColor(self.avgColor, self.W)
                yMove = self.getAvgColor(self.avgColor, self.N)

            elif self.squareColors[1] == "w2":
                xMove = self.getAvgColor(self.avgColor, self.W)
                yMove = self.getAvgColor(self.avgColor, self.S)
                
            elif self.squareColors[1] == "b2":
                xMove = self.getAvgColor(self.avgColor, self.E)
                yMove = self.getAvgColor(self.avgColor, self.S)
                 

        elif avgColor < 255/2:
            if self.squareColors[0] == "w1":
                xMove = self.getAvgColor(self.avgColor, self.E)
                yMove = self.getAvgColor(self.avgColor, self.N)

            elif self.squareColors[0] == "b1":
                xMove = self.getAvgColor(self.avgColor, self.W)
                yMove = self.getAvgColor(self.avgColor, self.N)

            elif self.squareColors[0] == "w2":
                xMove = self.getAvgColor(self.avgColor, self.W)
                yMove = self.getAvgColor(self.avgColor, self.S)
                
            elif self.squareColors[0] == "b2":
                xMove = self.getAvgColor(self.avgColor, self.E)
                yMove = self.getAvgColor(self.avgColor, self.S)
                
            elif self.squareColors[1] == "w1":
                xMove = self.getAvgColor(self.avgColor, self.W)
                yMove = self.getAvgColor(self.avgColor, self.N)
                
            elif self.squareColors[1] == "b1":
                xMove = self.getAvgColor(self.avgColor, self.E)
                yMove = self.getAvgColor(self.avgColor, self.N)

            elif self.squareColors[1] == "w2":
                xMove = self.getAvgColor(self.avgColor, self.E)
                yMove = self.getAvgColor(self.avgColor, self.S)
                
            elif self.squareColors[1] == "b2":
                xMove = self.getAvgColor(self.avgColor, self.W)
                yMove = self.getAvgColor(self.avgColor, self.S)

        if len(self.threshList) != 0:
            xMove = self.getBestThresh(xMove)
            yMove = self.getBestThresh(yMove)
                   
        if avgColor >= 255/2:
            if self.squareColors[0] == "w1":
                self.moveDirection = ["NW", avgColor, xMove, yMove]

            elif self.squareColors[0] == "b1":
                self.moveDirection = ["NE", avgColor, xMove, yMove]

            elif self.squareColors[0] == "w2":
                self.moveDirection = ["SE", avgColor, xMove, yMove]
                
            elif self.squareColors[0] == "b2":
                self.moveDirection = ["SW", avgColor, xMove, yMove]
                
            elif self.squareColors[1] == "w1":
                self.moveDirection = ["NE", avgColor, xMove, yMove]
                
            elif self.squareColors[1] == "b1":
                self.moveDirection = ["NW", avgColor, xMove, yMove]

            elif self.squareColors[1] == "w2":
                self.moveDirection = ["SW", avgColor, xMove, yMove]
                
            elif self.squareColors[1] == "b2":
                self.moveDirection = ["SE", avgColor, xMove, yMove]
                 

        elif avgColor < 255/2:
            if self.squareColors[0] == "w1":
                self.moveDirection = ["NE", avgColor, xMove, yMove]

            elif self.squareColors[0] == "b1":
                self.moveDirection = ["NW", avgColor, xMove, yMove]

            elif self.squareColors[0] == "w2":
                self.moveDirection = ["SW", avgColor, xMove, yMove]
                
            elif self.squareColors[0] == "b2":
                self.moveDirection = ["SE", avgColor, xMove, yMove]
                
            elif self.squareColors[1] == "w1":
                self.moveDirection = ["NW", avgColor, xMove, yMove]
                
            elif self.squareColors[1] == "b1":
                self.moveDirection = ["NE", avgColor, xMove, yMove]

            elif self.squareColors[1] == "w2":
                self.moveDirection = ["SE", avgColor, xMove, yMove]
                
            elif self.squareColors[1] == "b2":
                self.moveDirection = ["SW", avgColor, xMove, yMove]                
            
                 


        
    def setNeighborsList(self):
        if self.N != None:
            self.neighbors.append(self.N)
        if self.E != None:
            self.neighbors.append(self.E)
        if self.S != None:
            self.neighbors.append(self.S)
        if self.W != None:
            self.neighbors.append(self.W)

        if self.NE != None:
            self.neighbors.append(self.NE)
        if self.NW != None:
            self.neighbors.append(self.NW)
        if self.SE != None:
            self.neighbors.append(self.SE)
        if self.SW != None:
            self.neighbors.append(self.SW)



    def setAvgDarkestC(self):

##        if geometricThresholds == True:
##
##            tempthresh = geoThreshNum
##
##            for x in range(0,tempthresh):
##                if self.avgColor >= (x)*(255/tempthresh) and self.avgColor <= (x+1)*(255/tempthresh):
##                    if whiteOnBlack == True:
##                        self.avgDarkestC = (x)*(255/tempthresh)
##                    else:
##                        self.avgDarkestC = 255 - (x)*(255/tempthresh)

        #else:
        totalC = 0
        for neighbor in self.neighbors:
            totalC += neighbor.avgColor

        self.avgDarkestC = totalC/len(self.neighbors)



    def setNeighbors(self, squares, x, y):
        maxX = len(squares[0])
        maxY = len(squares)
        minY = 0
        minX = 0

        if (y-1) < minY:
            self.N = None
        else:
            self.N = squares[y-1][x]

        if (x+1) >= maxX:
            self.E = None
        else:
            self.E = squares[y][x+1]

        if (y+1) >= maxY:
            self.S = None
        else:
            self.S = squares[y+1][x]

        if (x-1) < minX:
            self.W = None
        else:
            self.W = squares[y][x-1]

        if (y-1) < minY or (x+1) >= maxX:
            self.NE = None
        else:
            self.NE = squares[y-1][x+1]

        if (y-1) < minY or (x-1) < minX:
            self.NW = None
        else:
            self.NW = squares[y-1][x-1]

        if (y+1) >= maxY or (x-1) < minX:
            self.SW = None
        else:
            self.SW = squares[y+1][x-1]

        if (y+1) >= maxY or (x+1) >= maxX:
            self.SE = None
        else:
            self.SE = squares[y+1][x+1]
