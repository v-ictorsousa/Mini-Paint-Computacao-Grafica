import glfw
from OpenGL.GL import *
import numpy as np

class LineDrawer:
    def __init__(self):
        self.points = []  # Armazena os pontos clicados
        self.lines = []  # Armazena as linhas desenhadas [(p1, p2), ...]
        self.current_line = None
        self.window = None

    def init_glfw(self):
        if not glfw.init():
            return False

        glfw.window_hint(glfw.RESIZABLE, glfw.FALSE)
        self.window = glfw.create_window(800, 600, "Desenhar Linhas - Bresenham", None, None)

        if not self.window:
            glfw.terminate()
            return False

        glfw.make_context_current(self.window)
        glfw.set_mouse_button_callback(self.window, self.mouse_button_callback)

        glClearColor(0.2, 0.2, 0.2, 1.0)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, 800, 600, 0, -1, 1)
        glMatrixMode(GL_MODELVIEW)

        return True

    def bresenham_line(self, x0, y0, x1, y1):
        """
        Implementação do algoritmo de Bresenham para desenhar linhas.
        Retorna uma lista de pontos (x, y) que formam a linha.
        """
        points = []

        # Converte para inteiros
        x0, y0, x1, y1 = int(x0), int(y0), int(x1), int(y1)

        dx = abs(x1 - x0)
        dy = abs(y1 - y0)

        # Determina direção do incremento
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1

        # Caso 1: inclinação < 1 (linha mais horizontal)
        if dx > dy:
            err = dx / 2.0
            x, y = x0, y0
            while x != x1:
                points.append((x, y))
                err -= dy
                if err < 0:
                    y += sy
                    err += dx
                x += sx
        # Caso 2: inclinação >= 1 (linha mais vertical)
        else:
            err = dy / 2.0
            x, y = x0, y0
            while y != y1:
                points.append((x, y))
                err -= dx
                if err < 0:
                    x += sx
                    err += dy
                y += sy

        # Adiciona o último ponto
        points.append((x1, y1))

        return points

    def bresenham_line_integer(self, x0, y0, x1, y1):
        """
        Versão otimizada do algoritmo de Bresenham usando apenas inteiros.
        """
        points = []

        x0, y0, x1, y1 = int(x0), int(y0), int(x1), int(y1)

        dx = abs(x1 - x0)
        dy = abs(y1 - y0)

        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1

        err = dx - dy

        x, y = x0, y0

        while True:
            points.append((x, y))

            if x == x1 and y == y1:
                break

            e2 = 2 * err

            if e2 > -dy:
                err -= dy
                x += sx

            if e2 < dx:
                err += dx
                y += sy

        return points

    def draw_bresenham_line(self, p1, p2, color=(1.0, 1.0, 1.0), point_size=1.0):
        """
        Desenha uma linha usando o algoritmo de Bresenham e glBegin(GL_POINTS)
        """
        glColor3f(*color)
        glPointSize(point_size)
        glBegin(GL_POINTS)

        # Usa a versão inteira (mais eficiente)
        points = self.bresenham_line_integer(p1[0], p1[1], p2[0], p2[1])

        for point in points:
            glVertex2f(point[0], point[1])

        glEnd()
        return len(points)  # Retorna o número de pontos desenhados

    def mouse_button_callback(self, window, button, action, mods):
        if button == glfw.MOUSE_BUTTON_LEFT and action == glfw.PRESS:
            x, y = glfw.get_cursor_pos(window)
            self.points.append((x, y))
            print(f"Ponto {len(self.points)} clicado: ({x:.0f}, {y:.0f})")

            if len(self.points) == 2:
                self.lines.append((self.points[0], self.points[1]))
                print(
                    f"Linha desenhada com Bresenham entre ({self.points[0][0]:.0f}, {self.points[0][1]:.0f}) e ({self.points[1][0]:.0f}, {self.points[1][1]:.0f})")
                self.points = []

    def draw_pixel(self, x, y, color=(1.0, 1.0, 1.0)):
        """Desenha um único pixel na posição (x, y)"""
        glColor3f(*color)
        glBegin(GL_POINTS)
        glVertex2f(x, y)
        glEnd()

    def draw_points(self):
        """Desenha pontos nos locais clicados temporariamente"""
        for point in self.points:
            glColor3f(1.0, 0.0, 0.0)
            glPointSize(8.0)
            glBegin(GL_POINTS)
            glVertex2f(point[0], point[1])
            glEnd()

    def draw_all_lines(self):
        """Desenha todas as linhas salvas usando Bresenham"""
        for line in self.lines:
            self.draw_bresenham_line(line[0], line[1], (0.0, 1.0, 0.0), 2.0)

    def run(self):
        if not self.init_glfw():
            print("Falha ao inicializar GLFW")
            return

        print("=== DESENHADOR DE LINHAS - ALGORITMO DE BRESENHAM ===")
        print("Clique em dois pontos para desenhar uma linha")
        print("Pressione ESC para sair")
        print("Pressione C para limpar todas as linhas")
        print("===================================================")

        # Configura tecla C para limpar
        def key_callback(window, key, scancode, action, mods):
            if action == glfw.PRESS:
                if key == glfw.KEY_C:
                    self.lines = []
                    self.points = []
                    print("Todas as linhas foram limpas!")
                elif key == glfw.KEY_ESCAPE:
                    glfw.set_window_should_close(window, True)

        glfw.set_key_callback(self.window, key_callback)

        while not glfw.window_should_close(self.window):
            glClear(GL_COLOR_BUFFER_BIT)

            # Desenha todas as linhas salvas
            self.draw_all_lines()

            # Desenha pontos temporários
            self.draw_points()

            # Preview da linha usando Bresenham enquanto espera o segundo clique
            if len(self.points) == 1:
                # Obtém posição atual do mouse para preview
                x, y = glfw.get_cursor_pos(self.window)
                self.draw_bresenham_line(self.points[0], (x, y), (1.0, 1.0, 0.0), 1.0)

            glfw.swap_buffers(self.window)
            glfw.poll_events()

        glfw.terminate()


class BresenhamDemo:
    """Uma classe de demonstração que mostra o funcionamento interno do algoritmo"""

    @staticmethod
    def visualize_bresenham():
        """Função para visualizar os passos do algoritmo de Bresenham"""
        print("\n=== DEMONSTRAÇÃO DO ALGORITMO DE BRESENHAM ===")

        # Exemplo 1: Linha com inclinação < 1
        print("\nExemplo 1: Linha de (2, 2) a (10, 5)")
        points1 = BresenhamDemo.bresenham_step_by_step(2, 2, 10, 5)
        print(f"Pontos gerados: {points1}")

        # Exemplo 2: Linha com inclinação > 1
        print("\nExemplo 2: Linha de (2, 2) a (5, 10)")
        points2 = BresenhamDemo.bresenham_step_by_step(2, 2, 5, 10)
        print(f"Pontos gerados: {points2}")

        # Exemplo 3: Linha reta horizontal
        print("\nExemplo 3: Linha horizontal de (2, 5) a (15, 5)")
        points3 = BresenhamDemo.bresenham_step_by_step(2, 5, 15, 5)
        print(f"Pontos gerados: {points3}")

        # Exemplo 4: Linha reta vertical
        print("\nExemplo 4: Linha vertical de (10, 2) a (10, 12)")
        points4 = BresenhamDemo.bresenham_step_by_step(10, 2, 10, 12)
        print(f"Pontos gerados: {points4}")

    @staticmethod
    def bresenham_step_by_step(x0, y0, x1, y1):
        """Versão passo a passo que mostra o processo de decisão"""
        points = []

        x0, y0, x1, y1 = int(x0), int(y0), int(x1), int(y1)

        dx = abs(x1 - x0)
        dy = abs(y1 - y0)

        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1

        err = dx - dy

        x, y = x0, y0

        print(f"Início: ({x}, {y})")
        print(f"dx = {dx}, dy = {dy}")
        print(f"direção x = {sx}, direção y = {sy}")
        print(f"Erro inicial = {err}")
        print("-" * 40)

        step = 0
        while True:
            points.append((x, y))
            print(f"Passo {step}: pixel ({x}, {y})")

            if x == x1 and y == y1:
                break

            e2 = 2 * err
            print(f"  e2 = 2*err = {e2}")

            if e2 > -dy:
                print(f"  e2 > -dy ({e2} > {-dy}) -> movendo x")
                err -= dy
                x += sx
                print(f"    novo err = {err}")

            if e2 < dx:
                print(f"  e2 < dx ({e2} < {dx}) -> movendo y")
                err += dx
                y += sy
                print(f"    novo err = {err}")

            step += 1

        return points


if __name__ == "__main__":
    import sys

    # Executa a demonstração primeiro
    BresenhamDemo.visualize_bresenham()

    print("\n" + "=" * 50)
    resposta = input("Executar programa gráfico? (s/n): ")

    if resposta.lower() == 's':
        app = LineDrawer()
        app.run()
    else:
        print("Encerrando...")