import glfw
import OpenGL.GL as gl
import numpy as np

# ============================================
# CONSTANTES E CONFIGURAÇÕES
# ============================================
WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 768


# ============================================
# FUNÇÕES DE DESENHO BASE
# ============================================
def draw_line_strip(points, color, line_width=2):
    """Desenha uma linha contínua passando pelos pontos"""
    gl.glLineWidth(line_width)
    gl.glColor3f(*color[:3])
    gl.glBegin(gl.GL_LINE_STRIP)
    for p in points:
        gl.glVertex2f(p[0], p[1])
    gl.glEnd()


def draw_polygon(points, color, line_width=1):
    """Desenha o polígono de controle"""
    if len(points) < 2:
        return
    gl.glLineWidth(line_width)
    gl.glColor3f(*color[:3])
    gl.glBegin(gl.GL_LINE_STRIP)
    for p in points:
        gl.glVertex2f(p[0], p[1])
    gl.glVertex2f(points[0][0], points[0][1])  # Fecha o polígono
    gl.glEnd()


def draw_points(points, color, point_size=6):
    """Desenha pontos de controle"""
    gl.glPointSize(point_size)
    gl.glColor3f(*color[:3])
    gl.glBegin(gl.GL_POINTS)
    for p in points:
        gl.glVertex2f(p[0], p[1])
    gl.glEnd()


def draw_line(p1, p2, color, line_width=2):
    """Desenha uma linha entre dois pontos"""
    gl.glLineWidth(line_width)
    gl.glColor3f(*color[:3])
    gl.glBegin(gl.GL_LINES)
    gl.glVertex2f(p1[0], p1[1])
    gl.glVertex2f(p2[0], p2[1])
    gl.glEnd()


# ============================================
# CURVA DE BÉZIER
# ============================================
def bezier_point(t, points):
    """
    Calcula um ponto na curva de Bézier usando algoritmo de De Casteljau.

    Args:
        t: parâmetro entre 0 e 1
        points: lista de pontos de controle (P0, P1, ..., Pn)

    Returns:
        ponto (x, y) na curva
    """
    # Copia os pontos de controle
    q = points.copy()
    n = len(points) - 1

    # Algoritmo de De Casteljau
    for r in range(1, n + 1):
        for i in range(n - r + 1):
            q[i] = (1 - t) * q[i] + t * q[i + 1]

    return q[0]


def generate_bezier_curve(points, num_segments=100):
    """Gera uma lista de pontos para desenhar a curva de Bézier"""
    curve_points = []
    for i in range(num_segments + 1):
        t = i / num_segments
        point = bezier_point(t, points)
        curve_points.append(point)
    return np.array(curve_points)


# ============================================
# CURVA DE HERMITE
# ============================================
def hermite_point(t, p0, p1, t0, t1):
    """
    Calcula ponto na curva cúbica de Hermite.

    Args:
        t: parâmetro entre 0 e 1
        p0, p1: pontos inicial e final
        t0, t1: vetores tangente em p0 e p1
    """
    t2 = t * t
    t3 = t2 * t

    # Funções de base de Hermite
    h00 = 2 * t3 - 3 * t2 + 1
    h10 = t3 - 2 * t2 + t
    h01 = -2 * t3 + 3 * t2
    h11 = t3 - t2

    return h00 * p0 + h10 * t0 + h01 * p1 + h11 * t1


def generate_hermite_curve(p0, p1, t0, t1, num_segments=100):
    """Gera uma curva de Hermite"""
    curve = []
    for i in range(num_segments + 1):
        t = i / num_segments
        point = hermite_point(t, p0, p1, t0, t1)
        curve.append(point)
    return np.array(curve)


# ============================================
# B-SPLINE
# ============================================
def bspline_basis(i, k, t, knots):
    """
    Calcula a função base B-Spline N_i,k(t)

    Args:
        i: índice da função base
        k: grau da curva
        t: parâmetro
        knots: vetor de nós
    """
    if k == 0:
        return 1.0 if knots[i] <= t < knots[i + 1] else 0.0

    # Recursão de Cox-De Boor
    left = 0.0
    if knots[i + k] != knots[i]:
        left = (t - knots[i]) / (knots[i + k] - knots[i]) * bspline_basis(i, k - 1, t, knots)

    right = 0.0
    if knots[i + k + 1] != knots[i + 1]:
        right = (knots[i + k + 1] - t) / (knots[i + k + 1] - knots[i + 1]) * bspline_basis(i + 1, k - 1, t, knots)

    return left + right


def generate_bspline_curve(control_points, degree=3, num_segments=200):
    """
    Gera uma curva B-Spline uniforme

    Args:
        control_points: pontos de controle
        degree: grau da curva (3 = cúbica)
        num_segments: resolução
    """
    n = len(control_points)
    if n <= degree:
        return np.array([])

    # Vetor de nós uniforme
    knots = np.linspace(0, 1, n + degree + 1)

    curve = []
    t_values = np.linspace(degree / len(knots),
                           (n - degree) / len(knots),
                           num_segments)

    for t in t_values:
        point = np.zeros(2)
        for i in range(n):
            basis = bspline_basis(i, degree, t, knots)
            if basis > 1e-6:  # Evita acumular ruído numérico
                point += basis * control_points[i]
        curve.append(point)

    return np.array(curve)


# ============================================
# CLASSE PRINCIPAL DA DEMONSTRAÇÃO
# ============================================
class CurveDemo:
    def __init__(self, window):
        self.window = window
        self.curve_type = 'bezier'  # 'bezier', 'hermite', 'bspline'

        # Pontos de controle para Bézier e B-Spline
        self.control_points = np.array([
            [-0.7, -0.3],
            [-0.4, 0.6],
            [0.0, 0.8],
            [0.4, 0.5],
            [0.7, -0.2]
        ], dtype=np.float32)

        # Configuração específica para Hermite
        self.hermite_p0 = np.array([-0.7, -0.3])
        self.hermite_p1 = np.array([0.7, 0.3])
        self.hermite_t0 = np.array([1.2, 0.6])
        self.hermite_t1 = np.array([1.0, -0.4])

        # Controle de animação
        self.animation_t = 0.0
        self.animate = False

    def draw_text_instructions(self):
        """Desenha instruções na tela (implementação simplificada)"""
        # Nota: Para texto real, seria necessário usar uma biblioteca como FreeType
        # Por enquanto, vamos apenas imprimir no console
        pass

    def draw_bezier(self):
        """Desenha curva de Bézier"""
        curve = generate_bezier_curve(self.control_points, 150)
        if len(curve) > 0:
            draw_line_strip(curve, (0.2, 0.8, 0.3, 1.0), line_width=3)

    def draw_hermite(self):
        """Desenha curva de Hermite"""
        curve = generate_hermite_curve(self.hermite_p0, self.hermite_p1,
                                       self.hermite_t0, self.hermite_t1, 150)
        draw_line_strip(curve, (1.0, 0.6, 0.2, 1.0), line_width=3)

        # Desenha tangentes
        draw_line(self.hermite_p0, self.hermite_p0 + self.hermite_t0 * 0.4,
                  (1.0, 0.8, 0.0, 1.0), line_width=1)
        draw_line(self.hermite_p1, self.hermite_p1 + self.hermite_t1 * 0.4,
                  (1.0, 0.8, 0.0, 1.0), line_width=1)

        # Desenha pontos extremos
        draw_points(np.array([self.hermite_p0, self.hermite_p1]),
                    (1.0, 0.5, 0.0, 1.0), point_size=10)

    def draw_bspline(self):
        """Desenha curva B-Spline"""
        curve = generate_bspline_curve(self.control_points, degree=3, num_segments=200)
        if len(curve) > 0:
            draw_line_strip(curve, (0.3, 0.6, 1.0, 1.0), line_width=3)

    def draw_control_polygon(self):
        """Desenha o polígono de controle baseado no tipo de curva"""
        if self.curve_type == 'hermite':
            # Para Hermite, mostramos os pontos extremos e tangentes
            points = np.array([self.hermite_p0,
                               self.hermite_p0 + self.hermite_t0 * 0.3,
                               self.hermite_p1 - self.hermite_t1 * 0.3,
                               self.hermite_p1])
            draw_polygon(points, (0.5, 0.5, 0.7, 1.0), line_width=1)
            draw_points(points, (1.0, 0.8, 0.2, 1.0), point_size=6)
        else:
            # Para Bézier e B-Spline
            draw_polygon(self.control_points, (0.5, 0.5, 0.7, 1.0), line_width=1)
            draw_points(self.control_points, (1.0, 0.8, 0.2, 1.0), point_size=8)

    def draw_de_casteljau_animation(self):
        """Anima o algoritmo de De Casteljau para Bézier"""
        if not self.animate or self.curve_type != 'bezier':
            return

        t = self.animation_t
        points = self.control_points.copy()
        n = len(points) - 1

        # Mostra todas as iterações do algoritmo
        for r in range(n + 1):
            if r > 0:
                # Desenha linhas entre pontos da iteração atual
                for i in range(n - r + 1):
                    if i < len(points) - 1:
                        draw_line(points[i], points[i + 1],
                                  (0.5, 0.5, 0.8, 1.0), line_width=1)

            # Calcula próximo nível de pontos
            next_points = []
            for i in range(n - r):
                next_points.append((1 - t) * points[i] + t * points[i + 1])

            if len(next_points) > 0:
                points = np.array(next_points)
            else:
                # Ponto final na curva
                draw_points(np.array([points[0]]), (1.0, 0.0, 0.0, 1.0), point_size=12)
                break

        # Atualiza animação
        self.animation_t += 0.01
        if self.animation_t > 1.0:
            self.animation_t = 0.0

    def handle_input(self):
        """Processa entrada do teclado"""
        # Teclas 1, 2, 3 para mudar tipo de curva
        if glfw.get_key(self.window, glfw.KEY_1) == glfw.PRESS:
            self.curve_type = 'bezier'
            print("Modo: Curva de Bézier")
        elif glfw.get_key(self.window, glfw.KEY_2) == glfw.PRESS:
            self.curve_type = 'hermite'
            print("Modo: Curva de Hermite")
        elif glfw.get_key(self.window, glfw.KEY_3) == glfw.PRESS:
            self.curve_type = 'bspline'
            print("Modo: B-Spline Cúbica")

        # Tecla A para animar De Casteljau
        if glfw.get_key(self.window, glfw.KEY_A) == glfw.PRESS:
            self.animate = not self.animate
            if self.animate:
                print("Animação De Casteljau: LIGADA")
            else:
                print("Animação De Casteljau: DESLIGADA")

        # Teclas R para resetar animação
        if glfw.get_key(self.window, glfw.KEY_R) == glfw.PRESS:
            self.animation_t = 0.0
            self.animate = False

    def run(self):
        """Loop principal da aplicação"""
        # Configuração inicial do OpenGL
        gl.glClearColor(0.1, 0.1, 0.15, 1.0)
        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

        print("\n=== DEMONSTRAÇÃO DE CURVAS EM COMPUTAÇÃO GRÁFICA ===")
        print("Teclas:")
        print("  1 - Curva de Bézier")
        print("  2 - Curva de Hermite")
        print("  3 - B-Spline Cúbica")
        print("  A - Animar algoritmo de De Casteljau (Bézier)")
        print("  R - Resetar animação")
        print("  ESC - Sair")
        print("=================================================\n")

        while not glfw.window_should_close(self.window):
            gl.glClear(gl.GL_COLOR_BUFFER_BIT)

            # Desenha grid de referência
            self.draw_grid()

            # Desenha a curva baseada no tipo selecionado
            if self.curve_type == 'bezier':
                self.draw_bezier()
            elif self.curve_type == 'hermite':
                self.draw_hermite()
            elif self.curve_type == 'bspline':
                self.draw_bspline()

            # Desenha polígono de controle
            self.draw_control_polygon()

            # Anima De Casteljau se necessário
            self.draw_de_casteljau_animation()

            # Processa input
            self.handle_input()

            # Mostra título do modo atual
            self.draw_mode_title()

            glfw.swap_buffers(self.window)
            glfw.poll_events()

            # Verifica ESC
            if glfw.get_key(self.window, glfw.KEY_ESCAPE) == glfw.PRESS:
                break

    def draw_grid(self):
        """Desenha um grid de referência"""
        gl.glLineWidth(1)
        gl.glColor3f(0.2, 0.2, 0.3)
        gl.glBegin(gl.GL_LINES)

        # Linhas verticais
        for x in np.arange(-1.0, 1.1, 0.2):
            gl.glVertex2f(x, -1.0)
            gl.glVertex2f(x, 1.0)

        # Linhas horizontais
        for y in np.arange(-1.0, 1.1, 0.2):
            gl.glVertex2f(-1.0, y)
            gl.glVertex2f(1.0, y)

        gl.glEnd()

        # Eixos principais
        gl.glLineWidth(2)
        gl.glColor3f(0.5, 0.5, 0.7)
        gl.glBegin(gl.GL_LINES)
        gl.glVertex2f(-1.0, 0.0)
        gl.glVertex2f(1.0, 0.0)
        gl.glVertex2f(0.0, -1.0)
        gl.glVertex2f(0.0, 1.0)
        gl.glEnd()

    def draw_mode_title(self):
        """Desenha título do modo atual (simplificado - texto no console)"""
        # Como desenhar texto no OpenGL puro é complexo,
        # vamos apenas manter o título no console
        pass


# ============================================
# INICIALIZAÇÃO DO GLFW
# ============================================
def init_glfw():
    """Inicializa GLFW e configura contexto OpenGL"""
    if not glfw.init():
        print("Erro: Não foi possível inicializar o GLFW")
        return None

    # Configuração para OpenGL moderno
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_COMPAT_PROFILE)  # Mude para COMPAT

    window = glfw.create_window(WINDOW_WIDTH, WINDOW_HEIGHT,
                                "Curvas em Computação Gráfica - Bézier, Hermite, B-Spline",
                                None, None)
    if not window:
        print("Erro: Não foi possível criar a janela")
        glfw.terminate()
        return None

    glfw.make_context_current(window)
    glfw.swap_interval(1)  # Vsync

    # Configura viewport e sistema de coordenadas
    gl.glViewport(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
    gl.glMatrixMode(gl.GL_PROJECTION)
    gl.glLoadIdentity()
    gl.glOrtho(-1.2, 1.2, -1.0, 1.0, -1.0, 1.0)  # Sistema de coordenadas
    gl.glMatrixMode(gl.GL_MODELVIEW)
    gl.glLoadIdentity()

    return window


# ============================================
# FUNÇÃO PRINCIPAL
# ============================================
def main():
    window = init_glfw()
    if not window:
        return

    demo = CurveDemo(window)
    demo.run()

    glfw.terminate()
    print("\nPrograma encerrado.")


if __name__ == "__main__":
    main()