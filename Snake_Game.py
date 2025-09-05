from tkinter import *
import random

# Game Config
CELLS = 4 # Ideally even values between 4 and 32
GAME_WIDTH = 720
GAME_HEIGHT = GAME_WIDTH
CELL_SIZE = GAME_WIDTH // CELLS
MAX_CELLS = CELLS * CELLS
UPDATE_INTERVAL = 180

START_SIZE = 3
SNAKE_COLOR = "#0000FF"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#000000"

class Snake:
    def __init__(self):
        self.positions = [] # Coordinates of each part
        self.cells = [] # List of occupied cells

    def create_snake(self):
        self.positions.clear()
        canvas.delete("snake")
        self.cells.clear()

        for i in range(0, START_SIZE):
            self.positions.append([0, 0])
        for x, y in self.positions:
            cell = canvas.create_rectangle(x, y, x + CELL_SIZE, y + CELL_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.cells.append(cell)

class Food:
    def __init__(self):
        self.position = [0, 0] # Position of the food

    def create_food(self):
        while len(snake.positions) < MAX_CELLS:
            x = random.randint(0, GAME_WIDTH // CELL_SIZE - 1) * CELL_SIZE
            y = random.randint(0, GAME_HEIGHT // CELL_SIZE - 1) * CELL_SIZE
            if [x, y] not in snake.positions:
                break
        
        canvas.delete("food")
        self.position = [x, y]
        canvas.create_rectangle(x, y, x + CELL_SIZE, y + CELL_SIZE, fill=FOOD_COLOR, tag="food")

def check_collisions(snake : Snake):
    x, y = snake.positions[0]
    if (x < 0 or x >= GAME_WIDTH) or (y < 0 or y >= GAME_HEIGHT):
        return True
    for body_part in snake.positions[1:]:
        if body_part == [x, y]:
            return True
    return False

def change_direction(dir : str):
    global next_direction
    if dir == 'up' and direction != 'down':
        next_direction = 'up'
    elif dir == 'down' and direction != 'up':
        next_direction = 'down'
    elif dir == 'left' and direction != 'right':
        next_direction = 'left'
    elif dir == 'right' and direction != 'left':
        next_direction = 'right'

def update(snake : Snake, food : Food):
    if not playing:
        return
    
    global direction, next_direction
    if next_direction:
        direction = next_direction
        next_direction = None

    x, y = snake.positions[0]
    if direction == 'up':
        y -= CELL_SIZE
    elif direction == 'down':
        y += CELL_SIZE
    elif direction == 'left':
        x -= CELL_SIZE
    elif direction == 'right':
        x += CELL_SIZE

    snake.positions.insert(0, [x, y])
    cell = canvas.create_rectangle(x, y, x + CELL_SIZE, y + CELL_SIZE, fill=SNAKE_COLOR)
    snake.cells.insert(0, cell)

    if x == food.position[0] and y == food.position[1]:
        global score
        score += 1
        label.config(text="Score: {}".format(score))

        if len(snake.positions) >= MAX_CELLS:
            game_win()
            return
        
        food.create_food()
    else:
        snake.positions.pop()
        canvas.delete(snake.cells.pop())

    if check_collisions(snake):
        game_over()
    else:
        window.after(UPDATE_INTERVAL, update, snake, food)

def game_over():
    global playing
    playing = False
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2, 
                       font=('Arial', 28), text="GAME OVER", fill="red", tag="menu")
    canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2 + 40, 
                       font=('Arial', 18), text="[Space to Play Again]", fill="red", tag="menu")

def game_win():
    global playing
    playing = False
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2, 
                       font=('Arial', 28), text="YOU WIN!", fill="green", tag="menu")
    canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2 + 40, 
                       font=('Arial', 18), text="[Space to Play Again]", fill="green", tag="menu")

def reset_game():
    global playing
    if playing:
        return
    
    global score, direction, next_direction
    playing = True
    score = 0
    direction = 'down'
    next_direction = None

    label.config(text="Score: {}".format(score))
    canvas.delete(ALL)
    
    snake.create_snake()
    food.create_food()
    update(snake, food)

def start_screen():
    canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2 - 40, 
                       font=('Arial', 28), text="SNAKE GAME", fill="white", tag="menu")
    canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2 + 20, 
                       font=('Arial', 18), text="Use arrow keys to move", fill="white", tag="menu")
    canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2 + 60, 
                       font=('Arial', 18), text="Eat the red food to grow", fill="white", tag="menu")
    canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2 + 100, 
                       font=('Arial', 18), text="Press SPACE to start", fill="white", tag="menu")

score = 0
playing = False
direction = 'down'
next_direction = None
snake = Snake()
food = Food()

window = Tk()
window.title("Snake Game")
window.resizable(False, False)

label = Label(window, text="Score: {}".format(score), font=('Arial', 16))
label.pack(side="top")

canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

window.update()
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2
window.geometry(f"{window_width}x{window_height}+{x}+{y}")

window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))
window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<space>', lambda event: reset_game())

canvas.delete(ALL)
start_screen()

window.mainloop()
