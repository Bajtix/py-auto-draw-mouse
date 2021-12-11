# created by bajtixone during a maths lesson
# 10.12.21

from svg.path import Path, Line, Arc, CubicBezier, QuadraticBezier, Move, Close, parse_path
import pyautogui
import time
import argparse, sys

# args

parser=argparse.ArgumentParser()

parser.add_argument("path", type=str, help="Plik ze ścieżką")

parser.add_argument('--scale', type=float, help='Skala z jaką jest rysowany', default=4)
parser.add_argument('--samples', type=int, help='Ilość sampli do interpolacji', default=5)

args=parser.parse_args()

def file_text(t):
    f = open(t, "r")
    r = f.read()
    f.close()
    return r

class pt:
    def __init__(self, x,y):
        self.x = x
        self.y =y

# settings
scale = args.scale
samples = args.samples
path = file_text(args.path) #zapisana w pliku

# code
points = []
isUp = []
ppath = parse_path(path)
segs = ppath._segments; #to jest tak zajebiście śmieszna nazwa zmiennej.  x kurcze D

print("Loading " +str(len(segs)) + " segments")

for s in segs:
    o = s.point(0)
    points.append(pt(o.real, o.imag))
    isUp.append(isinstance(s, Move))
    for v in range(0,samples):
        pp = v/samples
        if(pp == 0 or pp == 1): 
            continue
        o = s.point(pp)
        points.append(pt(o.real, o.imag))
        isUp.append(isinstance(s, Move))
    o = s.point(1)
    points.append(pt(o.real, o.imag))
    isUp.append(isinstance(s, Move))
    

clen = len(points);

print("Found " + str(clen) + " points. Get ready and move your mouse to the desired location! Drawing in 7 s")

time.sleep(7)

up = True

initX, initY = pyautogui.position()

shX = points[2].x
shY = points[2].y

for v in range(1, clen-1):
    print("Drawing " + str(v) + "/" + str(clen) + "  ("+str(v/clen * 100) + "%)")
    if(isUp[v]):
        if not up:
            pyautogui.mouseUp()
            up = True
    else:
        if up:
            pyautogui.mouseDown()
            up = False
    e = points[v]
    dx = e.x * scale + initX - (shX * scale)
    dy = e.y * scale + initY - (shY * scale)
    pyautogui.moveTo(dx,dy)

pyautogui.mouseUp()

print("All done!")