import tkinter as tk
import random
import time
from functools import partial

CANVAS_HEIGHT = 600
CANVAS_WIDTH = 450
RUNWAY_LEFT_X_POSITION = 100
RUNWAY_RIGHT_X_POSITION = CANVAS_WIDTH -100
RUNWAY_LENGTH = 30
CAR_WIDTH = 35
CAR_HEIGHT = 50

def init_score_and_lives_display(canvas):
    global _score_text, _lives_text, _score, _lives
    _score = 0
    _lives = 5
    _score_text = canvas.create_text(RUNWAY_LEFT_X_POSITION - 50, 10, text=f"Score: {_score}", fill='black', font=('Helvetica', 15))
    _lives_text = canvas.create_text(RUNWAY_RIGHT_X_POSITION + 50, 10, text=f"Lives: {_lives}", fill='black', font=('Helvetica', 15))
    _display_score()
    _display_lives()

def get_random_color():
    colors = ['red', 'green', 'blue', 'yellow', 'purple', 'orange']
    return random.choice(colors)

def create_random_incoming_car(y, existing_incoming_cars):
    while True:
        x = random.randint(RUNWAY_LEFT_X_POSITION, RUNWAY_RIGHT_X_POSITION - CAR_WIDTH)
        new_car = canvas.create_rectangle(x, y, x+CAR_WIDTH, y+CAR_HEIGHT, fill=get_random_color())
        if not any(do_overlap(canvas.coords(new_car), canvas.coords(car)) for car in existing_incoming_cars):
            return new_car
        else:
            canvas.delete(new_car)

def increase_score():
    global _score
    _score += 1
    _display_score()

def _display_score():
    global _score, _score_text
    canvas.itemconfig(_score_text, text=f"Score: {_score}")

def decrease_lives():
    global _lives
    _lives -= 1
    _display_lives()

def _display_lives():
    global _lives, _lives_text
    canvas.itemconfig(_lives_text, text=f"Lives: {_lives}")

def is_end_game():
    global _lives
    return _lives == 0

def end_game():
    game_over_text = "Game Over"
    canvas.create_text(CANVAS_WIDTH/2, CANVAS_HEIGHT/2, text=game_over_text, fill='red', font=('Helvetica', 30))


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
        incoming_cars.append(create_random_incoming_car(-i, incoming_cars))

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
    for incoming_car in incoming_cars.copy():
        canvas.move(incoming_car, 0, 6)
        if canvas.coords(incoming_car)[3] > CANVAS_HEIGHT:
            canvas.delete(incoming_car)
            incoming_cars.remove(incoming_car)
            incoming_cars.append(create_random_incoming_car(0, incoming_cars))
            increase_score()  # Update the score display            
        elif do_overlap(canvas.coords(car), canvas.coords(incoming_car)):
            canvas.delete(incoming_car)
            incoming_cars.remove(incoming_car)
            incoming_cars.append(create_random_incoming_car(0, incoming_cars))
            flash_main_car(car)
            decrease_lives()  # Decrement the lives
            if is_end_game():  # If no lives left
                end_game()  # End the game
                return  # Exit the function to stop moving the cars
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

def flash_main_car(car):
    for _ in range(5):
        canvas.itemconfig(car, fill='red')
        window.update()
        time.sleep(0.1)
        canvas.itemconfig(car, fill='white')
        window.update()
        time.sleep(0.1)
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
init_score_and_lives_display(canvas)

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