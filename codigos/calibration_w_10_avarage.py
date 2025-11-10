import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np
from scipy.stats import linregress

script_folder = os.path.dirname(__file__)
excel_path = os.path.join(script_folder, "result.xlsx")
excel_path = os.path.abspath(excel_path)

df = pd.read_excel(excel_path)

weights = []
averages = []

for col in df.columns:
    weight = int(col.replace("g", ""))
    weights.append(weight)
    top3 = df[col].nlargest(3)
    averages.append(top3.mean())

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

graphs_folder = os.path.join(script_folder, "graphs")
os.makedirs(graphs_folder, exist_ok=True)
output_graph = os.path.join(graphs_folder, "media_top3.png")
plt.savefig(output_graph, dpi=300, bbox_inches='tight')
plt.show()

print(f"Graph saved at: {output_graph}")
print(f"Linear regression: slope = {slope:.4f}, intercept = {intercept:.4f}")
