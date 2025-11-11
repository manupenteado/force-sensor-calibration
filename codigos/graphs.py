import matplotlib.pyplot as plt
import pandas as pd
import os

# Caminho absoluto do script
pasta_script = os.path.dirname(__file__)

# Caminho da planilha Excel (já dentro da pasta codigos)
excel_path = os.path.join(pasta_script, "..", "testes_pesos_manu_smf_com_eva/3_ponto/result_3_ponto.xlsx")
excel_path = os.path.abspath(excel_path)

# Lê a planilha
df = pd.read_excel(excel_path)

# Caminho absoluto da pasta de saída dos gráficos
graphs_folder = os.path.join(pasta_script, "..", "testes_pesos_manu_smf_com_eva/3_ponto", "graphs")
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
