import glfw             #biblioteca para gerencia de janelas 
                        #e acesso ao contexto gráfico
from OpenGL.GL import * #biblioteca para acessa todo o openGL
import numpy as np      #biblioteca para gerencia de arrays

#constantes globais
largura, altura = 800, 600
win = None
points = [[100,100],
          [200,100],
          [150,50]  
          ]

def render():
    #funcao basica do opengl q indica que desejamos limpar o buffer de cor
    glClear(GL_COLOR_BUFFER_BIT) #o _BIT indica q pode ser combinado com outros flags

    glColor(1,0,0)
    glPointSize( 1 )

    glBegin(GL_POINTS)
    for p in points:
        glVertex2f(p[0], p[1])    
    glEnd()

def init():
    global win

    #inicializa a biblioteca glfw
    glfw.init()

    #cria uma janela e retorna uma referencia para ela
    win = glfw.create_window( largura, altura, "1 - criacao da janela"
                             , None, None )
    #define a parte útil da janela como o contexto gráfico corrente
    glfw.make_context_current( win )

    #inicializacao OPENGL
    glClearColor(1,1,1,1)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, 800, 600, 0, -1, 1)
    glMatrixMode(GL_MODELVIEW)

def main():
    
    init()

    #loop principal
    while not glfw.window_should_close( win ):
        #processa eventos de entrada (mouse, teclado, etc...)
        glfw.poll_events()

        #desenha o framebuffer
        render()

        #troca entre buffer de desenho/exibição
        glfw.swap_buffers( win )

if __name__ == "__main__":
    main()
    glfw.terminate()
