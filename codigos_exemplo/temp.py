import glfw
from OpenGL.GL import *
import numpy as np


class LineDrawer:
    def __init__(self):
        self.points = []  # Armazena os pontos clicados
        self.lines = []  # Armazena as linhas desenhadas [(p1, p2), ...]
        self.current_line = None  # Linha que está sendo desenhada atualmente
        self.window = None

    def init_glfw(self):
        # Inicializa o GLFW
        if not glfw.init():
            return False

        # Configurações da janela
        glfw.window_hint(glfw.RESIZABLE, glfw.FALSE)
        self.window = glfw.create_window(800, 600, "Desenhar Linhas", None, None)

        if not self.window:
            glfw.terminate()
            return False

        glfw.make_context_current(self.window)

        # Configura callbacks
        glfw.set_mouse_button_callback(self.window, self.mouse_button_callback)

        # Configuração inicial do OpenGL
        glClearColor(0.2, 0.2, 0.2, 1.0)  # Fundo cinza escuro
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, 800, 600, 0, -1, 1)  # Sistema de coordenadas com origem no topo esquerdo
        glMatrixMode(GL_MODELVIEW)

        return True

    def mouse_button_callback(self, window, button, action, mods):
        if button == glfw.MOUSE_BUTTON_LEFT and action == glfw.PRESS:
            # Obtém posição do mouse
            x, y = glfw.get_cursor_pos(window)

            # Adiciona ponto à lista
            self.points.append((x, y))
            print(f"Ponto {len(self.points)} clicado: ({x:.0f}, {y:.0f})")

            # Se temos 2 pontos, cria a linha
            if len(self.points) == 2:
                # Adiciona a linha à lista de linhas
                self.lines.append((self.points[0], self.points[1]))
                print(
                    f"Linha desenhada entre ({self.points[0][0]:.0f}, {self.points[0][1]:.0f}) e ({self.points[1][0]:.0f}, {self.points[1][1]:.0f})")
                # Limpa os pontos temporários
                self.points = []

    def draw_line(self, p1, p2, color=(1.0, 1.0, 1.0), width=3.0):
        """Desenha uma linha entre dois pontos"""
        glColor3f(*color)
        glLineWidth(width)
        glBegin(GL_LINES)
        glVertex2f(p1[0], p1[1])
        glVertex2f(p2[0], p2[1])
        glEnd()

    def draw_points(self):
        """Desenha pontos nos locais clicados temporariamente"""
        for point in self.points:
            glColor3f(1.0, 0.0, 0.0)  # Pontos vermelhos
            glPointSize(8.0)
            glBegin(GL_POINTS)
            glVertex2f(point[0], point[1])
            glEnd()

    def draw_all_lines(self):
        """Desenha todas as linhas salvas"""
        for line in self.lines:
            self.draw_line(line[0], line[1])

    def run(self):
        if not self.init_glfw():
            print("Falha ao inicializar GLFW")
            return

        print("Clique em dois pontos para desenhar uma linha entre eles")
        print("Pressione ESC para sair")

        while not glfw.window_should_close(self.window):
            # Limpa a tela a cada frame
            glClear(GL_COLOR_BUFFER_BIT)

            # Desenha todas as linhas já criadas (persistentes)
            self.draw_all_lines()

            # Desenha os pontos temporários (enquanto aguarda o segundo clique)
            self.draw_points()

            # Se tiver 2 pontos temporários, desenha uma linha temporária (opcional)
            if len(self.points) == 2:
                # Linha temporária em amarelo enquanto mostra o preview
                self.draw_line(self.points[0], self.points[1], (1.0, 1.0, 0.0), 2.0)

            glfw.swap_buffers(self.window)
            glfw.poll_events()

            # Verifica tecla ESC para sair
            if glfw.get_key(self.window, glfw.KEY_ESCAPE) == glfw.PRESS:
                glfw.set_window_should_close(self.window, True)

        glfw.terminate()



if __name__ == "__main__":
    app = LineDrawer()
    app.run()