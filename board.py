from scipy.misc import toimage

class Grid:
    def __init__(self):
        self.squares = [] #2D array of all squares on the grid in l-r u-d order
        self.photo = None #2D array also
        self.pixelPhoto = [] #Lower-res 2D array

    def showPixelPhoto(self):
        toimage(self.pixelPhoto).show()
