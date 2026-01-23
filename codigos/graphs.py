import matplotlib.pyplot as plt
import pandas as pd
import os


# ============================================================================
#                         VARIÁVEIS GLOBAIS
# ============================================================================

# Caminho absoluto do script
PASTA_SCRIPT = os.path.dirname(__file__)

# FUNÇÃO PRINCIPAL: Plotar cada coluna do Excel em um gráfico separado
# Configurações para a função principal
EXCEL_PATH_PRINCIPAL = os.path.join(PASTA_SCRIPT, "..", "testes/silicone_cortado_1medida/result_silicone_smf.xlsx")
GRAPHS_FOLDER_PRINCIPAL = os.path.join(PASTA_SCRIPT, "..", "testes/silicone_cortado_1medida", "graphs")

# FUNÇÃO ADICIONAL: Plotar 3 colunas específicas no mesmo gráfico
# Configurações para a função adicional
EXCEL_PATH_ADICIONAL = os.path.join(PASTA_SCRIPT, "..", "testes/silicone_smf_5pontos/media_pesos_silicone_smf_com5pontos.xlsx")
GRAPHS_FOLDER_ADICIONAL = os.path.join(PASTA_SCRIPT, "..", "testes/silicone_smf_5pontos", "graphs")
COLUNAS_SELECIONADAS = ['50g', '199g', '400g']

# Configurações de estilo dos gráficos
FIGSIZE_INDIVIDUAL = (8, 4)
FIGSIZE_COMPARACAO = (10, 6)
CORES_COMPARACAO = ['teal', 'orange', 'red']
CORES_INDIVIDUAL = 'teal'
DPI = 300


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
    
    # Cria a pasta se não existir
    os.makedirs(graphs_folder, exist_ok=True)
    
    # Verifica se as colunas existem
    for col in columns:
        if col not in df.columns:
            print(f"Erro: coluna '{col}' não encontrada no Excel")
            return
    
    # Cria o gráfico
    plt.figure(figsize=FIGSIZE_COMPARACAO)
    
    for i, column in enumerate(columns):
        plt.plot(range(len(df[column])), df[column], color=CORES_COMPARACAO[i], label=column, linewidth=2)
    
    plt.title(f"Shift Measurements Comparison: {', '.join(columns)}")
    plt.xlabel("Measurement Index")
    plt.ylabel("Shift Value (Ghz)")
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    # Salva o gráfico
    filename = f"comparison_{'_'.join(columns)}_plot.png"
    exit_path = os.path.join(graphs_folder, filename)
    plt.savefig(exit_path, dpi=DPI, bbox_inches='tight')
    plt.close()
    
    print(f"Graph saved to {exit_path}")


# ============================================================================
#                         EXECUÇÃO
# ============================================================================

if __name__ == "__main__":
    # Executa função principal
    print("=" * 60)
    print("Plotando colunas individuais...")
    print("=" * 60)
    plotar_colunas_individuais(
        excel_path=os.path.abspath(EXCEL_PATH_PRINCIPAL),
        graphs_folder=os.path.abspath(GRAPHS_FOLDER_PRINCIPAL)
    )
    
    # Executa função adicional
    print("\n" + "=" * 60)
    print("Plotando colunas selecionadas...")
    print("=" * 60)
    plotar_colunas_selecionadas(
        excel_path=os.path.abspath(EXCEL_PATH_ADICIONAL),
        graphs_folder=os.path.abspath(GRAPHS_FOLDER_ADICIONAL),
        columns=COLUNAS_SELECIONADAS
    )


