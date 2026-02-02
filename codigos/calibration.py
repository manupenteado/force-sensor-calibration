import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np
from scipy.stats import linregress

script_folder = os.path.dirname(__file__)


number_of_points_analyzed = 5
excel_path = os.path.join(script_folder, "..", "testes/minimo_percebido/minimo_percebido.xlsx")
image_name = "minimo_percebido_relacao.png"
excel_path = os.path.abspath(excel_path)

df = pd.read_excel(excel_path)

weights = []
averages = []

for col in df.columns:
    weight = int(col.replace("g", ""))
    weights.append(weight)
    top = df[col].nlargest(number_of_points_analyzed)
    averages.append(top.mean())

weights, averages = zip(*sorted(zip(weights, averages)))

plt.figure(figsize=(10, 5))
plt.scatter(weights, averages, color='teal', s=100)
plt.plot(weights, averages, color='teal', linestyle='--', alpha=0.7)

slope, intercept, r_value, p_value, std_err = linregress(weights, averages)
regression_line = [slope * x + intercept for x in weights]
plt.plot(weights, regression_line, color='red', linestyle='-', linewidth=2, label=f"Linear Fit: y = {slope:.4f}x + {intercept:.4f}")
plt.legend()

plt.xlabel("Weight (g)")
plt.ylabel("Average Spectral Shift (GHz)")
plt.title("Calibration Curve: Average Spectral Shift vs Weight")
plt.grid(True, linestyle='--', alpha=0.5)

# Colocar a pasta de gráficos ao lado do arquivo Excel (diretório do Excel)
graphs_folder = os.path.join(os.path.dirname(excel_path), "graphs")
os.makedirs(graphs_folder, exist_ok=True)
output_graph = os.path.join(graphs_folder, image_name)
plt.savefig(output_graph, dpi=300, bbox_inches='tight')
plt.show()

print(f"Graph saved at: {output_graph}")
print(f"Linear regression: slope = {slope:.4f}, intercept = {intercept:.4f}")
