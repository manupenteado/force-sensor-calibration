import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np
from scipy.stats import linregress

# ======================= CONFIGURAÇÕES NO TOPO ===============================

# Escolha da função: 1 = plotar apenas uma reta, 2 = plotar 3 retas no mesmo gráfico
function = 2          # <-- altere aqui

# Exibir barras de erro? (True = exibe, False = não exibe)
use_erros = True      # <-- altere aqui

# Número de pontos com maior valor espectral usados para a média
number_of_points_analyzed = 5

# Caminhos para as planilhas
script_folder = os.path.dirname(__file__)

# Caminho para a planilha única (usada quando function = 1)
excel_path_single = os.path.join(script_folder, "..", "testes/peca_circular_madeira/matriz/A2 - 5/dadosA2.xlsx")
excel_path_single = os.path.abspath(excel_path_single)

# Caminhos para as 3 planilhas (usados quando function = 2)
excel_paths_triple = [
    os.path.abspath(os.path.join(script_folder, "..", "testes/peca_circular_madeira/matriz/C1 - 5/dadosC1.xlsx")),
    os.path.abspath(os.path.join(script_folder, "..", "testes/peca_circular_madeira/matriz/C2 - 5/dadosC2.xlsx")),
    os.path.abspath(os.path.join(script_folder, "..", "testes/peca_circular_madeira/matriz/C3 - 5/dadosC3.xlsx"))
]

# Nome da imagem de saída
if function == 1:
    image_name = "media_spectral_shift_matrizA2.png"
else:
    image_name = "media_spectral_shift_triple.png"

# ======================= FUNÇÕES AUXILIARES (ORIGINAL) =======================

def strip_error_rows(df: pd.DataFrame):
    """Return (clean_df, errors).

    If the penultimate row of ``df`` contains the string ``"eror"`` in every
    column we assume the last row holds per-column error values.  The two
    rows are removed from ``clean_df`` and the list of errors is returned.
    Otherwise ``errors`` is None and ``clean_df`` is ``df`` unchanged.
    """
    errors = None
    if df.shape[0] >= 2:
        second_last = df.iloc[-2].astype(str).str.lower()
        if (second_last == "eror").all():
            errors = pd.to_numeric(df.iloc[-1], errors="coerce").tolist()
            df = df.iloc[:-2]
    return df, errors


# ======================= NOVA FUNÇÃO DE PROCESSAMENTO =========================

def process_excel(excel_path):
    """
    Lê e processa um arquivo Excel retornando os dados prontos para plotagem.
    """

    # Ler planilha e remover linhas de erro
    raw_df = pd.read_excel(excel_path)
    df, errors = strip_error_rows(raw_df)

    weights = []
    averages = []
    error_values = []  # espelha weights/averages se houver erros

    for idx, col in enumerate(df.columns):
        # massa está no cabeçalho, ex: "100g"
        weight = int(col.replace("g", ""))
        weights.append(weight)

        # converte coluna para numérico, descarta NaN
        series = pd.to_numeric(df[col], errors="coerce")
        top = series.nlargest(number_of_points_analyzed)
        averages.append(top.mean())

        if errors is not None:
            error_values.append(errors[idx])

    # Ordena por peso para garantir eixo x monotônico
    if errors is not None:
        weights, averages, error_values = zip(*sorted(zip(weights, averages, error_values)))
    else:
        weights, averages = zip(*sorted(zip(weights, averages)))

    # Converte de volta para lista (zip retorna tuplas)
    weights = list(weights)
    averages = list(averages)
    if errors is not None:
        error_values = list(error_values)

    # Encontra o índice da coluna com maior média (após ordenação)
    idx_max_global = averages.index(max(averages))
    # Linha do maior valor na planilha original
    linha_excel_max = df.iloc[:, idx_max_global].idxmax() + 2
    max_row_text = f"Maior ponto: Linha {linha_excel_max}"

    return weights, averages, error_values, max_row_text


# ======================= FUNÇÃO DE PLOTAGEM (MODIFICADA) =====================

def plot_one_dataset(ax, weights, averages, error_values, label, color,
                     annotate_max=True):
    """
    Desenha no eixo `ax` os pontos, barras de erro, linha tracejada,
    regressão linear e anotação do maior ponto para um único conjunto de dados.

    Parâmetros:
    - label: string para a legenda (usado na reta de regressão)
    - color: cor base para pontos, linha tracejada e regressão
    - annotate_max: se True, adiciona o texto do maior ponto no local do máximo
    """

    # Dispersão dos pontos
    ax.scatter(weights, averages, color=color, s=80, zorder=3)

    # Barras de erro conforme a flag global
    if use_erros and error_values:
        ax.errorbar(weights, averages, yerr=error_values,
                    fmt='none', ecolor='gray', capsize=5, alpha=0.7, zorder=2)

    # Linha tracejada conectando as médias
    ax.plot(weights, averages, color=color, linestyle='--', alpha=0.7, zorder=1)

    # Regressão linear
    slope, intercept, r_value, p_value, std_err = linregress(weights, averages)
    r_squared = r_value ** 2
    regression_line = [slope * x + intercept for x in weights]
    ax.plot(weights, regression_line, color=color, linestyle='-', linewidth=2,
            label=f"{label}: y={slope:.4f}x+{intercept:.4f}\n(R²={r_squared:.4f})",
            zorder=4)

    # Anotação do ponto máximo (se solicitado)
    if annotate_max:
        # Posiciona o texto próximo ao ponto de maior média
        max_idx = averages.index(max(averages))
        x_max = weights[max_idx]
        y_max = averages[max_idx]
        ax.annotate(f"Max: linha {max_row_text}",
                    xy=(x_max, y_max),
                    xytext=(10, 10), textcoords='offset points',
                    fontsize=8, color=color, fontweight='bold',
                    bbox=dict(facecolor='white', alpha=0.7, edgecolor=color),
                    arrowprops=dict(arrowstyle='->', color=color, lw=1.2))


# ======================= FUNÇÃO PARA EXTRAIR LABEL DO ARQUIVO =================

def label_from_path(path):
    """Gera um rótulo curto a partir do nome do arquivo (ex: 'dadosA1' -> 'A1')."""
    base = os.path.splitext(os.path.basename(path))[0]  # remove extensão
    # Tenta extrair algo como 'A1' se o nome for 'dadosA1'
    if 'dados' in base:
        return base.replace('dados', '')
    return base


# ======================= MAIN ================================================

if __name__ == "__main__":

    if function == 1:
        # Processa um único arquivo
        weights, averages, error_values, max_row_text = process_excel(excel_path_single)

        fig, ax = plt.subplots(figsize=(10, 8))
        plot_one_dataset(ax, weights, averages, error_values,
                         label="Medidas", color='teal', annotate_max=True)

        ax.set_xlabel("Massa (g)", fontsize=20)
        ax.set_ylabel("Mudança espectral média (GHz)", fontsize=20)
        ax.legend(fontsize=12)
        ax.grid(True, linestyle='--', alpha=0.5)

        # Salva na pasta "graphs" ao lado do arquivo Excel
        graphs_folder = os.path.join(os.path.dirname(excel_path_single), "graphs")
        os.makedirs(graphs_folder, exist_ok=True)
        output_graph = os.path.join(graphs_folder, image_name)
        plt.savefig(output_graph, dpi=300, bbox_inches='tight')
        plt.show()

        print(f"Graph saved at: {output_graph}")
        slope, intercept, r_value, _, _ = linregress(weights, averages)
        print(f"Linear regression: slope = {slope:.4f}, intercept = {intercept:.4f}, R² = {r_value**2:.4f}")

    elif function == 2:
        # Três conjuntos de dados no mesmo gráfico
        fig, ax = plt.subplots(figsize=(12, 9))

        # Cores para diferenciar os datasets
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c']  # azul, laranja, verde

        for fpath, color in zip(excel_paths_triple, colors):
            weights, averages, error_values, max_row_text = process_excel(fpath)
            label = label_from_path(fpath)
            plot_one_dataset(ax, weights, averages, error_values,
                             label=label, color=color, annotate_max=True)

        ax.set_xlabel("Massa (g)", fontsize=20)
        ax.set_ylabel("Mudança espectral média (GHz)", fontsize=20)
        ax.legend(fontsize=11, loc='best')
        ax.grid(True, linestyle='--', alpha=0.5)

        # Salva na pasta "graphs" ao lado do primeiro arquivo da lista
        first_dir = os.path.dirname(excel_paths_triple[0])
        graphs_folder = os.path.join(first_dir, "graphs")
        os.makedirs(graphs_folder, exist_ok=True)
        output_graph = os.path.join(graphs_folder, image_name)
        plt.savefig(output_graph, dpi=300, bbox_inches='tight')
        plt.show()

        print(f"Graph saved at: {output_graph}")
        # Exibe os parâmetros de regressão para cada conjunto
        for fpath in excel_paths_triple:
            weights, averages, _, _ = process_excel(fpath)
            slope, intercept, r_value, _, _ = linregress(weights, averages)
            label = label_from_path(fpath)
            print(f"{label}: slope={slope:.4f}, intercept={intercept:.4f}, R²={r_value**2:.4f}")

    else:
        print("Valor inválido para 'function'. Use 1 ou 2.")