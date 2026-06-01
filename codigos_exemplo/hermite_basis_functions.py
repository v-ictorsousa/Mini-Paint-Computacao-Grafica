import numpy as np
import matplotlib.pyplot as plt


def hermite_basis_functions(t):
    """
    Calcula as 4 funções de base de Hermite para um dado t
    """
    t2 = t * t
    t3 = t2 * t

    h00 = 2 * t3 - 3 * t2 + 1  # Coeficiente de P₀
    h10 = t3 - 2 * t2 + t  # Coeficiente de T₀
    h01 = -2 * t3 + 3 * t2  # Coeficiente de P₁
    h11 = t3 - t2  # Coeficiente de T₁

    return h00, h10, h01, h11


# Visualização das funções de base
def plot_basis_functions():
    t = np.linspace(0, 1, 100)
    h00, h10, h01, h11 = hermite_basis_functions(t)

    plt.figure(figsize=(10, 6))
    plt.plot(t, h00, 'b-', label='H₀₀ (P₀)', linewidth=2)
    plt.plot(t, h10, 'r-', label='H₁₀ (T₀)', linewidth=2)
    plt.plot(t, h01, 'g-', label='H₀₁ (P₁)', linewidth=2)
    plt.plot(t, h11, 'm-', label='H₁₁ (T₁)', linewidth=2)
    plt.grid(True, alpha=0.3)
    plt.xlabel('t', fontsize=12)
    plt.ylabel('Valor da função base', fontsize=12)
    plt.title('Funções de Base de Hermite', fontsize=14)
    plt.legend()
    plt.axhline(y=0, color='k', linestyle='-', alpha=0.3)
    plt.show()


plot_basis_functions()