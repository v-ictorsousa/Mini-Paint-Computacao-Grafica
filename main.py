from window_manager import Window
from pencil_tool import PencilTool
from bucket_tool import FloodFill
from circle_tool import CircleTool
from line_tool import LineTool
from rectangle_tool import RectangleTool
from eraser_tool import EraserTool

# Classe de inicialização do programa, compile ela para funcionamento do programa
def main():
    window = Window("MiniPaint") # Cria a janela
    
    # Registramos cada ferramenta
    window.register_tool("Lapis", PencilTool(color = (0, 0, 0)))
    window.register_tool("Balde", FloodFill(color = (0, 0, 0)))
    window.register_tool("Circulo", CircleTool(color = (0, 0, 0)))
    window.register_tool("Circulo Cheio", CircleTool(color = (0, 0, 0), is_filled=True))
    window.register_tool("Linha", LineTool(color = (0, 0, 0)))
    window.register_tool("Retangulo", RectangleTool(color = (0, 0, 0)))
    window.register_tool("Retangulo Cheio", RectangleTool(color = (0, 0, 0), is_filled=True))
    window.register_tool("Borracha", EraserTool(color= window.canvas.BG_COLOR, size=10.0))

    # Marcamos o lápis como a ferramenta ativa por padrão ao abrir o programa
    window.active_tool = window.tools["Lapis"]

    # Loop principal da janela, é aqui onde chamamos frame a frame o update para atualizar a janela
    while not window.should_close():
        window.update()

    # Terminamos o programa
    window.terminate()

# Garante que a ao compilar esse .py ele vai entender que deve rodar o programa
if __name__ == "__main__":
    main()