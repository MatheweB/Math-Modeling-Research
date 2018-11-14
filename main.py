import board
import draw
import processBoard as boardProcessor
import processImg as imgProcessor

photoName = ("b")
tileSize =  10
setShapes = True
setShapeColors = True
setLines = False #Color
setLineColors = False
setDots = False
setDotColors = False

fancyColor = True
greyShades = 1
diagRestrict = False


lineWidth = (tileSize/8)
dotRadius = round((tileSize/6),2)

def main():
    grid = board.Grid()
    fileExt = "DotBoi.eps"
    bprocessor = boardProcessor.Process(tileSize)
    iprocessor = imgProcessor.Process(tileSize)
    drawer = draw.Drawer(tileSize, setShapeColors, setLines, lineWidth, setDotColors, setDots, \
                         dotRadius, setLineColors, setShapes, fancyColor, greyShades, diagRestrict)

    grid.photo = iprocessor.makeImage(photoName + ".jpg", tileSize)
    bprocessor.makeSquares(grid) #Makes all squares
    bprocessor.makeNeighbors(grid) #Sets neighbors of all squares and creates coords!
    PSFile = open(photoName + fileExt, "w+")
    drawer.drawPS(grid, PSFile)

main()
