import argparse
from PIL import Image
import numpy as np
import random as r


def addWanderingLine(data, args, color):
    height, width, colorRange = data.shape
    x,y = r.randint(0,height-args.startBoundary), r.randint(0,width-args.startBoundary)
    length = r.randint(args.minLineLength, args.maxLineLength)

    currentLength = 0
    change_every = r.randint(args.minChangeDirection,args.maxChangeDirection)
    xDirection, yDirection = r.randint(-args.xDelta,args.xDelta), r.randint(-args.yDelta,args.yDelta)
    while currentLength < length:
        if currentLength % change_every == 0:
            xDirection, yDirection = r.randint(-args.xDelta,args.xDelta), r.randint(-args.yDelta,args.yDelta)
        currentLength += 1
        x += xDirection
        y += yDirection

        if x > width-args.endBoundry or x < 0+args.endBoundry or y > height-args.endBoundry or y < 0+args.endBoundry:
            return data

        data[x,y] = color
        data[x+1,y] = color
        data[x-1,y] = color
        data[x+2,y] = color
        data[x-2,y] = color

    return data

Pantone_Colors = [
    [255,92,57],
    [137,178,196],
    [80,166,132],
    [255,134,116],
]

def paint(args):
    data = np.zeros((args.height, args.width, 3))
    for x in range(0,args.numLines):
        data = addWanderingLine(data, args, r.choice(Pantone_Colors))
    return data

def saveImage(painting, name="painting.png"):
    img = (painting).astype(np.uint8)
    img = Image.fromarray(img)
    img.save(name)

def saveAndShowImage(painting, name="painting.png"):
    img = (painting).astype(np.uint8)
    img = Image.fromarray(img)
    img.save(name)
    img.show()

parser = argparse.ArgumentParser(description='Generate Images by Drawing Random Lines.')
parser.add_argument('--height', '-he', type=int, default=2000, help='height of image in pixels. default 2000')
parser.add_argument('--width', '-wi', type=int, default=2000, help='width of image in pixels. default 2000')
parser.add_argument('--numPaintings', '-np', type=int, default=20, help='number of paintings to generate. default 20')
parser.add_argument('--numLines', '-nl', type=int, default=20, help='number of lines to draw. default 500')
parser.add_argument('--startBoundary', '-sb', type=int, default=500, help='restrict the start point to be this pixel distance away from the edge. default 500')
parser.add_argument('--endBoundry', '-eb', type=int, default=500, help='stop line if it comes this close to edge. default 500')
parser.add_argument('--minLineLength', '-mln', type=int, default=500, help='minimum length of each line in pixels. default 500')
parser.add_argument('--maxLineLength', '-mlp', type=int, default=2000, help='maximum length of each line of pixels. default 2000')
parser.add_argument('--minChangeDirection', '-cgn', type=int, default=200, help='minimum line length before possibly changing direction. default 5')
parser.add_argument('--maxChangeDirection', '-cgp', type=int, default=800, help='maximum line length before possibly changing direction. default 10')
parser.add_argument('--xDelta', '-xd', type=int, default=1, help='possible change in x direction. default 1')
parser.add_argument('--yDelta', '-yd', type=int, default=1, help='possible change in y direction. default 1')
args = parser.parse_args()

for x in range(0,args.numPaintings):
    painting = paint(args)
    saveImage(painting, name="painting-" + str(x)+ '.png')
    #saveAndShowImage(painting)
