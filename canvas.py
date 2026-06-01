from OpenGL.GL import *
import numpy as np
from PIL import Image
import os

# Classe que cuida do canvas, e suas funcionalidades
class Canvas:

    BG_COLOR = (255, 255, 255) # Cor do canvas, branca por padrão

    def __init__(self, width, height):
        self._width = width
        self._height = height
        self._pixels = np.full((height, width, 3), self.BG_COLOR, dtype=np.uint8) # Preenchendo a matriz que sera o canvas com o branco

    @property
    def width(self):
        return self._width
    
    @width.setter
    def width(self, width) -> None:
        self._width = width
    
    @property
    def height(self):
        return self._height
    
    @height.setter
    def height(self, height) -> None:
        self._height = height
        
    @property
    def pixels(self) -> list[tuple[int, int]]:
        return self._pixels
    
    # Método put_pixel, basicamente recebe as coordenadas do pixel na matriz, e a cor que vai colocar lá, e a coloca
    def put_pixel(self, coord_x, coord_y, color: tuple[int, int, int]) -> None:
        coord_x, coord_y = int(coord_x), int(coord_y)
        if 0 <= coord_x < self._width and 0 <= coord_y < self._height:
            self._pixels[coord_y, coord_x] = color

    # Método que retorna qual a cor de um pixel selecionado
    def get_pixel(self, coord_x, coord_y) -> tuple[int, int, int]:
        coord_x, coord_y = int(coord_x), int(coord_y)
        if 0 <= coord_x < self._width and 0 <= coord_y < self._height:
            return tuple(self._pixels[coord_y, coord_x])
        return self.BG_COLOR
    
    # Pinta todo o canvas com a cor inical novamente
    def clear(self, color: tuple[int, int, int] | None = None) -> None:
        self._pixels[:] = color if color is not None else self.BG_COLOR

    # Esse método é o método que vai desenhar o que está no cavas a cada frame, usamos o glDrawPixels para
    # fazer o desenho final que aparecerá na janela, basicamente o put_pixel diz para nossa matriz as informações
    # do pixel, aqui nós ativamente desenhamos os pixels na tela
    def draw(self) -> None:
        glClear(GL_COLOR_BUFFER_BIT)

        data = np.ascontiguousarray(np.flipud(self._pixels))
        glRasterPos2f(0, self._height)
        glDrawPixels(self._width, self._height, GL_RGB, GL_UNSIGNED_BYTE, data)

    # Salvo uma snapshot, isso é usado apenas para que sempre que aumentemos o tamanho de uma figura
    # ao arrastar o mouse ela não deixe rastros pra tras da figura anterior, ou seja, não queremos desenhar varias
    # figuras ao arrastar o mouse, queremos apagar a anterior e desenhar a nova, fazemos isso colocando a snapshot por cima
    # antes de desenhar, ou seja, pegamos a imagem como estava antes de começar a desenhar a figura
    # e colocamos ela por cima antes de desenhar o novo tamanho da figura
    def snapshot(self) -> np.ndarray:
        return self._pixels.copy()
    
    # Esse é o método que coloca a snapshot na tela
    def restore(self, snapshot: np.ndarray) -> None:
        self._pixels[:] = snapshot

    # Esse método usa a biblioteca os para criar um diretório chamado imagens salvas na pasta do programa caso não exista
    # e usa a bilbioteca Image para salvar a imagem no diretório, o tipo de imagem pega do nome, isto é, .png, .jpg, .webp, etc.
    def save(self, filename: str) -> None:
        os.makedirs("imagens salvas", exist_ok=True)
        image = Image.fromarray(self._pixels, 'RGB')
        image.save(f"imagens salvas/{filename}")