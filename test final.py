from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import random
import sys

# Initialize screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 480, 720
catcher_x = SCREEN_WIDTH // 2
catcher_y = 50
diamond_x = random.randint(50, SCREEN_WIDTH - 50)
diamond_y = SCREEN_HEIGHT - 50
diamond_speed = 2
score = 0
game_over = False
is_paused = False


# Function to draw a line using the Midpoint Line Algorithm
def draw_line(x1, y1, x2, y2, color):
    glColor3f(*color)
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    steep = abs(dy) > abs(dx)

    if steep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2
        dx, dy = dy, dx

    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1

    d = 2 * dy - dx
    y = y1

    for x in range(int(x1), int(x2) + 1):
        if steep:
            glBegin(GL_POINTS)
            glVertex2f(int(y), int(x))
            glEnd()
        else:
            glBegin(GL_POINTS)
            glVertex2f(int(x), int(y))
            glEnd()

        if d > 0:
            y += 1 if y1 < y2 else -1
            d -= 2 * dx
        d += 2 * dy


# Diamond
diamond_color = None


def draw_diamond(x, y):
    global diamond_color

    # Check if the diamond color has been generated
    if not diamond_color:
        diamond_color = [random.random(), random.random(), random.random()]  # Random color

    draw_line(x, y + 20, x - 15, y, diamond_color)
    draw_line(x, y + 20, x + 15, y, diamond_color)
    draw_line(x - 15, y, x, y - 20, diamond_color)
    draw_line(x + 15, y, x, y - 20, diamond_color)


# Function to draw the Catcher
def draw_catcher(x, y):
    global game_over
    color = [0.5, 0, 0.5]  # purple color

    if game_over:
        color = [1, 0, 0]  # Change to red

    x, y = catcher_x, catcher_y
    draw_line(x - 70, y, x + 70, y, color)
    draw_line(x - 70, y, x - 60, y - 20, color)
    draw_line(x + 70, y, x + 60, y - 20, color)
    draw_line(x - 60, y - 20, x + 60, y - 20, color)


# Display function
def display():
    glClear(GL_COLOR_BUFFER_BIT)
    draw_restart_button()
    draw_pause_button()
    draw_exit_button()
    draw_diamond(diamond_x, diamond_y)
    draw_catcher(catcher_x, catcher_y)
    glutSwapBuffers()


# Update function
def update(value):
    global diamond_x, diamond_y, score, diamond_speed, game_over, diamond_color

    if not is_paused and not game_over:
        diamond_y -= diamond_speed
        if diamond_y < 0:
            game_over = True
            print("Game Over. Final Score:", score)

        # Check for collision with catcher
        if catcher_x - 70 <= diamond_x <= catcher_x + 70 and catcher_y <= diamond_y <= catcher_y + 20:
            score += 1
            print("Score:", score)
            diamond_x = random.randint(50, SCREEN_WIDTH - 50)
            diamond_y = SCREEN_HEIGHT - 50
            diamond_speed += 0.1  # Increase speed of falling diamond
            diamond_color = None
    glutPostRedisplay()
    glutTimerFunc(16, update, 0)


# Function to draw the Restart Button
def draw_restart_button():
    draw_line(10, SCREEN_HEIGHT - 30, 60, SCREEN_HEIGHT - 30, [0, 1, 1])
    draw_line(10, SCREEN_HEIGHT - 30, 20, SCREEN_HEIGHT - 20, [0, 1, 1])
    draw_line(10, SCREEN_HEIGHT - 30, 20, SCREEN_HEIGHT - 40, [0, 1, 1])


# Function to draw the Pause Button
def draw_pause_button():
    if is_paused:
        # Draw Play button when paused
        draw_line(SCREEN_WIDTH // 2 - 5, SCREEN_HEIGHT - 20, SCREEN_WIDTH // 2 - 5, SCREEN_HEIGHT - 40, [1, 0.76, 0])
        draw_line(SCREEN_WIDTH // 2 + 5, SCREEN_HEIGHT - 20, SCREEN_WIDTH // 2 + 5, SCREEN_HEIGHT - 40, [1, 0.76, 0])
    else:
        # Draw Pause button when not paused
        draw_line(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 20, SCREEN_WIDTH // 2 + 10, SCREEN_HEIGHT - 40, [1, 0.76, 0])
        draw_line(SCREEN_WIDTH // 2 + 10, SCREEN_HEIGHT - 40, SCREEN_WIDTH // 2 + 20, SCREEN_HEIGHT - 20, [1, 0.76, 0])


# Function to draw the Exit Button
def draw_exit_button():
    draw_line(SCREEN_WIDTH - 30, SCREEN_HEIGHT - 20, SCREEN_WIDTH - 10, SCREEN_HEIGHT - 40, [1, 0, 0])
    draw_line(SCREEN_WIDTH - 30, SCREEN_HEIGHT - 40, SCREEN_WIDTH - 10, SCREEN_HEIGHT - 20, [1, 0, 0])


# Mouse click function
def mouse_click(button, state, x, y):
    global game_over, score, diamond_speed, diamond_x, diamond_y, is_paused, catcher_x, catcher_y   # Use global variables
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        y = SCREEN_HEIGHT - y

        if (SCREEN_WIDTH - 50 <= x <= SCREEN_WIDTH - 10) and (SCREEN_HEIGHT - 50 <= y <= SCREEN_HEIGHT - 10):
            print(f"Goodbye. Final Score: {score}")
            glutLeaveMainLoop()

        elif (SCREEN_WIDTH // 2 - 20 <= x <= SCREEN_WIDTH // 2 + 20) and (SCREEN_HEIGHT - 50 <= y <= SCREEN_HEIGHT - 10):
            is_paused = not is_paused
            glutPostRedisplay() 

        elif (10 <= x <= 60) and (SCREEN_HEIGHT - 50 <= y <= SCREEN_HEIGHT - 10):
            print("Starting Over")
            catcher_x = SCREEN_WIDTH // 2
            catcher_y = 50
            diamond_x = random.randint(50, SCREEN_WIDTH - 50)
            diamond_y = SCREEN_HEIGHT - 50
            diamond_speed = 2
            score = 0
            game_over = False
            is_paused = False


# Special keys function
def special_keys(key, x, y):
    global catcher_x
    if not is_paused:
        step = 10
        if key == GLUT_KEY_RIGHT:
            catcher_x = min(catcher_x + step, SCREEN_WIDTH - 30)
        elif key == GLUT_KEY_LEFT:
            catcher_x = max(catcher_x - step, 30)


# OpenGL initialization
glutInit()
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE)
glutInitWindowSize(SCREEN_WIDTH, SCREEN_HEIGHT)
glutCreateWindow(b"Catch the Diamonds!")
glOrtho(0, SCREEN_WIDTH, 0, SCREEN_HEIGHT, -1, 1)
glClearColor(0, 0, 0, 1)

# Set callback functions
glutDisplayFunc(display)
glutSpecialFunc(special_keys)
glutMouseFunc(mouse_click)
glutIdleFunc(display)
glutTimerFunc(16, update, 0)

# Start the main loop
glutMainLoop()
