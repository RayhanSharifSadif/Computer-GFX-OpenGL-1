from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# initial variable and boolean
window_width = 600
window_height = 600
is_pause_check = 0
init_circle_list = []
original_circle = []
growth_speed = 0.75

# midpoint circle algorithm
def MidPointCircle(cx, cy, radius):
    d = (1 - radius)
    x = 0
    y = radius

    CirclePoints(x, y, cx, cy)

    while x < y:
        if d < 0:
            d = d + 2 * x + 3
            x = x + 1
        else:
            d = d + 2 * x - 2 * y + 5
            x = x + 1
            y = y - 1

        CirclePoints(x, y, cx, cy)

# circle at x,y coordinate and cx,cy center
def CirclePoints(x, y, cx, cy):
    glVertex2f(x + cx, y + cy)
    glVertex2f(y + cx, x + cy)
    glVertex2f(y + cx, -x + cy)
    glVertex2f(x + cx, -y + cy)
    glVertex2f(-x + cx, -y + cy)
    glVertex2f(-y + cx, -x + cy)
    glVertex2f(-y + cx, x + cy)
    glVertex2f(-x + cx, y + cy)

# circle generation and deletion
def list_mem():
    global init_circle_list

    original_circle = []
    for itr in init_circle_list:
        if itr['radius'] < window_width + 100:
            original_circle.append(itr)
    init_circle_list = original_circle

    print("Circles Dict ->", init_circle_list)

# increasing the radius
def animate():
    global growth_speed

    if is_pause_check:
        pass
    else:
        for itr in init_circle_list:
            itr['radius'] += growth_speed

        list_mem()
    glutPostRedisplay()

# creating the point (pixel)
def point_create():
    glColor3f(0.447, 1.0, 0.973)
    glPointSize(2)
    glBegin(GL_POINTS)

    for itr in init_circle_list:
        MidPointCircle(itr['x'], itr['y'], itr['radius'])
    glEnd()

# finally display and others
def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # calling the point create function
    point_create()
    glutSwapBuffers()

# mouse and keyboard function
def mouseListener(button, state, x, y):
    global init_circle_list

    if is_pause_check:
        pass
    else:
        if button == GLUT_RIGHT_BUTTON:
            if state == GLUT_DOWN and not is_pause_check:
                init_circle_list.append({'x': x, 'y': window_height - y, 'radius': 20})

def KeyboardListener(key, x, y):
    global is_pause_check
    global growth_speed

    if key == b" ":
        is_pause_check = not is_pause_check
    elif key == GLUT_KEY_LEFT:
        growth_speed += 0.1  # Increase growth speed
    elif key == GLUT_KEY_RIGHT:
        growth_speed -= 0.1  # Decrease growth speed

def iterate():
    glViewport(0, 0, window_width, window_height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, window_width, 0.0, window_height, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

glutInit()
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
glutInitWindowSize(window_width, window_height)
glutInitWindowPosition(0, 0)
wind = glutCreateWindow(b"Water Ripple")
iterate()

glutIdleFunc(animate)
glutDisplayFunc(display)
glutMouseFunc(mouseListener)
glutKeyboardFunc(KeyboardListener)
glutSpecialFunc(KeyboardListener)  # Register the special function for arrow keys

glutMainLoop()
