import glfw
from OpenGL.GL import *
import numpy

#funcao principal
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

def dda_line( x0, y0, x1, y1):
        """
        Implementação do algoritmo DDA (Digital Differential Analyzer)
        para desenhar linhas.
        Retorna uma lista de pontos (x, y) que formam a linha.
        """
        points = []

        # Calcula diferenças
        dx = x1 - x0
        dy = y1 - y0

        # Calcula o número de passos necessário
        # O passo será o maior valor absoluto entre dx e dy
        steps = abs(dx) if abs(dx) > abs(dy) else abs(dy)

        # Se a linha é um ponto único
        if steps == 0:
            return [(int(x0), int(y0))]

        # Calcula incrementos
        x_increment = dx / steps
        y_increment = dy / steps

        # Ponto inicial
        x = x0
        y = y0

        # Gera os pontos
        for i in range(int(steps) + 1):
            points.append((int(round(x)), int(round(y))))
            x += x_increment
            y += y_increment

        return points



if __name__ == "__main__":
    main()