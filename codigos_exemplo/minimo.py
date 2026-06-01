import glfw
from OpenGL.GL import *
import numpy as np

vertices  = [[-0.5,-0.5],
             [0.5,-0.5],
             [0.0, 0.5]]
cores = [[1,0,0], [0,1,0], [0,0,1]]
def init():
    glClearColor(1,1,1,1)

def render():

    #glColor3f(1,0,0)
    #glBegin(GL_TRIANGLES)
    #glVertex2f(-0.5,-0.5)
    #glColor3f(0,1,0)
    #glVertex2f(0.5,-0.5)
    #glColor3f(0, 0, 1)
    #glVertex2f(0.0,0.5)
    #glEnd()

    glPointSize(6)
    glBegin(GL_POINTS)
    for v, c in vertices:
        glVertex2fv(v)
    glEnd()

    glLineWidth(3)
    glColor3f(0,0,0)
    #glBegin(GL_LINE)
    #glBegin(GL_LINE_STRIP)
    glBegin(GL_LINE_LOOP)
    for v in vertices:
        glVertex2fv(v)
    glEnd()

    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    glColor3f(0.3,0.5,0.7)
    glBegin(GL_TRIANGLES)
    for v in vertices:
        glVertex2fv(v)
    

def main():
    glfw.init()
    window = glfw.create_window(500,500,'Minimo', None, None)
    glfw.make_context_current(window)
    init()
    while not glfw.window_should_close(window):
        glfw.poll_events()
        render()
        glfw.swap_buffers(window)

if __name__ == "__main__":
    main()
    glfw.terminate()
