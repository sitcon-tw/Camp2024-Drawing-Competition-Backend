import turtle as turtle
import sys

def draw_square(t, size, color):
    t.begin_fill()
    t.color(color)
    for _ in range(4):
        t.forward(size)
        t.right(90)
    t.end_fill()

def draw_creeper_face(t):
    # Set up the drawing environment
    t.speed(0)
    t.penup()
    t.goto(-150, 150)  # Starting position for the face

    # Draw the green background
    t.pendown()
    draw_square(t, 300, "green")

    # Draw the eyes
    eye_positions = [(-90, 90), (30, 90)]
    t.color("black")
    for pos in eye_positions:
        t.penup()
        t.goto(pos)
        t.pendown()
        draw_square(t, 60, "black")

    # Draw the mouth
    mouth_positions = [(-90, -30), (-30, -30), (-30, -90), (30, -30), (30, -90)]
    for pos in mouth_positions:
        t.penup()
        t.goto(pos)
        t.pendown()
        draw_square(t, 60, "black")

def drawing():
    t.speed(0)
    t.penup()
    t.goto(-150, 150)
    
    # Draw green background
    t.pendown()
    t.color("green")
    t.begin_fill()
    for _ in range(4):
        t.forward(300)
        t.right(90)
    t.end_fill()
    
    # Draw eyes
    eye_size = 60
    eye_positions = [(-90, 90), (30, 90)]
    t.color("black")
    for pos in eye_positions:
        t.penup()
        t.goto(pos)
        t.pendown()
        t.begin_fill()
        for _ in range(4):
            t.forward(eye_size)
            t.right(90)
        t.end_fill()
    
    # Draw mouth
    mouth_positions = [(-90, -30), (-30, -30), (-30, -90), (30, -30), (30, -90)]
    for pos in mouth_positions:
        t.penup()
        t.goto(pos)
        t.pendown()
        t.begin_fill()
        for _ in range(4):
            t.forward(eye_size)
            t.right(90)
        t.end_fill()

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
    result_path = sys.argv[1]  # Accept output path as a command-line argument
    s = turtle.getscreen()
    t = turtle.Turtle()
    drawing()
    canvas = s.getcanvas()
    canvas.postscript(file=result_path)
    # turtle.done() # Uncomment this line if you want to keep the turtle graphics window open