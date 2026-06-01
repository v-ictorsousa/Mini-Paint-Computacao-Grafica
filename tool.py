from abc import ABC, abstractmethod
from canvas import Canvas

# Classe mãe de todas as ferramentas, ABC e abstractmethod é para fazer a classe se tornar abstrata
class Tool(ABC):
    def __init__(self, color: tuple[int, int, int] = (0, 0, 0), size: float = 1.0, canvas: Canvas = None):
        self._color: tuple[int, int, int] = color
        self._size: float = size
        self._is_drawing = False
        self._canvas = canvas
        self._disk_cache: dict[int, list] = {}
            
    @abstractmethod
    def on_press(self, x, y): ...

    @abstractmethod
    def on_drag(self, x, y): ...

    @abstractmethod
    def on_release(self): ...

    @property
    def is_drawing(self) -> bool:
        return self._is_drawing

    @property
    def color(self) -> tuple[int, int, int]:
        return self._color
    
    @color.setter
    def color(self, color: tuple[int, int, int]) -> None:
        self._color = color
    
    @property
    def size(self) -> float:
        return self._size
    
    @size.setter
    def size(self, size: float) -> None:
        self._size = size
    
    @property
    def canvas(self) -> Canvas:
        return self._canvas
    
    @canvas.setter
    def canvas(self, canvas: Canvas) -> None:
        self._canvas = canvas

    # Método get_disk basicamente cria no disk_cache a informação de um disco em volta de um pixel, isso é para
    # desenhar linhas mais grossas, sempre salvamos a area em volta de um pixel e deseignamos ela como desenhavel
    def _get_disk(self, size) -> list:
        radius = int(size) // 2
        if radius not in self._disk_cache:
            self._disk_cache[radius] = self._build_disk(radius)
        return self._disk_cache[radius]

    # Método estático pois queremos que seja carregado uma vez apenas para a memoria, ele nunca muda
    # draw_in_size basicamente usa nosso método de desenhar pixel a pixel para desenhar os discos que compoém o tamanho da linha mais grossa
    @staticmethod
    def _draw_in_size(coord_x, coord_y, canvas, color, disk) -> None:
        for dx, dy in disk:
            # Dentro do vetor de disco pega cada offset, dx e dy, e vai colocando os pixels em cada ponto do disco
            # por isso passamos as coordenadas + os offsets
            canvas.put_pixel(coord_x + dx, coord_y + dy, color)

    # Esse método constroi o disco, basicamente é o método que calcula a lista de pontos que compoem o disco
    # retorna essa lista de pontos como um offset que é usado pelo draw_in_size para falar pro put_pixel
    # CADA pixel que deve ser pintado
    @staticmethod
    def _build_disk(radius: int) -> list[tuple[int, int]]:
        offsets = []
        
        # Usamos a mesma lógica no desenho de circulo
        # Basicamente pegamos de -raio a raio + 1
        # ex: raio = 5 então circulo com raio 5 e diametro 10
        # ou seja, vai de x = 0 a x = 10 e y = 0 a y = 10, logo -raio nesse caso é
        # -5 e raio + 1 é 6, logo o -raio fala que queremos ir para a esquerda raio vezes
        # e raio + 1 diz que queremos ir para a direita raio + 1 vezes, para y é a mesma coisa,
        # ou seja, estamos pegando cada pixel em cada extremidade do raio, e colocando isso no vetor de disco
        # ou seja, estamos formando os offsets do ponto central do circulo 
        for dy in range(-radius, radius + 1):
            for dx in range(-radius, radius + 1):
                if dx**2 + dy**2 <= radius**2:
                    offsets.append((dx, dy))
        return offsets