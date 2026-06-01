from tool import Tool
from canvas import Canvas
from drawing_utils import DrawingUtils
import numpy as np

# Ferramenta de desenhar circulo
class CircleTool(Tool):
    def __init__(self, color: tuple[int, int, int] = (0, 0, 0), size: float = 1.0, canvas: Canvas = None, is_filled: bool = None):
        super().__init__(color, size, canvas)
        self._center = (0,0)
        self._snapshot = None
        self._filled = is_filled

    @property
    def filled(self) -> bool:
        return self._filled
    
    @filled.setter
    def filled(self, filled: bool) -> None:
        self._filled = filled
    
    @property
    def center(self) -> tuple[int, int]:
        return self._center

    # Ao apertar settamos is_drawing = True, salvamos o centro como onde clicamos e salvamos a snapshot
    def on_press(self, x, y) -> None:
        self._is_drawing = True
        self._center = (x, y)
        self._snapshot = self.canvas.snapshot()
     
    # Ao arrastar desenhamos o snapshot por cima do canvas, isto é pra não ter residuos do circulo que não queremos mais ver
    # então pegamos o novo raio como sendo a diferença entre o centro e onde está o mouse
    # e chamamos o código apropriado de desenho, seja ele o simples ou o cheio
    def on_drag(self, x, y) -> None:
        if self._is_drawing:
            self.canvas.restore(self._snapshot)
            cx, cy = self._center
            r = int (((x - cx)**2 + (y - cy)**2)**0.5)
            if self.filled:
                self._draw_filled_circle(cx, cy, r)
            elif not self.filled:
                self._draw_bresenham_circle(cx, cy, r)
               
    # Ao soltar o botão resetamos as insformações da ferramenta
    def on_release(self) -> None:
        self._is_drawing = False
        self._center = None
        self._snapshot = None

    # Aqui é onde fazemos o desenho do circulo simples, basicamente passamos para
    # bresenham_circle que nos retorna os pontos que devemos desenhar
    # pegamos esses pontos e calculamos seus discos para o tamanho
    # e então desenhamos em tamanho os pixels
    def _draw_bresenham_circle(self, cx, cy, r) -> None:
        points = DrawingUtils.bresenham_circle(cx, cy, r)
        
        disk = self._get_disk(self.size)
        for point in points:
            Tool._draw_in_size(point[0], point[1], self.canvas, self.color, disk)

    # Aqui é onde desenhamos o circulo cheio, basicamente a ideia é vamos andar do topo do circulo
    # até a parte inferior dele, e vamos pintando cada pixel para a esquerda e direita até chegamos no raio,
    # ou seja, vamos pintando linha a linha do vetor que compoe a parte interna do circulo
    def _draw_filled_circle(self, cx, cy, r) -> None:
        for y in range(-r, r + 1):
            x_span = int((r**2 - y**2)**0.5)
            for x in range(-x_span, x_span):
                self.canvas.put_pixel(cx + x, cy + y, self.color)
    
    # Código pesquisado e deixado como exemplo, basicamente ao pesquisar formas de otimizar o desenho preenchido
    # encontramos que com np.ogrid podemos criar basicamente uma matriz binário que marca como 1 onde deve pintar
    # e 0 onde não deve, e cria uma mascara e chama put_pixel na máscara e pinta todos os pixels de uma vez
    # ao usar o código a performance não melhorou usando sozinho pois o pu_pixel ainda é feito com loops internos
    # que é o gargalo principal  a melhor maneira de otimizar seria fazer o put_pixel colocar um conjunto de pixels
    # a cada loop e não apenas um pixel, por exemplo se pintar de 2 em 2 pixels diminuimos o tempo de execução do put_pixel
    # pela metade, desse forma poderiamos pensar em possivelmente desenhar um multiplo de pixels, digamos que desenhariamos de 4 em 4 pixels toda
    # vez que o desenho for maior que 4 pixels, dessa forma para desenhos grandes não teriamos muito overheading, usar paralelismos também melhoraria muito
    #def _draw_filled_circle(self, cx, cy, r, canvas) -> None:
    #    y, x = np.ogrid[-cy:canvas.height - cy, -cx:canvas.width - cx]
    #    mask = x**2 + y**2 <= r**2
    #    canvas.pixels[mask] = self.color