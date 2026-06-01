
import glfw
from OpenGL.GL import *
import numpy as np

if not glfw.init():
    raise Exception("Falha ao iniciar")

width, height = 800, 600

window = glfw.create_window(width, height, "Minimo", None, None)
if not window:
    raise Exception("Falha ao criar a janela")

glfw.make_context_current(window)

while not glfw.window_should_close(window):
    glfw.poll_events()

glfw.terminate()