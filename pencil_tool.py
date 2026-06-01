from tool import Tool
from canvas import Canvas
from drawing_utils import DrawingUtils
from OpenGL.GL import *

# Ferramenta de lapis
class PencilTool(Tool):
    def __init__(self, color: tuple[int, int, int] = (0, 0, 0), size: float = 1.0, canvas: Canvas = None):
        super().__init__(color, size, canvas)
        self._last_pos = None

    @property
    def last_pos(self) -> tuple[int, int]:
        return self._last_pos
    
    # Ao clicar falmos que esta desenhando e salvamos o local do clique como a ultima posição
    def on_press(self, coord_x, coord_y) -> None:
        self._is_drawing = True
        self._last_pos = (coord_x, coord_y)

    # Ao arrastar desenhamos a linha e salvamos a ultima posição como onde está o mouse ao fim da chamada desse método
    def on_drag(self, coord_x, coord_y) -> None:
        if self._is_drawing and self._last_pos:
            self._draw_bresenham_line(self._last_pos, (coord_x, coord_y))
            self._last_pos = (coord_x, coord_y)

    # Ao soltar zeramos a posição e marcamos que não estamos mais desenhando
    def on_release(self) -> None:
        self._is_drawing = False
        self._last_pos = None

    # Neste método calculamos a linha usando bresenham, calculamos o disco para o tamanho e então desenhamos
    def _draw_bresenham_line(self, p1, p2) -> None:
        points = DrawingUtils.bresenham_line_integer(p1[0], p1[1], p2[0], p2[1])

        disk = self._get_disk(self.size)
        for point in points:
            Tool._draw_in_size(point[0], point[1], self.canvas, self.color, disk)