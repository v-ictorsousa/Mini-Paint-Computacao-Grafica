import glfw
from OpenGL.GL import *
import numpy as np
import math


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
        self.window = glfw.create_window(800, 600, "Desenhar Linhas - Algoritmo DDA", None, None)

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

    def dda_line(self, x0, y0, x1, y1):
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

    def dda_line_optimized(self, x0, y0, x1, y1):
        """
        Versão otimizada do algoritmo DDA com tratamento especial
        para linhas horizontais e verticais.
        """
        points = []

        dx = x1 - x0
        dy = y1 - y0

        # Tratamento especial para linhas horizontais (mais eficiente)
        if dy == 0:
            step_x = 1 if dx > 0 else -1
            for x in range(int(x0), int(x1) + step_x, step_x):
                points.append((x, int(y0)))
            return points

        # Tratamento especial para linhas verticais (mais eficiente)
        if dx == 0:
            step_y = 1 if dy > 0 else -1
            for y in range(int(y0), int(y1) + step_y, step_y):
                points.append((int(x0), y))
            return points

        # Caso geral
        steps = max(abs(dx), abs(dy))
        x_increment = dx / steps
        y_increment = dy / steps

        x, y = x0, y0

        for i in range(int(steps) + 1):
            points.append((int(round(x)), int(round(y))))
            x += x_increment
            y += y_increment

        return points

    def draw_dda_line(self, p1, p2, color=(1.0, 1.0, 1.0), point_size=1.0):
        """
        Desenha uma linha usando o algoritmo DDA e glBegin(GL_POINTS)
        """
        glColor3f(*color)
        glPointSize(point_size)
        glBegin(GL_POINTS)

        # Usa a versão otimizada
        points = self.dda_line_optimized(p1[0], p1[1], p2[0], p2[1])

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
                # Calcula quantos pontos a linha terá
                points_count = len(self.dda_line_optimized(self.points[0][0], self.points[0][1],
                                                           self.points[1][0], self.points[1][1]))
                print(
                    f"Linha desenhada com DDA entre ({self.points[0][0]:.0f}, {self.points[0][1]:.0f}) e ({self.points[1][0]:.0f}, {self.points[1][1]:.0f})")
                print(f"  {points_count} pontos gerados")
                self.points = []

    def draw_points(self):
        """Desenha pontos nos locais clicados temporariamente"""
        for point in self.points:
            glColor3f(1.0, 0.0, 0.0)
            glPointSize(8.0)
            glBegin(GL_POINTS)
            glVertex2f(point[0], point[1])
            glEnd()

    def draw_all_lines(self):
        """Desenha todas as linhas salvas usando DDA"""
        for line in self.lines:
            # Cores diferentes para cada linha
            colors = [(0.0, 1.0, 0.0), (1.0, 0.0, 0.0), (0.0, 0.0, 1.0),
                      (1.0, 1.0, 0.0), (1.0, 0.0, 1.0), (0.0, 1.0, 1.0)]
            color_index = len(self.lines) % len(colors) if len(self.lines) > 0 else 0
            self.draw_dda_line(line[0], line[1], colors[color_index], 2.0)

    def run(self):
        if not self.init_glfw():
            print("Falha ao inicializar GLFW")
            return

        print("=== DESENHADOR DE LINHAS - ALGORITMO DDA ===")
        print("Clique em dois pontos para desenhar uma linha")
        print("Pressione ESC para sair")
        print("Pressione C para limpar todas as linhas")
        print("Pressione S para mostrar estatísticas")
        print("===========================================")

        # Configura callbacks de teclado
        def key_callback(window, key, scancode, action, mods):
            if action == glfw.PRESS:
                if key == glfw.KEY_C:
                    self.lines = []
                    self.points = []
                    print("Todas as linhas foram limpas!")
                elif key == glfw.KEY_S:
                    self.show_statistics()
                elif key == glfw.KEY_ESCAPE:
                    glfw.set_window_should_close(window, True)

        glfw.set_key_callback(self.window, key_callback)

        while not glfw.window_should_close(self.window):
            glClear(GL_COLOR_BUFFER_BIT)

            # Desenha todas as linhas salvas
            self.draw_all_lines()

            # Desenha pontos temporários
            self.draw_points()

            # Preview da linha usando DDA enquanto espera o segundo clique
            if len(self.points) == 1:
                # Obtém posição atual do mouse para preview
                x, y = glfw.get_cursor_pos(self.window)
                self.draw_dda_line(self.points[0], (x, y), (1.0, 1.0, 0.0), 1.0)

            glfw.swap_buffers(self.window)
            glfw.poll_events()

        glfw.terminate()

    def show_statistics(self):
        """Mostra estatísticas sobre as linhas desenhadas"""
        if not self.lines:
            print("\nNenhuma linha desenhada ainda!")
            return

        print("\n=== ESTATÍSTICAS DAS LINHAS ===")
        total_points = 0

        for i, (p1, p2) in enumerate(self.lines, 1):
            points = self.dda_line_optimized(p1[0], p1[1], p2[0], p2[1])
            distance = math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)
            total_points += len(points)
            print(f"Linha {i}:")
            print(f"  De ({p1[0]:.0f}, {p1[1]:.0f}) para ({p2[0]:.0f}, {p2[1]:.0f})")
            print(f"  Distância: {distance:.2f} pixels")
            print(f"  Pontos gerados: {len(points)}")

        print(f"\nTotal de linhas: {len(self.lines)}")
        print(f"Total de pontos desenhados: {total_points}")
        print("=============================\n")


class DDADemo:
    """Uma classe de demonstração que mostra o funcionamento do algoritmo DDA"""

    @staticmethod
    def visualize_dda():
        """Função para visualizar os passos do algoritmo DDA"""
        print("\n=== DEMONSTRAÇÃO DO ALGORITMO DDA ===")

        # Exemplo 1: Linha com inclinação < 1
        print("\nExemplo 1: Linha de (2, 2) a (10, 5)")
        points1 = DDADemo.dda_step_by_step(2, 2, 10, 5)
        print(f"Pontos gerados: {points1}")

        # Exemplo 2: Linha com inclinação > 1
        print("\nExemplo 2: Linha de (2, 2) a (5, 10)")
        points2 = DDADemo.dda_step_by_step(2, 2, 5, 10)
        print(f"Pontos gerados: {points2}")

        # Exemplo 3: Linha reta horizontal
        print("\nExemplo 3: Linha horizontal de (2, 5) a (15, 5)")
        points3 = DDADemo.dda_step_by_step(2, 5, 15, 5)
        print(f"Pontos gerados: {points3}")

        # Exemplo 4: Linha reta vertical
        print("\nExemplo 4: Linha vertical de (10, 2) a (10, 12)")
        points4 = DDADemo.dda_step_by_step(10, 2, 10, 12)
        print(f"Pontos gerados: {points4}")

    @staticmethod
    def dda_step_by_step(x0, y0, x1, y1):
        """Versão passo a passo que mostra o processo do algoritmo DDA"""
        points = []

        print(f"Ponto inicial: ({x0}, {y0})")
        print(f"Ponto final: ({x1}, {y1})")

        dx = x1 - x0
        dy = y1 - y0

        print(f"dx = {dx}, dy = {dy}")

        # Calcula o número de passos
        steps = max(abs(dx), abs(dy))
        print(f"Número de passos: {steps}")

        if steps == 0:
            return [(int(x0), int(y0))]

        # Calcula incrementos
        x_increment = dx / steps
        y_increment = dy / steps

        print(f"Incremento em x: {x_increment:.4f}")
        print(f"Incremento em y: {y_increment:.4f}")
        print("-" * 50)

        x = x0
        y = y0

        for i in range(int(steps) + 1):
            rounded_x = int(round(x))
            rounded_y = int(round(y))
            points.append((rounded_x, rounded_y))
            print(f"Passo {i}: x={x:.4f}, y={y:.4f} -> pixel ({rounded_x}, {rounded_y})")
            x += x_increment
            y += y_increment

        return points

    @staticmethod
    def compare_algorithms():
        """Compara DDA com Bresenham para diferentes tipos de linha"""
        print("\n=== COMPARAÇÃO DDA vs BRESENHAM ===")

        test_cases = [
            ((2, 2), (10, 5), "Inclinação moderada"),
            ((2, 2), (5, 10), "Inclinação íngreme"),
            ((2, 5), (15, 5), "Linha horizontal"),
            ((10, 2), (10, 12), "Linha vertical"),
            ((1, 1), (20, 20), "Diagonal 45°"),
        ]

        for (p1, p2, desc) in test_cases:
            print(f"\n{desc}: {p1} -> {p2}")

            # DDA
            dda_points = DDADemo.dda_line_compare(p1[0], p1[1], p2[0], p2[1])

            # Bresenham (implementação simples para comparação)
            bresenham_points = DDADemo.bresenham_line_compare(p1[0], p1[1], p2[0], p2[1])

            print(f"  DDA: {len(dda_points)} pontos")
            print(f"  Bresenham: {len(bresenham_points)} pontos")
            print(f"  Diferença: {abs(len(dda_points) - len(bresenham_points))} pontos")

    @staticmethod
    def dda_line_compare(x0, y0, x1, y1):
        """Versão simples do DDA para comparação"""
        points = []
        dx = x1 - x0
        dy = y1 - y0
        steps = max(abs(dx), abs(dy))

        if steps == 0:
            return [(int(x0), int(y0))]

        x_increment = dx / steps
        y_increment = dy / steps

        x, y = x0, y0

        for i in range(int(steps) + 1):
            points.append((int(round(x)), int(round(y))))
            x += x_increment
            y += y_increment

        return points

    @staticmethod
    def bresenham_line_compare(x0, y0, x1, y1):
        """Versão simples do Bresenham para comparação"""
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


if __name__ == "__main__":
    import sys

    # Executa a demonstração do DDA
    DDADemo.visualize_dda()

    # Comparação opcional
    print("\n" + "=" * 50)
    resposta = input("Mostrar comparação DDA vs Bresenham? (s/n): ")
    if resposta.lower() == 's':
        DDADemo.compare_algorithms()

    print("\n" + "=" * 50)
    resposta = input("Executar programa gráfico? (s/n): ")

    if resposta.lower() == 's':
        app = LineDrawer()
        app.run()
    else:
        print("Encerrando...")