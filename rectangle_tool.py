from tool import Tool
from canvas import Canvas
from drawing_utils import DrawingUtils
import numpy as np

# Ferramenta de retângulo, herda de Tool
class RectangleTool(Tool):
    def __init__(self, color: tuple[int, int, int] = (0, 0, 0), size: float = 1.0, canvas: Canvas = None, is_filled: bool = None):
        super().__init__(color, size, canvas)
        self._start_point = (0,0)
        self._snapshot = None
        self._filled = is_filled

    @property
    def filled(self) -> bool:
        return self._filled
    
    @filled.setter
    def filled(self, filled) -> None:
        self._filled = filled

    # Método que dita o que acontece quando clicamos na tela
    # No caso settamos is_drawing = True pois estamos desenhando um retângulo
    # Pegamos o ponto inicial, onde clicamos, e criamos o snapshot
    def on_press(self, x, y):
        self._is_drawing = True
        self._start_point = (x,y)
        self._snapshot = self.canvas.snapshot()
        
    # Neste método nós verificamos se estamos desenhadno, caso estejamos nós pegamos
    # o snapshot que salvamos novamente, e depois decidimos se é um retâgulo cheio ou não
    # e chamamos o método associado a cada um
    def on_drag(self, x, y) -> None:
        if self._is_drawing:
            self.canvas.restore(self._snapshot)
            if self._filled:
                self._draw_filled_rectangle(self._start_point, (x, y))
            else:
                self._draw_bresenham_rectangle(self._start_point, (x, y))
        
    # Ao soltar apagamos o ponto incial, e marcamos que não estamos mais desenhando
    def on_release(self) -> None:
        self._is_drawing = False
        self._start_point = None

    # Aqui temos o código que desenha o retângulo
    # Basicamente passamos dois pontos, onde clicamos e onde esta o mouse agora
    def _draw_bresenham_rectangle(self, p1, p2) -> None:
            
        # Calculamos o disco para o tamanho, se o tamanho for 1 essa fução só retorna direto o tamanho ela nem calcula nada
        disk = self._get_disk(self.size)
        
        #Linha do topo
        # Usamos bresenham que está na classe DrawingUtils para determinar os pontos
        points = DrawingUtils.bresenham_line_integer(p1[0], p1[1], p2[0], p1[1])
        
        # Desenhamos ponto a ponto os pixels
        for point in points:
            Tool._draw_in_size(point[0], point[1], self.canvas, self.color, disk)
                
        #Linha de baixo
        points = DrawingUtils.bresenham_line_integer(p1[0], p2[1], p2[0], p2[1])
        for point in points:
            Tool._draw_in_size(point[0], point[1], self.canvas, self.color, disk)
                
        #Linha da direita
        points = DrawingUtils.bresenham_line_integer(p2[0], p1[1], p2[0], p2[1])
        for point in points:
            Tool._draw_in_size(point[0], point[1], self.canvas, self.color, disk)

        #Linha da esquerda
        points = DrawingUtils.bresenham_line_integer(p1[0], p1[1], p1[0], p2[1])
        for point in points:
            Tool._draw_in_size(point[0], point[1], self.canvas, self.color, disk)

    # Aqui temos o método que desenha o retângulo cheio, basicamente
    # pegamos as coordenadas dos dois pontos principais, onde clicamos
    # e onde está o mouse, então desenhamos em todos os pixels dentro
    def _draw_filled_rectangle(self, p1, p2) -> None:
        x0, y0 = int(p1[0]), int(p1[1])
        x1, y1 = int(p2[0]), int(p2[1])
        for y in range(min(y0, y1), max(y0, y1)):
            for x in range(min(x0, x1), max(x0, x1)):
                self.canvas.put_pixel(x, y, self.color)