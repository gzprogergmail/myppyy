import tkinter as tk
import random
from functools import partial

CANVAS_HEIGHT = 600
CANVAS_WIDTH = 500
RUNWAY_LEFT_X_POSITION = 100
RUNWAY_RIGHT_X_POSITION = CANVAS_WIDTH -100
RUNWAY_LENGTH = 30
CAR_WIDTH = 30
CAR_HEIGHT = 50

def get_random_color():
    colors = ['red', 'green', 'blue', 'yellow', 'purple', 'orange']
    return random.choice(colors)

def create_random_rectangle(y):
   x = random.randint(RUNWAY_LEFT_X_POSITION, RUNWAY_RIGHT_X_POSITION - CAR_WIDTH)        
   return canvas.create_rectangle(x, y, x+CAR_WIDTH, y+CAR_HEIGHT, fill=get_random_color())


# Create the lines of the runway
def create_lines():
    lines = []
    for i in range(0, CANVAS_HEIGHT, RUNWAY_LENGTH*2):
        lines.append(canvas.create_line(RUNWAY_LEFT_X_POSITION, i, RUNWAY_LEFT_X_POSITION, i+RUNWAY_LENGTH, fill='white'))
        lines.append(canvas.create_line(RUNWAY_RIGHT_X_POSITION, i, RUNWAY_RIGHT_X_POSITION, i+RUNWAY_LENGTH, fill='white'))

    return lines

def create_incoming_cars():
    # Create the rectangles at random x positions and colors
    incoming_cars = []
    for i in range(0, CANVAS_HEIGHT, 120):    
        incoming_cars.append(create_random_rectangle(-i))

    return incoming_cars

# Function to move the lines
def move_lines(lines):
    for line in lines:
        canvas.move(line, 0, 5)
        if canvas.coords(line)[3] > CANVAS_HEIGHT:  # if the line has moved off the bottom of the canvas
            canvas.move(line, 0, -CANVAS_HEIGHT)  # move it back to the top

    window.after(50, move_lines, lines)

# Function to move the incoming cars
def move_incoming_cars(incoming_cars, car):
    for incoming_car in incoming_cars:
        canvas.move(incoming_car, 0, 6)  # rectangles move slightly faster than the lines
        if canvas.coords(incoming_car)[3] > CANVAS_HEIGHT:  # if the rectangle has moved off the bottom of the canvas
            canvas.delete(incoming_car)  # delete the rectangle
            incoming_cars.remove(incoming_car)  # remove the rectangle from the list
            # create a new rectangle at a random x position at the top
            incoming_cars.append(create_random_rectangle(0))  # add the new rectangle to the list
        elif do_overlap(canvas.coords(car), canvas.coords(incoming_car)):
            flash_main_car(car)
    window.after(50, move_incoming_cars, incoming_cars, car)
    
#region main car
def create_main_car():
    x = (RUNWAY_LEFT_X_POSITION + RUNWAY_RIGHT_X_POSITION) / 2 - CAR_WIDTH / 2
    y = CANVAS_HEIGHT - CAR_HEIGHT - 10
    return canvas.create_rectangle(x, y, x+CAR_WIDTH, y+CAR_HEIGHT, fill='pink')

# Function to move the main car to the left
def move_main_car_left(event,car):
    x1, y1, x2, y2 = canvas.coords(car)
    if x1 > RUNWAY_LEFT_X_POSITION:
        canvas.move(car, -5, 0)

# Function to move the main car to the right
def move_main_car_right(event, car):
    x1, y1, x2, y2 = canvas.coords(car)
    if x2 < RUNWAY_RIGHT_X_POSITION:
        canvas.move(car, 5, 0)

def flash_main_car(car, color_index=0):
    colors = ['grey', 'white']
    canvas.itemconfig(car, fill=colors[color_index % 2])
    if color_index < 3:  
        window.after(200, flash_main_car, car, color_index + 1)
    else:
        reset_main_car(car)

def do_overlap(rect1, rect2):
    x1, y1, x2, y2 = rect1  # Coordinates of the first rectangle
    x3, y3, x4, y4 = rect2  # Coordinates of the second rectangle

    # Check if the rectangles overlap on the x and y axes
    return not (x2 < x3 or x1 > x4 or y2 < y3 or y1 > y4)

def reset_main_car(car):
    canvas.coords(car, (RUNWAY_LEFT_X_POSITION + RUNWAY_RIGHT_X_POSITION) / 2 - CAR_WIDTH / 2, CANVAS_HEIGHT - CAR_HEIGHT - 10, (RUNWAY_LEFT_X_POSITION + RUNWAY_RIGHT_X_POSITION) / 2 + CAR_WIDTH / 2, CANVAS_HEIGHT - 10)
    canvas.itemconfig(car, fill='pink')

#endregion

# Create the main window
window = tk.Tk()
window.title("Moving Runway")

# Set up the canvas
canvas = tk.Canvas(window, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg='gray')
canvas.pack()


# Start moving the lines and rectangles
lines_list = create_lines()
incoming_cars_list = create_incoming_cars()
main_car = create_main_car()
move_lines(lines_list)
move_incoming_cars(incoming_cars_list, main_car)


# Bind the left and right arrow keys
window.bind('<Left>', partial(move_main_car_left, car=main_car))
window.bind('<Right>', partial(move_main_car_right, car=main_car))

# Start the game loop
window.mainloop()