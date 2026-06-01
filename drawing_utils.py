from collections import deque

# Classe auxiliar que guarda de forma estática todos os métodos de calculo de desenho
# estes métodos não mudam por isso são estáticos
class DrawingUtils:

    # Uma versão otimizada de bresenham que calcula a linha que deveria ser desenhada ponto a ponto
    # usando inteiros para eliminar gargalo de calcular ponto flutuante
    @staticmethod
    def bresenham_line_integer( x0, y0, x1, y1) -> list[tuple[int, int]]:
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
    
    # Uma adaptação do código anterior onde calculamos não apenas uma linha mas sim todos os pontos em volta do circulo
    # baseados no raio dele e retornamos uma lista desses pontos
    @staticmethod
    def bresenham_circle(cx, cy, r) -> list[tuple[int, int]]:
        points = []
        x = 0
        y = -r
        p = -r

        while x < -y:
            if p > 0:
                y += 1
                p += 2*(x+y) + 1
            else:
                p += 2*x + 1
            

            # Observa que são 8 pois estamos calculando do centro até cada "canto"
            points.append((cx + x, cy + y)) # Ponto para a direita e baixo
            points.append((cx - x, cy + y)) # Ponto para esquerda e baixo
            points.append((cx + x, cy - y)) # Ponto para a direita e cima
            points.append((cx - x, cy - y)) # Ponto para a esquerda e cima
            
            # Daqui pra baixo basicamente pegamos os complementos dos pontos anteriores, ou seja,
            # aqueles pontos que estão paralelos aos anteriores
            points.append((cx + y, cy + x))
            points.append((cx + y, cy - x))
            points.append((cx - y, cy + x))
            points.append((cx - y, cy - x))

            x += 1

        return points
    
    # Esse método é usado pelo balde para preencher uma areá completa, ele usa o método de
    # 4 pixels, ou seja, ele enche de 4 em 4 pixels o que é melhor para o tratamento de diagonais
    def flood_fill(start_coord_x, start_coord_y, new_color, canvas) -> None:
        # Cor que queremos preencher, ou seja, a cor que queremos pintar por cima
        target_color = canvas.get_pixel(start_coord_x, start_coord_y)

        # Se a cor que queremos pintar por cima for igual a cor que estamos aplicando então não tem que pintar
        if target_color == new_color:
            return
        
        # Usamos a biblioteca deque para fazer a fila de pintura, usamos a fila pois o pixel que entra primeiro deve ser o primeiro
        # a ser desenhado por cima, dessa forma vamos desenhando da onde clicamos até as bordas do desenho, ou seja, até onde
        # a cor muda
        queue = deque([(start_coord_x, start_coord_y)])

        # Loop de desenho, viamos por todos os pixels quadados na fila
        while queue:
            # Coordenadas do pixel que estamos pegando agora
            coord_x, coord_y = queue.popleft()

            # Checa se é valida, ou seja, se está dentro do canvas
            if 0 <= coord_x < canvas._width and 0 <= coord_y < canvas._height:
                # Esse check basicamente pergunta, o pixel aqui é da cor que queremos pintar por cima
                # se for ele pinta e pega os 4 pixels em volta e colocam na fila, se não for ele não pinta
                # e não pega os pixels em volta, pois significa que terminamos de pintar para aquele lado
                if canvas.get_pixel(coord_x, coord_y) == target_color:
                    canvas.put_pixel(coord_x, coord_y, new_color)
                    queue.append((coord_x + 1, coord_y))
                    queue.append((coord_x - 1, coord_y))
                    queue.append((coord_x, coord_y - 1))
                    queue.append((coord_x, coord_y + 1))