# Mini Paint --- Computação Gráfica

Um aplicativo interativo de desenho (estilo Paint) desenvolvido em Python, utilizando a biblioteca **Dear ImGui** para a interface gráfica de usuário (GUI). O projeto foi construído do zero com o objetivo de aplicar, na prática, os principais algoritmos clássicos de rasterização da disciplina de Computação Gráfica.

---

## 🚀 Funcionalidades

O projeto simula um software de pintura digital completo, contendo:
* **Lona Dinâmica (Canvas):** Lógica customizada de matriz de pixels para renderização de desenhos.
* **Ferramenta Lápis (Pencil):** Desenho livre pixel a pixel.
* **Ferramenta Borracha (Eraser):** Limpeza seletiva de pixels no canvas.
* **Lixeira (Clear Screen):** Limpa toda a tela instantaneamente.
* **Ferramentas de Formas Geométricas e Preenchimento:** Implementadas manualmente com algoritmos matemáticos, sem o uso de funções prontas de desenho da biblioteca.

---

## 🧠 Conceitos de Computação Gráfica Implementados

Em vez de utilizar funções nativas do ecossistema de interface para desenhar retas ou círculos, toda a rasterização na tela foi codificada manualmente através dos seguintes algoritmos estruturados:

* **Algoritmo de Linha de Bresenham:** Utilizado para calcular os pixels que formam linhas retas com alta performance (apenas aritmética de inteiros), aplicado na ferramenta de linhas e formas.
* **Algoritmo DDA (Digital Differential Analyzer):** Implementação linear passo a passo para estudo comparativo de interpolação e rasterização de retas.
* **Algoritmo de Bresenham para Círculos (Ponto Médio):** Utilizado na ferramenta de geração de circunferências e círculos perfeitos de forma incremental.
* **Flood Fill (Preenchimento por Balde):** Algoritmo de semente recursivo utilizado na ferramenta de balde de tinta para preencher áreas delimitadas com uma nova cor.

A estrutura do repositório também conta com uma pasta de `codigos_exemplo` detalhando o desenvolvimento evolutivo e isolado de cada um desses conceitos antes da integração no ecossistema principal.

---

## 🛠️ Tecnologias Utilizadas

* **Python 3** (Linguagem base)
* **Dear ImGui** (via `imgui` / `pyimgui` para renderização da interface e janelas)
* **OpenGL** / **PyGLFW** (para gerenciamento de janelas e contexto gráfico de backend)

---

## 💻 Como Rodar o Projeto

Siga os passos abaixo para clonar o repositório e executar o Mini Paint na sua máquina.

### Pré-requisitos
Certifique-se de ter o Python 3 instalado no seu computador. Você também precisará do gerenciador de pacotes `pip`.

### 1. Clonar o Repositório
Abra o seu terminal ou prompt de comando (CMD) e execute:
```bash
git clone [https://github.com/v-ictorsousa/Mini-Paint-Computacao-Grafica.git](https://github.com/v-ictorsousa/Mini-Paint-Computacao-Grafica.git)
cd Mini-Paint-Computacao-Grafica
