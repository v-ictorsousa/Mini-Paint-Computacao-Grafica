from tool import Tool
from OpenGL.GL import *
from drawing_utils import DrawingUtils
from canvas import Canvas

# Ferramenta de balde
class FloodFill(Tool):
    
    def __init__(self, color: tuple[int, int, int], size: float = 1.0, canvas: Canvas = None):
        super().__init__(color, size, canvas)

    # Ao clicar falamos que estamos desenhando, chamamos flood_fill e marcamos novamente que não estamos desenhando
    # o balde deve simplesmente preencher uma area ao clicar, não tem arrasto
    def on_press(self, coord_x, coord_y) -> None:
        self._is_drawing = True
        DrawingUtils.flood_fill(coord_x, coord_y, self.color, self.canvas)
        self._is_drawing = False

    def on_drag(self, coord_x, coord_y) -> None:
        return

    def on_release(self) -> None:
        return