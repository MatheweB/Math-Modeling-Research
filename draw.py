tileSize = None #defines the square size of a given tile
setColors = True
setLines = True
dotR = None
setDotColors = None
setDots = None
lineWidth = None
setLineColors = False
setShapes = False


greyColor = None
greyShades = []
diagRestrict = None

class Drawer:

    def __init__(self, tSize, setVal, lineBool, lWidth, setDotCol, setD, dotRad, setLineCol, setShap, greyCol, greyShade, dRestrict):
        global tileSize
        global setColors
        global setLines
        global lineWidth
        global dotR
        global setDotColors
        global setDots
        global setLineColors
        global setShapes
        global greyColor
        global greyShades
        global diagRestrict
        setColors = setVal
        tileSize = tSize
        setLines = lineBool
        lineWidth = lWidth
        dotR = dotRad
        setDotColors = setDotCol
        setDots = setD
        setLineColors = setLineCol
        setShapes = setShap
        greyColor = greyCol
        if greyColor:
            count = 0
            for x in range(0,greyShade+1):
                greyShades.append(count)
                count += 255/greyShade
        diagRestrict = dRestrict
        

    def drawDots(self, ytop, f, mySquares, avgColor):
            

        for square in mySquares:
            dotX = str(square.newVertexPos[0]) #X Coord
            dotY = str(ytop - square.newVertexPos[1]) #Y Coord

            if setDotColors == True:
                f.write(str(avgColor) + " setgray\n")
            else:
                f.write("0 setgray\n")
            f.write("newpath\n")
            f.write(dotX + " " + dotY + " " + str(dotR) + " 0 360 arc\n")
            f.write("fill\n")
            f.write("closepath\n\n")


    def findGrey(self, square, avgColor):
        start = greyShades[0]
        end = greyShades[1]

        ahaPoint = 0
        
        if avgColor >= start and avgColor <= end:
            if self.hasConflict(square, start) == False:
                return start
            elif self.hasConflict(square, end) == False:
                return end
        
        if len(greyShades) > 2:
            
            for x in range(2,len(greyShades)):
                start = end
                end = greyShades[x]
                if avgColor >= start and avgColor <= end:
                    if self.hasConflict(square, start) == False:
                        return start
                    elif self.hasConflict(square, end) == False:
                        return end
                    else:
                        ahaPoint = x
                        break
                
            leftC = ahaPoint-1
            rightC = ahaPoint+1
            while (leftC >= 0 or rightC <= len(greyShades)-1):
                if leftC >= 0:
                    if self.hasConflict(square, greyShades[leftC]) == False:
                        return greyShades[leftC]
                    else:
                        leftC -= 1
                    
                if rightC <= len(greyShades)-1:
                    if self.hasConflict(square, greyShades[rightC]) == False:
                        return greyShades[rightC]
                    else:
                        rightC += 1

        
    def hasConflict(self, square, grey):
        conflict = False
        
        if square.N != None:
            if square.N.greyColor == grey:
                conflict = True           

        if square.E != None:
            if square.E.greyColor == grey:
                conflict = True

        if square.S != None:
            if square.S.greyColor == grey:
                conflict = True

        if square.W != None:
            if square.W.greyColor == grey:
                conflict = True

        if diagRestrict == True:
            if square.NE != None:
                if square.NE.greyColor == grey:
                    conflict = True
                    
            if square.NW != None:
                if square.NW.greyColor == grey:
                    conflict = True

            if square.SE != None:
                if square.SE.greyColor == grey:
                    conflict = True

            if square.SW != None:
                if square.SW.greyColor == grey:
                    conflict = True


        return conflict
    
            
                
    def drawSquare(self, grid, f, ytop, mySquares, shapeColor, avgColor):
        noLines = False
        noDots = False
        whiteOnBlack = False
        
        
        if noLines != True:
            #Draws a line to the darkest boi
            if setShapes == True or setLines == True:
                f.write("newpath\n")
                f.write(str(mySquares[0].newVertexPos[0]) + " " + str(ytop - mySquares[0].newVertexPos[1]) + " moveto\n")
                f.write(str(mySquares[1].newVertexPos[0]) + " " + str(ytop - mySquares[1].newVertexPos[1]) + " lineto\n")
                f.write(str(mySquares[3].newVertexPos[0]) + " " + str(ytop - mySquares[3].newVertexPos[1]) + " lineto\n")
                f.write(str(mySquares[2].newVertexPos[0]) + " " + str(ytop - mySquares[2].newVertexPos[1]) + " lineto\n")
                f.write(str(mySquares[0].newVertexPos[0]) + " " + str(ytop - mySquares[0].newVertexPos[1]) + " lineto\n")
                f.write("closepath\n")

            if setShapes == True:
                f.write("gsave\n")
                
                if setColors == True:

                    if greyColor == True:
                        greyCol = self.findGrey(mySquares[0], mySquares[0].avgColor)
                        mySquares[0].greyColor = greyCol
                        f.write(str(greyCol/255) + " setgray\n")

                    else:
                        f.write(str(avgColor) + " setgray\n") #Any spectrum
                    
                elif shapeColor == "white":
                    f.write("1.0 setgray\n")
                else:
                    f.write("0.0 setgray\n")
                
                f.write("fill\n")
                f.write("grestore\n")
            
            if setLineColors == True:
                f.write(str(avgColor) + " setgray\n")
                
            else:
                f.write("0 setgray\n")
            
            f.write("stroke\n\n")

    def drawPS(self, grid, f):

        f.write("%!PS-Adobe-3.0 EPSF-3.0\n%%BoundingBox: 0 0 "+ str(len(grid.photo[0])) + " " + str(len(grid.photo)) + "\n\n")
        f.write("0 0 translate\n")
        f.write("1 setlinejoin\n")
        f.write("1 setlinecap\n")
        if setLines == True:
            f.write(str(lineWidth) + " setlinewidth\n")
        else:
            f.write("0 setlinewidth\n")
        f.write("0.0 setgray\n\n") #Black

        allItems = []
        for y in range(0,len(grid.squares)):
            rowItems = []
            for x in range(0,len(grid.squares[0])):
                rowItems.append([y,x])

            allItems.append(rowItems)
            

        for y in range(0,len(allItems)-1):
            for x in range(0,len(allItems[0])-1):
                if y % 2 == 0:
                    if x % 2 == 0:
                        color = "black"

                    elif x % 2 != 0:
                        color = "white"
                        
                else:
                    if x % 2 == 0:
                        color = "white"

                    elif x % 2 != 0:
                        color = "black"
                    
                one = grid.squares[y][x]
                two = grid.squares[y][x+1]
                three = grid.squares[y+1][x]
                four = grid.squares[y+1][x+1]
                mySquares = [one, two, three, four]

                avgColor = 0
                for square in mySquares:
                    avgColor += square.avgColor
                    
                shapeColor = round(avgColor/4, 2)/255

                self.drawSquare(grid, f, len(grid.photo), mySquares, color, shapeColor)

                if setDots == True:
                    self.drawDots(len(grid.photo), f, mySquares, shapeColor)



        f.write("stroke\n\n")

        f.write("showpage\n\n")
        f.write("%EOF")
        f.close()
