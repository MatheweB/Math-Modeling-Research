geometricThresholds = False
geoThreshNum = 20
darkThreshold = (255/2)
tileSize = None #defines the square size of a given tile
import math

class Square:
    def __init__(self, c, avgColor, x, y, gridx, gridy, tSize):

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

    def getColorString(self, color):
        if color == 1 or color == 3:
            return "black"
        else:
            return "white"
        
        
    def setColors(self):
            
        if self.W == None:
            self.squareColors = [self.getColorString(self.c), None]
            

        elif self.E == None:
            self.squareColors = [None, self.getColorString(self.W.c)]

        else:
            self.squareColors = [self.getColorString(self.c), self.getColorString(self.E.c)]

        print(self.squareColors)

        

    def setNewVertexPos(self):

        quadrantX = tileSize/2
        quadrantY = tileSize/2

        #hypoteneuse = math.sqrt(quadrantX**2 + quadrantY**2)

        #scaleSize = hypoteneuse/255

        #scaledHypLenX = self.moveDirection[1][0] * scaleSize
        #scaledHypLenY = self.moveDirection[1][1] * scaleSize

        scaledHypLenX = self.moveDirection[1][0]
        scaledHypLenY = self.moveDirection[1][1]

        if scaledHypLenX < 15:
            scaledHypLenX = 15
        if scaledHypLenY < 15:
            scaledHypLenY  = 15

        if scaledHypLenX > 240:
            scaledHypLenX = 240
        if scaledHypLenY > 240:
            scaledHypLenY  = 240
            
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

    def setDirection(self):

        dirNames = ["NE", "SE", "SW", "NW"]
        
        diagQuadrants = [None for x in range (0,4)]
        
        mySum = self.avgColor

        if self.N != None and self.NE != None and self.E != None:
            mySum = self.N.avgColor + self.NE.avgColor + self.E.avgColor + self.avgColor

            xSum = self.NE.avgColor + self.E.avgColor
            ySum = self.N.avgColor + self.NE.avgColor

            diagQuadrants[0] = [xSum/2, ySum/2, mySum/4]
            
            #diagQuadrants[0] = mySum/4
            
        if self.E != None and self.SE != None and self.S != None:
            xSum = self.E.avgColor + self.SE.avgColor
            ySum = self.SE.avgColor + self.S.avgColor
            mySum = self.E.avgColor + self.SE.avgColor + self.S.avgColor + self.avgColor
            diagQuadrants[1] = [xSum/2, ySum/2, mySum/4]
            #diagQuadrants[1] = mySum/4

        if self.S != None and self.SW != None and self.W != None:
            mySum = self.S.avgColor + self.SW.avgColor + self.W.avgColor + self.avgColor
            xSum = self.SW.avgColor + self.W.avgColor
            ySum = self.S.avgColor + self.SW.avgColor

            diagQuadrants[2] = [xSum/2, ySum/2, mySum/4]
            
            
            #diagQuadrants[2] = mySum/4

        if self.W != None and self.NW != None and self.N != None:
            mySum = self.W.avgColor + self.NW.avgColor + self.N.avgColor + self.avgColor
            xSum = self.W.avgColor + self.NW.avgColor
            ySum = self.NW.avgColor + self.N.avgColor

            diagQuadrants[3] = [xSum/2, ySum/2, mySum/4]
            
            #diagQuadrants[3] = mySum/4

        maxQuad = 0
        darkestNum = 0
        
        for x in range(0,4):
            if diagQuadrants[x] != None:
                if diagQuadrants[x][2]  > darkestNum:
                    maxQuad = x
                    #darkestNum = diagQuadrants[x]
                    darkestNum = diagQuadrants[x][2]

                   
        if darkestNum >= 255/2:
            if self.diagColors[maxQuad].c == 1 or self.diagColors[maxQuad].c == 3: #Black
                self.moveDirection = [dirNames[maxQuad], diagQuadrants[maxQuad]] #Same direction to make smaller
                
                 

            elif self.diagColors[maxQuad].c == 0 or self.diagColors[maxQuad].c == 2: #White
                self.moveDirection = [dirNames[(maxQuad+2)%4], diagQuadrants[maxQuad]] #Opposite direction to make bigger
                 

        elif darkestNum < 255/2:
            if self.diagColors[maxQuad].c == 1 or self.diagColors[maxQuad].c == 3: #Black
                self.moveDirection = [dirNames[(maxQuad+2)%4], diagQuadrants[maxQuad]] #Opposite direction to make bigger
                

            elif self.diagColors[maxQuad].c == 0 or self.diagColors[maxQuad].c == 2: #White
                self.moveDirection = [dirNames[maxQuad], diagQuadrants[maxQuad]] #Same direction to make smaller
                 


        
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

        if geometricThresholds == True:

            tempthresh = geoThreshNum

            for x in range(0,tempthresh):
                if self.avgColor >= (x)*(255/tempthresh) and self.avgColor <= (x+1)*(255/tempthresh):
                    if whiteOnBlack == True:
                        self.avgDarkestC = (x)*(255/tempthresh)
                    else:
                        self.avgDarkestC = 255 - (x)*(255/tempthresh)

        else:
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
