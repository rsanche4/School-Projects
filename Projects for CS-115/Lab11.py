#****
# Name       : Rafael Sanchez
# Pledge     : I pledge my Honor I have abided by the Stevens Honor System
# Motivation : Lab11
#****
from cs5png import PNGImage

def mult(c, n):
    '''Given numbers c & n, return c*n, using only addition and lööps'''
    answerSoFar = 0
    for i in range(c):
        answerSoFar = answerSoFar + n
    return answerSoFar

def update(c, n):
    '''Given numbers c & n,
    return z where z(0, c) = z and z(n, c) = z(n-1, c)**2 + c,
    absolutely no recursion'''
    z = 0
    for i in range(n):
        z = z**2 + c
    return z

def inMSet(c, n):
    '''Given a complex c and a number n, return if the magnitude of z
    never goes above 2 in the process of doing update(...). Don't(!)
    call update'''
    z = 0
    for i in range(n):
        z = z**2 + c
        if abs(z)>2:
            return False
    else:
        return True
    

def scale(pix, pixelMax, floatMin, floatMax):
    '''Given a pixel value, the max pixel value,
    return where that pixel lies on [floatMin, floatMax] where
    pix=0 -> floatMin and pix=pixelMax -> floatMax'''
    x = (floatMax - floatMin)*(pix/pixelMax)
    flot = x + floatMin
    return flot

def mset(n):
    '''Creates a 300x200 image of the Mandelbrot set, where
    the image is of the complex plane with x real [-2, 1] and y imaginary, [-i, i]'''
    width = 300
    height = 200
    image = PNGImage(width, height)

    for col in range(300):
        for row in range(200):
            x = scale(col, 300, -2.0, 1.0)
            y = scale(row, 200, -1.0, 1.0)
            c = x + y*1j
            if inMSet(c, n):
                image.plotPoint(col, row)
    image.saveFile()

if __name__ == "__main__":
    iterations = 25 # Change this to play with the picture, once everything's working
    mset(iterations)



"""
def weWantThisPixel(col, row):
    if col % 10 == 0 or row % 10 == 0:
        return True
    else:
        return False

def test():
    width = 300
    height = 200
    image = PNGImage(width, height)
    for col in range(width):
        for row in range(height):
            if weWantThisPixel(col, row):
                image.plotPoint(col, row)
    image.saveFile()

"""


