import board
import draw
import processBoard as boardProcessor
import processImg as imgProcessor

photoName = ("mona")
tileSize =  5
setShapes = True
setShapeColors = False
setLines = False #Color
setLineColors = False
setDots = False
setDotColors = False

fancyColor = False
greyShades = 14
diagRestrict = False

thresholding = False
threshNum = 0


lineWidth = (tileSize/8)
dotRadius = round((tileSize/6),2)

def main():
    grid = board.Grid()
    fileExt = "DotBoi.eps"
    bprocessor = boardProcessor.Process(tileSize, thresholding, threshNum)
    iprocessor = imgProcessor.Process(tileSize)
    drawer = draw.Drawer(tileSize, setShapeColors, setLines, lineWidth, setDotColors, setDots, \
                         dotRadius, setLineColors, setShapes, fancyColor, greyShades, diagRestrict)

    grid.photo = iprocessor.makeImage(photoName + ".jpg", tileSize)
    bprocessor.makeSquares(grid) #Makes all squares
    bprocessor.makeNeighbors(grid) #Sets neighbors of all squares and creates coords!
    PSFile = open(photoName + fileExt, "w+")
    drawer.drawPS(grid, PSFile)

main()
