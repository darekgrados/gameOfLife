#pygame

# To create & start using python venv:
#       python -m venv venv
#       source venv/bin/activate

# Install specific modules with pip:
# f.e.:   pip install pygame

# Requirements
# 1. Make simulation real time
# 2. Add pause / resume logic
# 3. Add save / load logic

# High-level logic
# 1. Create and init the simulation grid
# 2. Start the simulation with a tick interval of <n> seconds
# 3. At each tick:
#   3.1. Update the grid - loop over each element of the board
#   3.2. Render new generation

# General approach
# 1. Plan & write down the general workflow
#  1.1. Define Input&Output 
#  1.2. Consider adding validation
# 2. Separate the main algorithms / actors in the code. Try to abstract as much common code as possible
# 3. Define communication between the objects
# 4. List the patterns you could apply
# 5. Build PoCs (Proof of concepts). Try to separate implementation of specific steps. Prepare smaller modules
#    and combine them into a complete application
# 6. Refine if needed

# Deadline - 15th of December 2023
# Mail with: 
# 1. short screen recording demonstrating the new features
# 2. Linked code
# 3. Short description of the changes. Which design patterns you used and how you applied them. 

import pygame
import numpy as np

# Initialize Pygame
pygame.init()

# Screen dimensions
width, height = 1200, 800
screen = pygame.display.set_mode((width, height))

# Grid dimensions
n_cells_x, n_cells_y = 40, 30
cell_width = width // n_cells_x
cell_height = height // n_cells_y

# Game state
game_state = np.random.choice([0, 1], size=(n_cells_x, n_cells_y), p=[0.8, 0.2])

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
gray = (128, 128, 128)
green = (0, 255, 0)

# Button dimensions
button_width, button_height = 200, 50
button_x, button_y = (width - button_width) // 2 - 150, height - button_height - 10
restart_button_x, restart_button_y = (width - button_width) // 2 + 150, height - button_height - 10

# Game variables
clock = pygame.time.Clock()
time_per_frame = 1.0  # Calculate the time per frame in seconds
paused = False
running = True

class State:
    def __init__(self):
        self.state_num = 1
        self.state_num += 1

state = State()

class GameUI:
    def draw_button():
        pygame.draw.rect(screen, green, (button_x, button_y, button_width, button_height))
        font = pygame.font.Font(None, 36)
        text = font.render("Next Generation", True, black)
        text_rect = text.get_rect(center=(button_x + button_width // 2, button_y + button_height // 2))
        screen.blit(text, text_rect)

    def draw_restart_button():
        pygame.draw.rect(screen, green, (restart_button_x, button_y, button_width, button_height))
        font = pygame.font.Font(None, 36)
        text = font.render("Restart", True, black)
        text_rect = text.get_rect(center=(restart_button_x + button_width // 2, button_y + button_height // 2))
        screen.blit(text, text_rect)

    def draw_grid():
        for y in range(0, height, cell_height):
            for x in range(0, width, cell_width):
                cell = pygame.Rect(x, y, cell_width, cell_height)
                pygame.draw.rect(screen, gray, cell, 1)

class GameLogic:
    def next_generation():
        global game_state
        new_state = np.copy(game_state)

        for y in range(n_cells_y):
            for x in range(n_cells_x):
                n_neighbors = game_state[(x - 1) % n_cells_x, (y - 1) % n_cells_y] + \
                            game_state[(x) % n_cells_x, (y - 1) % n_cells_y] + \
                            game_state[(x + 1) % n_cells_x, (y - 1) % n_cells_y] + \
                            game_state[(x - 1) % n_cells_x, (y) % n_cells_y] + \
                            game_state[(x + 1) % n_cells_x, (y) % n_cells_y] + \
                            game_state[(x - 1) % n_cells_x, (y + 1) % n_cells_y] + \
                            game_state[(x) % n_cells_x, (y + 1) % n_cells_y] + \
                            game_state[(x + 1) % n_cells_x, (y + 1) % n_cells_y]

                if game_state[x, y] == 1 and (n_neighbors < 2 or n_neighbors > 3):
                    new_state[x, y] = 0
                elif game_state[x, y] == 0 and n_neighbors == 3:
                    new_state[x, y] = 1

        game_state = new_state

    def restart_game():
        global game_state
        game_state = np.random.choice([0, 1], size=(n_cells_x, n_cells_y), p=[0.8, 0.2])

    def draw_cells():
        for y in range(n_cells_y):
            for x in range(n_cells_x):
                cell = pygame.Rect(x * cell_width, y * cell_height, cell_width, cell_height)
                if game_state[x, y] == 1:
                    pygame.draw.rect(screen, black, cell)


while running:
    def save_state(filename):
        np.save(filename, game_state)

    def load_state(filename):
        global game_state
        game_state = np.load(filename)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                paused = not paused
            elif event.key == pygame.K_s:
                save_state("saved_state.npy")
            elif event.key == pygame.K_l:
                load_state("saved_state.npy")
            elif event.key == pygame.K_r:
                GameUI.restart_game()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if button_x <= event.pos[0] <= button_x + button_width and button_y <= event.pos[
                1] <= button_y + button_height:
                GameUI.next_generation()
            elif restart_button_x <= event.pos[0] <= restart_button_x + button_width and button_y <= event.pos[
                1] <= button_y + button_height:
                GameLogic.restart_game()
            else:
                x, y = event.pos[0] // cell_width, event.pos[1] // cell_height
                game_state[x, y] = not game_state[x, y]

    # Tick and update
    clock.tick()  # No argument needed for tick when using time per frame
    screen.fill(white)
    GameUI.draw_grid()
    GameLogic.draw_cells()
    GameUI.draw_button()
    GameUI.draw_restart_button()
    pygame.display.flip()

    # Perform simulation step if not paused
    if not paused:
        GameLogic.next_generation()

    # Introduce delay for time per frame
    pygame.time.delay(int(time_per_frame * 1000))  # Delay in milliseconds

pygame.quit()


# Changes: new button for resart in case you get stuck in game
# Keyboard interaction: 'P' for pause, 'S' for save, 'L' for load
# You can set timer for every new generation in time_per_frame - support value in seconds
# Communication between functions works on DI (Dependency Injection), code is written with DRY rules 

# Design patterns provided in this code
# Observer Pattern:
# The code has a basic event handling mechanism where the program reacts to various events such as key presses, mouse clicks, and window closure. 

# Separation of Concerns:
# The code separates concerns into different classes for UI (GameUI) and game logic (GameLogic). This helps in organizing the code and makes it more modular.

# MVC (Model-View-Controller) Pattern:
# The code has elements that resemble the MVC pattern. The GameUI class is responsible for rendering the view (drawing buttons and grid), and the GameLogic class is responsible for the game's logic.

# Command Pattern:
# The code handles different user inputs (e.g., key presses, mouse clicks) with conditional statements, which is a basic form of the command pattern. Each command is associated with a specific action.

# Encapsulation and Abstraction:
# The code makes use of classes and methods to encapsulate functionality, providing a level of abstraction. For example, the GameUI and GameLogic classes encapsulate the UI rendering and game logic, respectively.
