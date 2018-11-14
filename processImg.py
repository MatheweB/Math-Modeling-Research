from PIL import Image
import numpy as np

tileSize = None #defines the square size of a given tile

class Process:
    def __init__(self, tSize):
        global tileSize
        tileSize = tSize

        
    def makeDimensionsWork(self, img):
        x = img.size[0]
        y = img.size[1]

        while x%tileSize != 0:
            x += 1
        while y%tileSize != 0:
            y += 1

        img = img.resize([x,y], Image.ANTIALIAS)
        return img


    def numPyIfy(self, img): #creates a 2D array of pixels
        img = np.asarray(img)
        return img

    def makeImage(self, imageName, tSize):
        global tileSize
        tileSize = tSize
        
        img = Image.open(imageName).convert('L') #Black & White
        storedImg = img.copy()
        img.close()

        storedImg = self.makeDimensionsWork(storedImg)
        storedImg = self.numPyIfy(storedImg)

        return storedImg
