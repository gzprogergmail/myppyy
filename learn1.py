import tkinter as tk
import random

canvas_height = 800
canvas_width = 500
runway_left = 100
runway_right = 400
runway_length = 30
car_width = 30
car_height = 50

def get_random_color():
    colors = ['red', 'green', 'blue', 'yellow', 'purple', 'orange']
    return random.choice(colors)

def create_random_rectangle(y):
   x = random.randint(runway_left, runway_right - car_width)        
   return canvas.create_rectangle(x, y, x+car_width, y+car_height, fill=get_random_color())


# Create the lines of the runway
def create_lines():
    lines = []
    for i in range(0, canvas_height, runway_length*2):
        line = canvas.create_line(runway_left, i, runway_left, i+runway_length, fill='white')
        lines.append(line)
    for i in range(0, canvas_height, runway_length*2):
        line = canvas.create_line(runway_right, i, runway_right, i+runway_length, fill='white')
        lines.append(line)
    return lines

def create_rectangles():
    # Create the rectangles at random x positions and colors
    rectangles = []
    for i in range(0, canvas_height, 120):    
        rectangle = create_random_rectangle(-i)
        rectangles.append(rectangle)
    return rectangles

# Function to move the lines
def move_lines(lines):
    for line in lines:
        canvas.move(line, 0, 5)
        if canvas.coords(line)[3] > canvas_height:  # if the line has moved off the bottom of the canvas
            canvas.move(line, 0, -canvas_height)  # move it back to the top
    window.after(50, move_lines, lines)

# Function to move the rectangles
def move_rectangles(rectangles):
    for rectangle in rectangles:
        canvas.move(rectangle, 0, 6)  # rectangles move slightly faster than the lines
        if canvas.coords(rectangle)[3] > canvas_height:  # if the rectangle has moved off the bottom of the canvas
            canvas.delete(rectangle)  # delete the rectangle
            rectangles.remove(rectangle)  # remove the rectangle from the list
            # create a new rectangle at a random x position at the top
            new_rectangle = create_random_rectangle(0)
            rectangles.append(new_rectangle)  # add the new rectangle to the list
    window.after(50, move_rectangles, rectangles)
    

# Create the main window
window = tk.Tk()
window.title("Moving Runway")

# Set up the canvas
canvas = tk.Canvas(window, width=canvas_width, height=canvas_height, bg='gray')
canvas.pack()




# Start moving the lines and rectangles
lines = create_lines()
rectangles = create_rectangles()
move_lines(lines)
move_rectangles(rectangles)

# Start the game loop
window.mainloop()