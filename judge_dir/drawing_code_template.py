import turtle as turtle
import sys
import time
import os
import requests

"""
#################
!!Don't touch the code below!!
Unless you want to uncomment the 'turtle.done()' line
#################
'turtle.done()' is used to keep the turtle graphics window open
Uncomment the line if you want to see the turtle graphics window

However, when judging your code, we don't want to see the turtle graphics window, 
so we commented it
#################
"""

if __name__ == '__main__':
    start_time = time.time()
    ps_file = sys.argv[1]  # Accept output path as a command-line argument
    s = turtle.getscreen()
    pen = turtle.Turtle()

    drawing(pen)

    canvas = s.getcanvas()
    canvas.postscript(file=ps_file)