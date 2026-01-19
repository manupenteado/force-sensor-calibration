import matplotlib.pyplot as plt
import pandas as pd
import os


# Caminho absoluto do script
pasta_script = os.path.dirname(__file__)

# Caminho da planilha Excel (já dentro da pasta codigos)
#
#                                                             MUDAR
#
excel_path = os.path.join(pasta_script, "..", "testes/silicone_cortado_1medida/result_silicone_smf.xlsx")
excel_path = os.path.abspath(excel_path)

# Lê a planilha
df = pd.read_excel(excel_path)

# Caminho absoluto da pasta de saída dos gráficos

#
#                                                              MUDAR
#
graphs_folder = os.path.join(pasta_script, "..", "testes/silicone_cortado_1medida", "graphs")
graphs_folder = os.path.abspath(graphs_folder)
os.makedirs(graphs_folder, exist_ok=True)

# Criação dos gráficos
for column in df.columns:
    plt.figure(figsize=(8, 4))
    plt.plot(range(len(df[column])), df[column], color='teal')
    plt.title(f"Shift Measurements for {column} ")
    plt.xlabel("Measurement Index")
    plt.ylabel("Shift Value (Ghz)")
    plt.grid(True)

    # Caminho final do arquivo
    exit_path = os.path.join(graphs_folder, f"{column}_shift_plot.png")
    plt.savefig(exit_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Graph saved to {exit_path}")



"""


def plot_selected_columns(excel_path, graphs_folder, columns):
    """
    Plota 3 colunas selecionadas do Excel no mesmo gráfico.
    
    Parâmetros:
    - excel_path: caminho do arquivo Excel
    - graphs_folder: pasta onde salvar o gráfico
    - columns: lista com 3 nomes de colunas (ex: ['50g', '200g', '400g'])
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
    plt.figure(figsize=(10, 6))
    
    colors = ['teal', 'orange', 'red']
    for i, column in enumerate(columns):
        plt.plot(range(len(df[column])), df[column], color=colors[i], label=column, linewidth=2)
    
    plt.title(f"Shift Measurements Comparison: {', '.join(columns)}")
    plt.xlabel("Measurement Index")
    plt.ylabel("Shift Value (Ghz)")
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    # Salva o gráfico
    filename = f"comparison_{'_'.join(columns)}_plot.png"
    exit_path = os.path.join(graphs_folder, filename)
    plt.savefig(exit_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Graph saved to {exit_path}")

pasta_script = os.path.dirname(__file__)
excel_path = os.path.join(pasta_script, "..", "testes/silicone_smf_5pontos/media_pesos_silicone_smf_com5pontos.xlsx")
excel_path = os.path.abspath(excel_path)
graphs_folder = os.path.join(pasta_script, "..", "testes/silicone_smf_5pontos", "graphs")
graphs_folder = os.path.abspath(graphs_folder)


plot_selected_columns(
    excel_path=excel_path,
    graphs_folder=graphs_folder,
    columns=['50g', '199g', '400g']
)

"""

