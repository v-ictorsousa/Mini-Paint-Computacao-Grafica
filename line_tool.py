from tool import Tool
from drawing_utils import DrawingUtils
from canvas import Canvas
import numpy as np

# Ferramenta de linha, ferramenta que desenha uma linha fixa
class LineTool(Tool):
    def __init__(self, color: tuple[int, int, int], size: float = 1.0, canvas: Canvas = None):
        super().__init__(color, size, canvas)
        self._start_point = None
        self._snapshot = None

    # Pegamos onde clicamos como o ponto incial, e salvamos uma snapshot
    def on_press(self, coord_x, coord_y) -> None:
        self._is_drawing = True
        self._start_point = (coord_x, coord_y)
        self._snapshot = self.canvas.snapshot()

    # Ao arrastar desenhamos a linha até o ponto atual, que é onde esta o ponteiro
    def on_drag(self, coord_x, coord_y) -> None:
        if self._is_drawing:
            self.canvas.restore(self._snapshot)
            self._draw_line(self._start_point, (coord_x, coord_y))

    # Ao soltar restauramos os atributos base
    def on_release(self) -> None:
        self._is_drawing = False
        self._start_point = None

    # Aqui chamamos o breseham_line_integer para calcular a linha, calculamos o disco de espessura e desenhamos a linha
    def _draw_line(self, p1, p2) -> None:
        points = DrawingUtils.bresenham_line_integer(p1[0], p1[1], p2[0], p2[1])
        
        disk = self._get_disk(self.size)
        for point in points:
            Tool._draw_in_size(point[0], point[1], self.canvas, self.color, disk)

    