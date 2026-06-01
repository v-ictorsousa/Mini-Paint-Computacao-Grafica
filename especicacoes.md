# Trabalho do Mini Paint
## Requisitos funcionais mínimos

1. Área de desenho (canvas) de tamanho fixo (ex.: 800x600)
2. **Ferramentas essenciais:**
    - Lápis (pincel de 1 pixel)
    - Borracha (pinta com a cor do fundo)
    - Linha reta (algoritmo de Bresenham ou DDA)
    - Retângulo vazado e preenchido
    - Círculo vazado e preenchido
    - Balde de tinta (Flood fill com 4 ou 8 conectado)
3. Paleta de cores com pelo menos 8 cores pré-definidas (preto, branco, vermelho, azul, amarelo, ciano, magenta)
4. Seleção de espessura do pincel/ferramenta (3 opções: Fino, médio, grosso)
5. **Botão "Novo"** (Limpa o canvas com a cor de fundo)
6. **Botão "Salvar"** (exportar para um formato simples, como BMP, PPM ou PNG via biblioteca)

## Requisitos técnicos

- Para desenho primitivo podemos usar SDL2, SFML, OpenGL com glDrawPixels o que não podemos é usar funções prontas de desenho de linha como drawLine.
### Deve ser implementado
- put_pixel(x, y, cor)
- get_pixel(x, y)
- Algoritmo de linha (Bresenham)
- Algorítmo de círculo (Bresenham ou ponto médio)
- Flood fill recursivo ou com pilha/queue (não usar função pronta).
- **Tratamento de eventos** do mouse (clique, arrasto, soltar)
- **Estrutura de dados para** o canvas: matriz 2D de inteiros (cores indexadas) ou struct RGB