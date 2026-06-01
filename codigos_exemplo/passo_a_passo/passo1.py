import glfw             #biblioteca para gerencia de janelas 
                        #e acesso ao contexto gráfico
from OpenGL.GL import * #biblioteca para acessa todo o openGL
import numpy as np      #biblioteca para gerencia de arrays

#constantes globais
largura, altura = 800, 600

def main():
    #inicializa a biblioteca glfw
    glfw.init()

    #cria uma janela e retorna uma referencia para ela
    win = glfw.create_window( largura, altura, "1 - criacao da janela"
                             , None, None )
    #define a parte útil da janela como o contexto gráfico corrente
    glfw.make_context_current( win )

    

    #loop principal
    while not glfw.window_should_close( win ):
        #processa eventos de entrada (mouse, teclado, etc...)
        glfw.poll_events()

        #troca entre buffer de desenho/exibição
        glfw.swap_buffers( win )

if __name__ == "__main__":
    main()
