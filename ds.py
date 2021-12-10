# created by bajtixone during a maths lesson
# 10.12.21

from svg.path import Path, Line, Arc, CubicBezier, QuadraticBezier, Move, Close, parse_path
import pyautogui
import time
import argparse, sys

# SKŁADNIKI

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

# USTAWIENIA
scale = args.scale
samples = args.samples
path = file_text(args.path) #zapisana w pliku




# KOD
points = []
isUp = []
ppath = parse_path(path)
segs = ppath._segments; #to jest tak zajebiście śmieszna nazwa zmiennej.  x kurcze D


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

print("Znaleziono " + str(clen) + " pkt. Przygotuj się! Rysowanie za 5 s")

time.sleep(5)

up = True

initX, initY = pyautogui.position()

shX = points[2].x
shY = points[2].y

for v in range(1, clen-1):
    print("Rysuję " + str(v) + "/" + str(clen))
    if(isUp[v]):
        if not up:
            pyautogui.mouseUp()
            up = True
    else:
        if up:
            pyautogui.mouseDown()
            up = False
    e = points[v]
    #dx = (e.x * scale) - (s.x* scale)
    #dy = (e.y * scale) - (s.y * scale)
    dx = e.x * scale + initX - (shX * scale)
    dy = e.y * scale + initY - (shY * scale)
    pyautogui.moveTo(dx,dy)

pyautogui.mouseUp()

print("Gotowe!")