import matplotlib.pyplot as plt
import pandas as pd
import os
import numpy as np


def strip_error_rows(df: pd.DataFrame):
    """Remove rows de erro se a planilha os contém.

    Se a penúltima linha contiver "eror" em todas as colunas, assumimos que a
    última linha contém valores de erro por coluna. Retornamos o dataframe sem
    essas duas últimas linhas e uma lista de erros.
    """
    errors = None
    if df.shape[0] >= 2:
        second_last = df.iloc[-2].astype(str).str.lower()
        if (second_last == "eror").all():
            errors = pd.to_numeric(df.iloc[-1], errors="coerce").tolist()
            df = df.iloc[:-2]
    return df, errors


# ============================================================================
#                         VARIÁVEIS GLOBAIS
# ============================================================================

# Caminho absoluto do script
PASTA_SCRIPT = os.path.dirname(__file__)

# FUNÇÃO PRINCIPAL: Plotar cada coluna do Excel em um gráfico separado
# Configurações para a função principal
EXCEL_PATH_PRINCIPAL = os.path.join(PASTA_SCRIPT, "..", "testes/peca_circular_madeira/matriz/C3 - 5/dadosC3.xlsx")
GRAPHS_FOLDER_PRINCIPAL = os.path.join(PASTA_SCRIPT, "..", "testes/peca_circular_madeira/matriz/C3 - 5", "graphs")

# FUNÇÃO ADICIONAL: Plotar 3 colunas específicas no mesmo gráfico
# Configurações para a função adicional
EXCEL_PATH_ADICIONAL = os.path.join(PASTA_SCRIPT, "..", "testes/2 pesos ao mesmo tempo/400g e 300g/400g_e_300g.xlsx")
GRAPHS_FOLDER_ADICIONAL = os.path.join(PASTA_SCRIPT, "..", "testes/2 pesos ao mesmo tempo/400g e 300g", "graphs")
COLUNAS_SELECIONADAS = ['350g', '400g', '600g']

# Configurações de estilo dos gráficos
FIGSIZE_INDIVIDUAL = (8, 4)
FIGSIZE_COMPARACAO = (10, 6)
CORES_COMPARACAO = ['teal', 'orange', 'red']
CORES_INDIVIDUAL = 'teal'
DPI = 300
X_SCALE_FACTOR = 0.65
ROWS_TO_DROP_INITIAL = 2
AXIS_LABEL_FONTSIZE = 16
AXIS_TICK_FONTSIZE = 14

# Configurações da função de matriz 3x3
ROWS_TO_DROP_INITIAL = 3
MATRIX_TITLE_FONTSIZE = 30
MATRIX_LINEWIDTH = 2.2


# ============================================================================
#                      FUNÇÃO PRINCIPAL
# ============================================================================

def plotar_colunas_individuais(excel_path, graphs_folder):
    """
    Plota cada coluna do Excel em um gráfico separado.
    
    Parâmetros:
    - excel_path: caminho do arquivo Excel
    - graphs_folder: pasta onde salvar os gráficos
    """
    # Lê a planilha
    df = pd.read_excel(excel_path)
    df, errors = strip_error_rows(df)
    # Cria a pasta se não existir
    os.makedirs(graphs_folder, exist_ok=True)
    
    # Criação dos gráficos
    for column in df.columns:
        plt.figure(figsize=FIGSIZE_INDIVIDUAL)
        plt.plot(range(len(df[column])), df[column], color=CORES_INDIVIDUAL)
        plt.title(f"Shift Measurements for {column} ")
        plt.xlabel("Measurement Index")
        plt.ylabel("Shift Value (Ghz)")
        plt.grid(True)

        # Caminho final do arquivo
        exit_path = os.path.join(graphs_folder, f"{column}_shift_plot.png")
        plt.savefig(exit_path, dpi=DPI, bbox_inches='tight')
        plt.close()
        print(f"Graph saved to {exit_path}")


# ============================================================================
#                      FUNÇÃO ADICIONAL
# ============================================================================

def plotar_colunas_selecionadas(excel_path, graphs_folder, columns):
    """
    Plota colunas selecionadas do Excel no mesmo gráfico.
    
    Parâmetros:
    - excel_path: caminho do arquivo Excel
    - graphs_folder: pasta onde salvar o gráfico
    - columns: lista com nomes de colunas (ex: ['50g', '200g', '400g'])
    """
    # Lê a planilha
    df = pd.read_excel(excel_path)

    # Retira possíveis linhas de erro ("eror" + valores de erro na última linha)
    df, errors = strip_error_rows(df)
    error_map = {}
    if errors is not None:
        # Mapear coluna -> valor de erro (mesmo valor aplicado a todos os pontos da coluna)
        error_map = dict(zip(df.columns, errors))

    # Cria a pasta se não existir
    os.makedirs(graphs_folder, exist_ok=True)

    # Verifica se as colunas existem
    for col in columns:
        if col not in df.columns:
            print(f"Erro: coluna '{col}' não encontrada no Excel")
            return
    
    # Cria o gráfico
    plt.figure(figsize=(10, 8))
    
    # cada índice corresponde a 2.6 mm; geramos um array de floats e
    # definimos os ticks manualmente em 10, 20, …, 70 mm
    import numpy as np

    for i, column in enumerate(columns):
        x = np.arange(len(df[column])) * 2.6               # 0, 2.6, 5.2, … (mm)
        y = df[column]

        plt.plot(x, y,
                 color=CORES_COMPARACAO[i],
                 label=column, linewidth=2)
        plt.scatter(x, y,
                    color=CORES_COMPARACAO[i],
                    s=20, alpha=0.6)

        # Se houver valores de erro declarados na planilha, adiciona barras de erro
        # if errors is not None:
        #     err_value = error_map.get(column)
        #     if pd.notna(err_value):
        #         plt.errorbar(x, y,
        #                      yerr=err_value,
        #                      fmt='none',
        #                      ecolor=CORES_COMPARACAO[i],
        #                      capsize=3,
        #                      alpha=0.4)

    # limites e rótulos do eixo x em milímetros
    plt.xlim(5, 70)  # começa em 5 mm conforme solicitado
    plt.xticks([10, 20, 30, 40, 50, 60, 70])
    
    #plt.title(f"Comparação das medidas: {', '.join(columns)}")
    plt.xlabel("Comprimento da fibra (mm)", fontsize=20)
    plt.ylabel("Mudança espectral (GHz)", fontsize=20)
    plt.grid(True, alpha=0.3)
    plt.legend(fontsize=16)
    
    # Salva o gráfico
    filename = f"comparacao_{'_'.join(columns)}_plot.png"
    exit_path = os.path.join(graphs_folder, filename)
    plt.savefig(exit_path, dpi=DPI, bbox_inches='tight')
    plt.close()
    
    print(f"Graph saved to {exit_path}")


# ============================================================================
#                    FUNÇÕES DE MÉDIA POR LINHA
# ============================================================================

def compute_row_means_from_excel(excel_path, columns=None, drop_first_row=True, rows_to_drop_initial=ROWS_TO_DROP_INITIAL):
    """
    Lê um Excel e retorna a Series com a média linha-a-linha das colunas

    - excel_path: caminho do arquivo Excel
    - columns: lista de colunas a considerar (None = todas as colunas)
    - drop_first_row: se True, remove a primeira linha de dados (não o cabeçalho)

    Retorna uma `pd.Series` contendo a média por linha (índice 0..N-1).
    """
    df = pd.read_excel(excel_path)
    df, errors = strip_error_rows(df)

    if drop_first_row and df.shape[0] > 0:
        if rows_to_drop_initial > 0:
            df = df.iloc[rows_to_drop_initial:].reset_index(drop=True)
        else:
            df = df.reset_index(drop=True)

    if columns is None:
        cols = list(df.columns)
    else:
        cols = list(columns)

    missing = [c for c in cols if c not in df.columns]
    if missing:
        raise ValueError(f"Colunas não encontradas no Excel: {missing}")

    # Converte valores com vírgula decimal para ponto e força tipo numérico
    # pandas 3.x pode não ter `applymap`; usar operações vetorizadas
    df_selected = df[cols].astype(str).replace(',', '.', regex=True)
    df_numeric = df_selected.apply(lambda s: pd.to_numeric(s, errors='coerce'))

    # Calcular média linha-a-linha (ignora NaNs nas colunas)
    means = df_numeric.mean(axis=1)
    return means


def plot_row_means(excel_path, graphs_folder, columns=None, drop_first_row=True, filename=None, rows_to_drop_initial=ROWS_TO_DROP_INITIAL):
    """
    Gera e salva um gráfico da média linha-a-linha.

    - excel_path: caminho do arquivo Excel
    - graphs_folder: pasta onde salvar o gráfico
    - columns: lista de colunas a considerar (None = todas)
    - drop_first_row: remover a primeira linha de dados
    - filename: nome do arquivo de saída (se None, usa 'row_means_plot.png')

    Retorna o vetor numpy com as médias (eixo Y).
    """
    means = compute_row_means_from_excel(
        excel_path,
        columns=columns,
        drop_first_row=drop_first_row,
        rows_to_drop_initial=rows_to_drop_initial,
    )
    y = means.values
    x = np.arange(1, len(y) + 1) * X_SCALE_FACTOR

    plt.figure(figsize=FIGSIZE_INDIVIDUAL)
    plt.plot(x, y, marker='o', color=CORES_INDIVIDUAL)
    plt.scatter(x, y, color=CORES_INDIVIDUAL, s=20, alpha=0.7)
    plt.xlabel("Optical fiber length (mm)", fontsize=AXIS_LABEL_FONTSIZE)
    plt.ylabel("Average spectral shift (GHz)", fontsize=AXIS_LABEL_FONTSIZE)
    plt.xticks(fontsize=AXIS_TICK_FONTSIZE)
    plt.yticks(fontsize=AXIS_TICK_FONTSIZE)
    plt.grid(True)

    os.makedirs(graphs_folder, exist_ok=True)
    if filename is None:
        filename = "row_means_plot.png"
    exit_path = os.path.join(graphs_folder, filename)
    plt.savefig(exit_path, dpi=DPI, bbox_inches='tight')
    plt.close()
    print(f"Graph saved to {exit_path}")

    return y


# ============================================================================
#                    FUNÇÃO: MATRIZ 3x3 COM COLUNA 400g
# ============================================================================

def plotar_matriz_3x3_400g():
    """
    Cria uma figura com 9 subplots em uma matriz 3x3, cada um contendo
    a curva da coluna "400g" dos 9 arquivos especificados.
    
    Organização:
    - Linha 1: A1, B1, C1
    - Linha 2: A2, B2, C2
    - Linha 3: A3, B3, C3
    
    Sem eixos x/y visíveis, sem barras de erro, sem legenda.
    """
    
    # Lista de arquivos e labels na ordem desejada (por linha)
    arquivos_config = [
        # Linha 1: A1, B1, C1
        (os.path.join(PASTA_SCRIPT, "..", "testes/peca_circular_madeira/matriz/A1 - 5/dadosA1.xlsx"), "A1"),
        (os.path.join(PASTA_SCRIPT, "..", "testes/peca_circular_madeira/matriz/B1 - 5/dadosB1.xlsx"), "B1"),
        (os.path.join(PASTA_SCRIPT, "..", "testes/peca_circular_madeira/matriz/C1 - 5/dadosC1.xlsx"), "C1"),
        # Linha 2: A2, B2, C2
        (os.path.join(PASTA_SCRIPT, "..", "testes/peca_circular_madeira/matriz/A2 - 5/dadosA2.xlsx"), "A2"),
        (os.path.join(PASTA_SCRIPT, "..", "testes/peca_circular_madeira/matriz/B2 - 5/dadosB2.xlsx"), "B2"),
        (os.path.join(PASTA_SCRIPT, "..", "testes/peca_circular_madeira/matriz/C2 - 5/dadosC2.xlsx"), "C2"),
        # Linha 3: A3, B3, C3
        (os.path.join(PASTA_SCRIPT, "..", "testes/peca_circular_madeira/matriz/A3 - 5/dadosA3.xlsx"), "A3"),
        (os.path.join(PASTA_SCRIPT, "..", "testes/peca_circular_madeira/matriz/B3 - 5/dadosB3.xlsx"), "B3"),
        (os.path.join(PASTA_SCRIPT, "..", "testes/peca_circular_madeira/matriz/C3 - 5/dadosC3.xlsx"), "C3"),
    ]
    
    # Criar figura com 9 subplots em matriz 3x3
    fig, axes = plt.subplots(3, 3, figsize=(15, 12))
    axes = axes.flatten()  # Achata a matriz de axes para iteração fácil
    
    # Iterar sobre os arquivos e criar os plots
    for idx, (excel_path, label) in enumerate(arquivos_config):
        ax = axes[idx]
        abs_excel = os.path.abspath(excel_path)
        
        if os.path.exists(abs_excel):
            try:
                # Ler planilha
                df = pd.read_excel(abs_excel)
                df, errors = strip_error_rows(df)
                
                # Extrair coluna "400g"
                if "400g" in df.columns:
                    data_series = df["400g"].iloc[ROWS_TO_DROP_INITIAL:]
                    y = data_series.values
                    x = np.arange(len(y))
                    
                    # Plotar no subplot
                    ax.plot(x, y, color=CORES_INDIVIDUAL, linewidth=MATRIX_LINEWIDTH)
                    ax.set_title(label, fontsize=MATRIX_TITLE_FONTSIZE, fontweight='bold')
                    ax.set_facecolor('white')
                    # Remover eixos por enquanto
                    ax.set_xticks([])
                    ax.set_yticks([])
                    ax.spines['top'].set_visible(False)
                    ax.spines['right'].set_visible(False)
                    ax.spines['bottom'].set_visible(False)
                    ax.spines['left'].set_visible(False)
                else:
                    ax.text(0.5, 0.5, f"Coluna '400g'\nnão encontrada", 
                            ha='center', va='center', transform=ax.transAxes)
                    ax.set_title(label, fontsize=MATRIX_TITLE_FONTSIZE, fontweight='bold')
            except Exception as e:
                ax.text(0.5, 0.5, f"Erro ao ler\n{label}", 
                        ha='center', va='center', transform=ax.transAxes)
                ax.set_title(label, fontsize=MATRIX_TITLE_FONTSIZE, fontweight='bold')
                print(f"Erro ao processar {label}: {e}")
        else:
            ax.text(0.5, 0.5, f"Arquivo não encontrado\n{label}", 
                    ha='center', va='center', transform=ax.transAxes)
            ax.set_title(label, fontsize=MATRIX_TITLE_FONTSIZE, fontweight='bold')
            print(f"Arquivo não encontrado: {abs_excel}")
    
    # Ajustar layout
    plt.tight_layout()
    
    # Salvar figura
    graphs_folder = os.path.join(PASTA_SCRIPT, "..", "testes/peca_circular_madeira/matriz", "graphs")
    os.makedirs(graphs_folder, exist_ok=True)
    output_path = os.path.join(graphs_folder, "matriz_3x3_400g.png")
    plt.savefig(output_path, dpi=DPI, bbox_inches='tight')
    plt.close()
    
    print(f"Matriz 3x3 salva em: {output_path}")


# ============================================================================
#                         EXECUÇÃO
# ============================================================================

if __name__ == "__main__":

    
    # Chama a função que plota a média linha-a-linha e salva o PNG na
    # mesma pasta onde está o arquivo Excel (se o arquivo existir).
    abs_excel = os.path.abspath(EXCEL_PATH_ADICIONAL)
    excel_folder = os.path.dirname(abs_excel)

    print("\n" + "=" * 60)
    print("Plotando média linha-a-linha (row means)...")
    print("=" * 60)

    if os.path.exists(abs_excel):
        try:
            y = plot_row_means(
                excel_path=abs_excel,
                graphs_folder=excel_folder,
                columns=None,  # None = usa todas as colunas do arquivo
                drop_first_row=True,
                filename=None  # usar nome padrão
            )
            print(f"Row means vector length: {len(y)}")
        except Exception as e:
            print(f"Erro ao gerar gráfico de médias: {e}")
    else:
        print(f"Arquivo Excel não encontrado: {abs_excel}")

        """
    
    # Plotar matriz 3x3 com coluna 400g
    print("\n" + "=" * 60)
    print("Plotando matriz 3x3 com coluna 400g...")
    print("=" * 60)
    try:
        plotar_matriz_3x3_400g()
    except Exception as e:
        print(f"Erro ao gerar matriz 3x3: {e}")

"""
