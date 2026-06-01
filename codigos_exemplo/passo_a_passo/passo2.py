import glfw             #biblioteca para gerencia de janelas 
                        #e acesso ao contexto gráfico
from OpenGL.GL import * #biblioteca para acessa todo o openGL
import numpy as np      #biblioteca para gerencia de arrays

#constantes globais
largura, altura = 800, 600

def main():
    #inicializa a biblioteca glfw
    glfw.init()

    monitor = glfw.get_primary_monitor()

    glfw.window_hint(glfw.RESIZABLE, glfw.TRUE)
    #cria uma janela e retorna uma referencia para ela
    win1 = glfw.create_window( largura, altura, "2 - Janela 1"
                             , monitor, None )
    
    #win2 = glfw.create_window( largura, altura, "2 - Janela 2"
    #                         , None, None )
    
    
    #define a parte útil da janela como o contexto gráfico corrente
    glfw.make_context_current( win1 )

    

    #loop principal
    while not glfw.window_should_close( win1 ):
        #processa eventos de entrada (mouse, teclado, etc...)
        glfw.poll_events()

        #troca entre buffer de desenho/exibição
        glfw.swap_buffers( win1 )

if __name__ == "__main__":
    main()
