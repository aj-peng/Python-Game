from tkinter import *
import random

# Configuration
CELLS = 4  # Ideally even values between 4 and 32
GAME_WIDTH = 720
GAME_HEIGHT = GAME_WIDTH
CELL_SIZE = GAME_WIDTH // CELLS
MAX_CELLS = CELLS * CELLS
ALL_CELLS = set((x * CELL_SIZE, y * CELL_SIZE)
                for x in range(GAME_WIDTH // CELL_SIZE)
                for y in range(GAME_HEIGHT // CELL_SIZE))

UPDATE_INTERVAL = 180
START_SIZE = 3
SNAKE_COLOR = "#03254c"
HEAD_COLOR = "#1167b1"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#000000"

# Game state
score = 0
playing = False

# Class definitions
class Snake:
    def __init__(self):
        self.cells = []  # List of occupied cells
        self.positions = []  # Coordinates of each part
        self.direction = 'down'  # Current direction
        self.next_direction = None  # Next turning direction

    def create_snake(self):
        self.cells.clear()
        self.positions.clear()
        self.direction = 'down'
        self.next_direction = None

        canvas.delete("snake")
        for _ in range(START_SIZE):
            self.positions.append([0, 0])
        for x, y in self.positions:
            cell = canvas.create_rectangle(x, y, x + CELL_SIZE, y + CELL_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.cells.append(cell)

    def get_position(self):
        return self.positions[0]

    def change_direction(self, direction):
        if direction == 'up' and self.direction != 'down':
            self.next_direction = 'up'
        elif direction == 'down' and self.direction != 'up':
            self.next_direction = 'down'
        elif direction == 'left' and self.direction != 'right':
            self.next_direction = 'left'
        elif direction == 'right' and self.direction != 'left':
            self.next_direction = 'right'
    
    def check_collisions(self):
        x, y = self.get_position()
        if (x < 0 or x >= GAME_WIDTH) or (y < 0 or y >= GAME_HEIGHT):
            return True
        for body_part in self.positions[1:]:
            if body_part == [x, y]:
                return True
        return False

class Food:
    def __init__(self):
        self.position = [0, 0]  # Position of the food

    def create_food(self):
        occupied = set(tuple(pos) for pos in snake.positions)
        free_cells = list(ALL_CELLS - occupied)
        if not free_cells:
            return
        
        self.position = list(random.choice(free_cells))
        x, y = self.get_position()
        canvas.delete("food")
        canvas.create_rectangle(x, y, x + CELL_SIZE, y + CELL_SIZE, fill=FOOD_COLOR, tag="food")

    def get_position(self):
        return self.position

# Game functions
def update(snake: Snake, food: Food):
    if not playing:
        return
    
    if snake.next_direction:
        snake.direction = snake.next_direction
        snake.next_direction = None

    x, y = snake.get_position()
    if snake.direction == 'up':
        y -= CELL_SIZE
    elif snake.direction == 'down':
        y += CELL_SIZE
    elif snake.direction == 'left':
        x -= CELL_SIZE
    elif snake.direction == 'right':
        x += CELL_SIZE
    
    snake.positions.insert(0, [x, y])
    cell = canvas.create_rectangle(x, y, x + CELL_SIZE, y + CELL_SIZE, fill=SNAKE_COLOR, tag="snake")
    snake.cells.insert(0, cell)

    if len(snake.cells) > 1:
        canvas.itemconfig(snake.cells[1], fill=SNAKE_COLOR)
    canvas.itemconfig(snake.cells[0], fill=HEAD_COLOR)

    food_x, food_y = food.get_position()
    if x == food_x and y == food_y:
        global score
        score += 1
        label.config(text=f"Score: {score}")

        if len(snake.positions) >= MAX_CELLS:
            game_win()
            return
        food.create_food()
    else:
        snake.positions.pop()
        cell = snake.cells.pop()
        canvas.delete(cell)

    if snake.check_collisions():
        game_over()
    else:
        window.after(UPDATE_INTERVAL, update, snake, food)

def display_text(text: str, subtext: str, color: str):
    canvas.delete(ALL)
    canvas.create_text(GAME_WIDTH / 2, GAME_HEIGHT / 2, 
                     font=('Arial', 28), text=text, fill=color, tag="menu")
    canvas.create_text(GAME_WIDTH / 2, GAME_HEIGHT / 2 + 40, 
                     font=('Arial', 18), text=subtext, fill=color, tag="menu")

def game_over():
    global playing
    playing = False
    display_text("GAME OVER", "[Space to Play Again]", "red")

def game_win():
    global playing
    playing = False
    display_text("YOU WIN!", "[Space to Play Again]", "green")

def reset_game():
    global playing, score
    if playing:
        return
    
    playing = True
    score = 0
    label.config(text="Score: {}".format(score))
    canvas.delete(ALL)
    snake.create_snake()
    food.create_food()
    update(snake, food)

def start_screen():
    canvas.delete(ALL)
    canvas.create_text(GAME_WIDTH / 2, GAME_HEIGHT / 2 - 40, 
                     font=('Arial', 28), text="SNAKE GAME", fill="white", tag="menu")
    canvas.create_text(GAME_WIDTH / 2, GAME_HEIGHT / 2 + 20, 
                     font=('Arial', 18), text="Use arrow keys to move", fill="white", tag="menu")
    canvas.create_text(GAME_WIDTH / 2, GAME_HEIGHT / 2 + 60, 
                     font=('Arial', 18), text="Eat the red food to grow", fill="white", tag="menu")
    canvas.create_text(GAME_WIDTH / 2, GAME_HEIGHT / 2 + 100, 
                     font=('Arial', 18), text="Press SPACE to start", fill="white", tag="menu")

# Setup
snake = Snake()
food = Food()

window = Tk()
window.title("Snake Game")
window.resizable(False, False)

label = Label(window, text=f"Score: {score}", font=('Arial', 16))
label.pack(side="top")

canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.focus_set()
canvas.pack()

window.update()
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

offset_x = (screen_width - window_width) // 2
offset_y = (screen_height - window_height) // 2
window.geometry(f"{window_width}x{window_height}+{offset_x}+{offset_y}")

window.bind('<Up>', lambda event: snake.change_direction('up'))
window.bind('<Down>', lambda event: snake.change_direction('down'))
window.bind('<Left>', lambda event: snake.change_direction('left'))
window.bind('<Right>', lambda event: snake.change_direction('right'))
window.bind('<space>', lambda event: reset_game())

start_screen()
window.mainloop()
