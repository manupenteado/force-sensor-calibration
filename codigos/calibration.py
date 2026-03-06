import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np
from scipy.stats import linregress


# helper ---------------------------------------------------------------------

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

# -----------------------------------------------------------------------------

script_folder = os.path.dirname(__file__)


number_of_points_analyzed = 5
excel_path = os.path.join(script_folder, "..", "testes/silicone_smf_5pontos/dados.xlsx")
image_name = "media_spectral_shift_sacpt.png"
excel_path = os.path.abspath(excel_path)

# read the spreadsheet and remove any trailing error rows
raw_df = pd.read_excel(excel_path)
df, errors = strip_error_rows(raw_df)

weights = []
averages = []
error_values = []  # will mirror weights/averages if errors were found

for idx, col in enumerate(df.columns):
    # weight is stored in the column header e.g. "100g"
    weight = int(col.replace("g", ""))
    weights.append(weight)

    # convert the column to numeric, dropping any non-numeric (e.g. NaN)
    series = pd.to_numeric(df[col], errors="coerce")
    top = series.nlargest(number_of_points_analyzed)
    averages.append(top.mean())

    # keep track of the corresponding error if available
    if errors is not None:
        error_values.append(errors[idx])

# sort by weight to guarantee monotonic x-axis
if errors is not None:
    weights, averages, error_values = zip(*sorted(zip(weights, averages, error_values)))
else:
    weights, averages = zip(*sorted(zip(weights, averages)))

plt.figure(figsize=(10, 5))
# always draw the scatter so points are clearly visible
plt.scatter(weights, averages, color='teal', s=100)
# if we have error values, overlay error bars
if errors is not None:
    plt.errorbar(weights, averages, yerr=error_values,
                 fmt='none', ecolor='gray', capsize=5, alpha=0.7)

# draw connecting line between the means
plt.plot(weights, averages, color='teal', linestyle='--', alpha=0.7)

slope, intercept, r_value, p_value, std_err = linregress(weights, averages)

# coeficiente de determinação
r_squared = r_value ** 2

regression_line = [slope * x + intercept for x in weights]
plt.plot(weights, regression_line, color='red', linestyle='-', linewidth=2,
         label=f"Fit linear: y = {slope:.4f}x + {intercept:.4f} (R²={r_squared:.4f})")
plt.legend()

plt.xlabel("Peso (g)")
plt.ylabel("Mudança espectral média (GHz)")
plt.title("Curva de Calibração: Mudança Espectral Média vs Peso")
plt.grid(True, linestyle='--', alpha=0.5)

# Colocar a pasta de gráficos ao lado do arquivo Excel (diretório do Excel)
graphs_folder = os.path.join(os.path.dirname(excel_path), "graphs")
os.makedirs(graphs_folder, exist_ok=True)
output_graph = os.path.join(graphs_folder, image_name)
plt.savefig(output_graph, dpi=300, bbox_inches='tight')
plt.show()

print(f"Graph saved at: {output_graph}")
print(f"Linear regression: slope = {slope:.4f}, intercept = {intercept:.4f}")
