from pencil_tool import PencilTool


# Ferramenta de borracha, basicamente ela herda de lápis pois a borracha é
# funcionalmente apenas um lápis que SEMPRE desenha na cor de fundo
# a lógica de manter a cor não é tratada nesse classe e sim na detecção da ferramenta selecionada
class EraserTool(PencilTool):
    @property
    def color(self):
        return self.canvas.BG_COLOR
    
    @color.setter
    def color(self, value):
        pass