import imgui
from imgui.integrations.glfw import GlfwRenderer
import glfw
from OpenGL.GL import *
from canvas import Canvas
from tool import Tool

# A classe que cria a janela e gerencia tudo que acontece nela
# Usa glfw para criar a janela e gerenciar as entradas de dados do mouse
# Usa imgui para gerenciar a GUI do programa.
class Window:

    # Construtor
    def __init__(self, title = "MiniPaint", width = 900, height = 600):
        self._active_tool: Tool = None # Ferramenta selecionada atualmente
        self._title = title # Titulo da janela, existe aqui por modularidade mas em realidade sempre vai ser MiniPaint
        self._width = width # Largura da janela
        self._height = height # Altura da janela, note que é diferente do canvas, pois os 100px extras de largura são para a barra lateral na direita
        self._toolbar_height = 40 # Altura da barra de ferramentas
        self._sidebar_width = 100 # Largura da barra lateral
        self._win: glfw._GLFWwindow = self._create_window() # Janela criada pelo glfw, já criamos elas assim que instânciamos um objeto dessa classe
        self._canvas = Canvas(800, 600) # Instâncioamos um canvas assim que instânciamos um objeto janela, basicamente na main sempre interagimos apenas com a janela
        self._save_filename = "desenho.png" # Nome base para o arquivo
        self._tools = {} # Dicionário de ferramentas
        
        imgui.create_context() # aqui criamos o contexto do imgui
        self._imgui_renderer = GlfwRenderer(self._win) # Aqui salvamos um renderizados do IMGUI que usa glfw
        self._setup_mouse_callbacks() # Configuramos os callbacks de mouse

    # @property são getters e @metodo.setter são os setters com mesmo nome dos getters
    @property
    def tools(self) -> dict:
        return self._tools
 
    @property
    def active_tool(self) -> Tool:
        return self._active_tool
 
    @active_tool.setter
    def active_tool(self, tool: Tool) -> None:
        self._active_tool = tool
 
    @property
    def canvas(self) -> Canvas:
        return self._canvas
 
    @property
    def width(self) -> int:
        return self._width
 
    @property
    def height(self) -> int:
        return self._height
 
    @property
    def win(self) -> glfw._GLFWwindow:
        return self._win
    
    @property
    def title(self) -> list:
        return self._title

    # Esse metodo cria a janela do programa usando glfw por isso o retorno é _GLFWwindow
    def _create_window(self) -> glfw._GLFWwindow:
        if not glfw.init():
            raise Exception("GLFW falhou ao iniciar")

        # Cria a janela e a hint de que ela pode ser manipulada para aumentar ou diminuir de tamanho
        glfw.window_hint(glfw.RESIZABLE, glfw.TRUE)
        window = glfw.create_window(self.width, self.height, self.title, None, None)

        if not window:
            glfw.terminate()
            raise Exception("GLFW falhou ao criar a janela")

        # Marca a janela criada como o contexto atual
        glfw.make_context_current(window)

        # Coloca a cor de fundo da janela, como queremos diferenciar o canvas da janela
        # pintamos o fundo de cinza pois o canvas sera branco
        # glClearColor é uma função do OpenGL que recebe 4 parâmetros onde os três primeiros são as cores e
        # o quarto é a transparencia da cor, as cores vão de 0 a 1.0 assim como a transpoarencia, sendo
        # representadas como porcentagens
        glClearColor(0.663, 0.663, 0.663, 1.0)
        
        # Este callback checa se o botão de maximizar da janela foi clicado
        self._resize_callback(window, self.width, self.height)

        # Aqui setta o callback de maximizar para funcionar no programa
        glfw.set_framebuffer_size_callback(window, self._resize_callback)
        return window

    # Esse metodo simplesmente faz todo o setup do funcionamento do mouse
    def _setup_mouse_callbacks(self) -> None:
        glfw.set_mouse_button_callback(self.win, self._mouse_button_callback)
        glfw.set_cursor_pos_callback(self.win, self._cursor_pos_callback)

    # Nesse metodo é aonde a logica do mouse é feita, recebe a janela, botão e ação
    def _mouse_button_callback(self, window, button, action, mods) -> None:
        # Essa linha basicamente sinaliza se o imgui também quer capturar o mouse, necessária
        # para o funcionamento simultâneo, caso ela seja retirada não é possível selecionar
        # as ferramentas usando os botões da GUI
        if imgui.get_io().want_capture_mouse:
            return
        
        # Check simples se existe alguma ferramenta sendo usada, caso não exista a função não deve capturar nenhuma ação pois
        # não estamos querendo desenhar nada
        if self.active_tool is None:
            return
        
        # Pega a posição do clique
        coord_x, coord_y = glfw.get_cursor_pos(window)
        
        # Checa se o botão clicado foi o esquerdo, e então checa qual foi a ação
        # clique ou soltar o botão
        if button == glfw.MOUSE_BUTTON_LEFT:
                if action == glfw.PRESS:
                    self._active_tool.on_press(coord_x, coord_y)
                elif action == glfw.RELEASE:
                    self.active_tool.on_release()

    # Esse método basicamente faz o mesmo que o anterior, como queriamos que nossas ferramentas funcionassem
    # com clicar, segurar o clique e arrastar, então tratamos o arrasto em um callback diferente pois não precisamos
    # simplesmente tratar se for clicado, mas sim se ele esta sendo arrastado e precisamos passar a posição constantemente
    # Aqui só tramamos se a ferramenta está desenhando ou não e se ela está ativa, o loop de desenho é tratado em outro método    
    def _cursor_pos_callback(self, window, x, y) -> None:
        if self.active_tool is None:
            return
        if self.active_tool.is_drawing:
            self.active_tool.on_drag(x, y)

    # Esse callback trata o tamanho da tela, ele basicamente existe para que a tela seja
    # propriamente desenhada quando a janela for maximizada
    def _resize_callback(self, window, width, height) -> None:
        self._width = width
        self._height = height
        
        # glViewport basicamente recebe a nova posição, os primeiros dois parêmtros são o offset
        # como queremos sempre desenhar a partir de (0,0) então passamos 0 como parametro, a altura também é a padrão
        # mas a largura precisamos considerar o tamanho do espaço separado para o menu lateral onde o imgui vai usar para
        # desenhar o menu de cores, espessura, salvar e novo
        glViewport(0, 0, width - self._sidebar_width, height)
        
        # Basicamente diz para o contexto qual matriz na pilha que queremos que as operações sejam feitas
        # Aqui queremos que seja a matriz de projeção
        glMatrixMode(GL_PROJECTION)
        
        # Basicamente carrega dentro da matriz a matriz de identidade.
        glLoadIdentity()
        
        # Multiplica a matriz por uma matriz ortogonal, ou seja, pega nossa matriz identidade
        # e multiplica por uma matriz com as informações passadas como parâmetro
        # Basicamente é o que dita as zonas de clipping, zonas onde queremos que seja possivel alterar o contexto
        glOrtho(0, width - self._sidebar_width, height, 0, -1, 1)
        
        # Avisamos que agora queremos mexer na matriz de modelview e carregamos a matriz indetidade nela novamente
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    # Simples check se a janela fechou
    def should_close(self) -> None:
        return glfw.window_should_close(self.win)

    # Nosso loop principal condensado em um método, no caso o loop principal ainda é tratado pela main
    # mas ele não chama tudo que está aqui dentro separando o trabalho da main do gerenciador de janelas
    # na main o loop principal simplesmente chama update a cada iteração
    def update(self) -> None:
        # Processamento de eventos do glfw e do imgui
        # basicamente é aqui que vai ler os callbacks e dizer ao sistema o que fazer
        glfw.poll_events()
        self._imgui_renderer.process_inputs()

        # Renderizamos primeiro a ui usando IMGUI
        imgui.new_frame()
        self._render_ui()
        imgui.render()

        # Aqui limpamos a tela, desenhamos o canvas, redesenhamos a GUI e trocamos o frame atual pelo framebuffer
        glClear(GL_COLOR_BUFFER_BIT)
        self.canvas.draw()
        self._imgui_renderer.render(imgui.get_draw_data())
        glfw.swap_buffers(self.win)

    # Fecha o glfw e o imgui
    def terminate(self) -> None:
        self._imgui_renderer.shutdown()
        glfw.terminate()

    # Esse método registra todas as ferramentas que podem ser usadas pelo programa, dessa forma a janela sabe quais ferramentas
    # estão disponíveis, o vetor de ferramentas é um auxiliar para que o IMGUI consiga interligar os botões com sucesso a cada ferramenta
    def register_tool(self, name: str, tool: Tool) -> None:
        self._tools[name] = tool
        tool.canvas = self._canvas

    # Método principal de desenho da GUI, basicamente usa 100%$ imgui para desenhar toda a GUI
    def _render_ui(self) -> None:
        
        # Configurações do imgui, basicamente selecionamos onde queremos desenhar a proxima gui, fazemos com que o largura
        # seja o mesmo da janela e a altura seja 40 pixels, criamos então a nossa toolbar mas com flags que impedem que seja uma janela separada
        # em primeira instância tentamos usar begin_main_menu() que basicamente cria uma barra de menu como de aplicativos normais, com botões
        # que abrem em cascata com várias opções, porém não dava pra fazer o funcionamento de ferramentas corretamente assim e pra não criar muitos
        # componentes de ui fomos por esse atalho
        imgui.set_next_window_position(0, 0)
        imgui.set_next_window_size(self._width, self._toolbar_height)
        imgui.begin("##toolbar", flags=
            imgui.WINDOW_NO_TITLE_BAR |
            imgui.WINDOW_NO_RESIZE |
            imgui.WINDOW_NO_MOVE |
            imgui.WINDOW_NO_SCROLLBAR
        )

        # Aqui basicamente desenha o botão e trata o que acontece ao clicar
        # em um botão de ferramenta
        # exemplo: Ao clicar em Lapis, manda pra cá e colocar a pencil_tool como ferramenta ativa
        for name, tool in self._tools.items():
            if imgui.button(name):
                self.active_tool = tool
            imgui.same_line()

        # Termina o desenho da barra superior de ferramentas
        imgui.end()

        # Aqui estamos desenhando a barra lateral para as 8 cores fixas, usamos o mesmo truque que usamos com a barra
        # de ferramentas, no caso observe que estamos dizendo que o local que desenharemos sera
        # a largura da tela - largura da barra, isto é por que queremos a barra do lado direito da tela
        # e seu tamanho será basicamente o tamanho settado para ela, que é 100px e a altura da tela para
        # percorrer a tela inteira
        imgui.set_next_window_position(self._width - self._sidebar_width, self._toolbar_height)
        imgui.set_next_window_size(self._sidebar_width, self._height)
        imgui.begin("##sidebar", flags=
            imgui.WINDOW_NO_TITLE_BAR |
            imgui.WINDOW_NO_RESIZE |
            imgui.WINDOW_NO_MOVE |
            imgui.WINDOW_NO_SCROLLBAR
        )

        # Aqui estamos criando cada botão, separator() basicamente desenha uma linha onde ele aparece
        imgui.separator()
        
        # Ao clicar em novo simplesmente limpa a tela
        if imgui.button("Novo"):
            self.canvas.clear()
        
        imgui.separator()
        
        # Ao clica em salvar abre um popup
        if imgui.button("Salvar"):
            imgui.open_popup("Salvar")
        imgui.same_line()
        
        # Criação do popup de salvar, coloca um texto pedindo o nome do arquivo
        if imgui.begin_popup("Salvar"):
            imgui.text("Nome do arquivo:")
            
            # Cria uma caixa que recebe um texto, changed vai ser o check se foi digitado algo para salvar na memoria a nova informação
            changed, self._save_filename = imgui.input_text("##filename", self._save_filename, 256)
            
            # Botão que confirma o salvamento, _save_filename é o caminho obtido no passo anterior
            # apos salvar fecha o popup
            if imgui.button("Confirmar"):
                self.canvas.save(self._save_filename)
                imgui.close_current_popup()
            
            # Botão de cancelar que fecha o popup sem fazer nada
            # same_line() basicamente diz que o que eu quero desenhar está na mesma linha
            # do que já foi desenhado, isso deixa salvar e cancelar um do lado do outro na tela
            imgui.same_line()
            if imgui.button("Cancelar"):
                imgui.close_current_popup()
            
            # new_line() basicamente diz que queremos que as proximas coisas sejam desenhadas abaixo da linha anterior
            # escrevemos uma explicação simples do caminho padrão e termina o desenho do popup
            imgui.new_line()
            imgui.text("O seu arquivo será salvo na pasta (imagens salvas) dentro do diretório do programa")
            imgui.end_popup()

        imgui.separator()
        # Aqui começamos o desenho da area das cores bases
        imgui.text("Cores")
        imgui.separator()

        # Cores que serão usadas
        colors = [
            ("Preto",   (0, 0, 0)),
            ("Branco",  (255, 255, 255)),
            ("Vermelho",(255, 0, 0)),
            ("Azul",    (0, 0, 255)),
            ("Amarelo", (255, 255, 0)),
            ("Ciano",   (0, 255, 255)),
            ("Magenta", (255, 0, 255)),
        ]

        # Desenhamos um botão para cada cor de tamanho 80
        for name, color in colors:
            
            # Tratamento de tipo de dados, basicamente passamos por cada cor
            # E dividimos ela por 255, isto é por que nosso moedlo usa
            # inteiros de 0 a 255 para cores, mas o imgui usa float
            # então estamos basicamente separando cada cor em seu valor float
            # is_active é axuliar para o highlight
            r, g, b = [c / 255 for c in color]
            is_active = self.active_tool and self.active_tool.color == color
    
            # Colocamos a cor dentro do botão desenhado
            imgui.push_style_color(imgui.COLOR_BUTTON, r, g, b, 1.0)
            imgui.push_style_color(imgui.COLOR_BUTTON_HOVERED, r, g, b, 0.8)
            
            # Borda mais clara se for a cor ativa
            border = 2.0 if is_active else 0.0
            imgui.push_style_var(imgui.STYLE_FRAME_BORDERSIZE, border)
            
            # Basicamente criamos o botão e chamos o clique e passamos a cor que foi clicada
            # f"    ##{name}" baiscamente da um nome único para cada botão, mesmo que não veremos
            # é necessário pois o imgui precisa que cada botão tenha um nome único já que usa esse nome
            # para referenciar o botão
            if imgui.button(f"  ##{name}", width=80):
                if self.active_tool:
                    self.active_tool.color = color
            
            # pop_style_color com 2 pois demos 2 pushes anteriormente
            # pop_style_varpois fizemos um push_style_var
            imgui.pop_style_var()
            imgui.pop_style_color(2)

        imgui.separator()
        
        # Por fim estamos criando um slider para o tamanho, nesse caso
        # é possível escolher tamanhos intermediários entre os fixos
        # os valores são de 1 a 10 e são em float, basicamente eles dizem
        # Quantos pixels cada linha deve ter de espessura
        imgui.text("Tamanho")
        changed, size = imgui.slider_float("", self.active_tool.size, 1.0, 10.0)
        if changed:
            self.active_tool.size = size
        
        imgui.separator()
        
        # Aqui criamos 3 tamanhos fixos, o interessante é que ao clicar
        # em cada um dos botões aqui o slider também muda mostrando cada
        # valor do botão na prática
        imgui.text("Tamanho Fixo")
        if imgui.button("Pequeno"):
            self.active_tool.size = 1.0
        if imgui.button("Medio"):
            self.active_tool.size = 5.0
        if imgui.button("Grande"):
            self.active_tool.size = 10.0

        # Termina de desenhar tudo da GUI
        imgui.end()