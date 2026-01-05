import os
import pandas as pd
import numpy as np
from scipy import stats

# Caminhos
script_folder = os.path.dirname(__file__)
excel_path = os.path.join(script_folder, "..", "testes", "silicone_smf_5pontos", "media_pesos_silicone_smf_com5pontos.xlsx")
excel_path = os.path.abspath(excel_path)
output_path = os.path.join(script_folder, "..", "testes", "silicone_smf_5pontos", "estatisticas_pesos.xlsx")

if not os.path.exists(excel_path):
    raise FileNotFoundError(f"Arquivo de médias não encontrado: {excel_path}")

# Ler planilha onde cada coluna é um peso (ex.: '100g') e cada linha é a média do experimento
df = pd.read_excel(excel_path)

# Número de medidas por coluna (deveria ser 1 se a planilha contém apenas médias; mas garantimos conteudo)
n = pd.DataFrame({"count": df.count()}).T

# Estatísticas solicitadas (exceto média)
std = df.std(ddof=1)
var = df.var(ddof=1)
sem = std / np.sqrt(df.count())
minimum = df.min()
maximum = df.max()
median = df.median()
q1 = df.quantile(0.25)
q3 = df.quantile(0.75)
iqr = q3 - q1
cv_pct = 100 * std / df.mean()
skew = df.skew()
kurt = df.kurtosis()

# Intervalo de confiança 95% (usando t de Student)
ci_lower = pd.Series(index=df.columns, dtype=float)
ci_upper = pd.Series(index=df.columns, dtype=float)
for col in df.columns:
    cnt = df[col].count()
    if cnt > 1:
        m = df[col].mean()
        s = df[col].std(ddof=1)
        sem_col = s / np.sqrt(cnt)
        tval = stats.t.ppf(0.975, df=cnt-1)
        ci_lower[col] = m - tval * sem_col
        ci_upper[col] = m + tval * sem_col
    else:
        ci_lower[col] = np.nan
        ci_upper[col] = np.nan

# Construir DataFrame de estatísticas
stats_df = pd.DataFrame({
    "count": df.count(),
    "std": std,
    "var": var,
    "sem": sem,
    "min": minimum,
    "max": maximum,
    "median": median,
    "q1": q1,
    "q3": q3,
    "IQR": iqr,
    "CV_%": cv_pct,
    "skew": skew,
    "kurtosis": kurt,
    "CI95_lower": ci_lower,
    "CI95_upper": ci_upper,
})

# Salvar
os.makedirs(os.path.dirname(output_path), exist_ok=True)
stats_df.to_excel(output_path)

# Impressão explicativa no terminal
explanations = {
    "std": "Desvio padrão: dispersão típica das medidas (mesma unidade dos dados).",
    "var": "Variância: dispersão média (unidade ao quadrado).",
    "sem": "Erro padrão da média (SEM): estimativa da incerteza da média (std/sqrt(n)).",
    "IQR": "IQR (Q3-Q1): intervalo interquartil, robusto a outliers.",
    "CV_%": "Coeficiente de variação (CV%): variabilidade relativa (std/mean * 100).",
    "skew": "Assimetria (skewness): se >0 distribuição tem cauda à direita.",
    "kurtosis": "Curtose: se alta, distribuição tem cauda mais pesada/valor extremo.",
    "CI95_lower": "Limite inferior do intervalo de confiança de 95% para a média.",
    "CI95_upper": "Limite superior do intervalo de confiança de 95% para a média.",
    "min": "Mínimo observado.",
    "max": "Máximo observado.",
    "median": "Mediana: valor central robusto.",
}

print('\n=== Estatísticas por peso (arquivo salvo em: {}) ===\n'.format(output_path))
for col in stats_df.columns:
    # print apenas colunas de interesse com explicação acima
    pass

# Mostrar por peso: cada métrica com explicação
for peso in stats_df.index:
    print(f"--- {peso} ---")
    print(f"Número de pontos: {int(stats_df.loc[peso,'count'])}")
    print(f"Desvio padrão (std): {stats_df.loc[peso,'std']:.6g} — {explanations['std']}")
    print(f"Variância (var): {stats_df.loc[peso,'var']:.6g} — {explanations['var']}")
    print(f"Erro padrão da média (sem): {stats_df.loc[peso,'sem']:.6g} — {explanations['sem']}")
    print(f"Coeficiente de variação (CV%): {stats_df.loc[peso,'CV_%']:.4f}% — {explanations['CV_%']}")
    print(f"Min / Max: {stats_df.loc[peso,'min']:.6g} / {stats_df.loc[peso,'max']:.6g} — {explanations['min']} / {explanations['max']}")
    print(f"Mediana: {stats_df.loc[peso,'median']:.6g} — {explanations['median']}")
    print(f"IQR: {stats_df.loc[peso,'IQR']:.6g} — {explanations['IQR']}")
    print(f"Skewness: {stats_df.loc[peso,'skew']:.6g} — {explanations['skew']}")
    print(f"Kurtosis: {stats_df.loc[peso,'kurtosis']:.6g} — {explanations['kurtosis']}")
    lower = stats_df.loc[peso,'CI95_lower']
    upper = stats_df.loc[peso,'CI95_upper']
    if not np.isnan(lower):
        print(f"CI95: [{lower:.6g}, {upper:.6g}] — intervalo de confiança de 95% para a média")
    else:
        print("CI95: n/a (poucos pontos)")
    print()

print('Arquivo de estatísticas gerado:', output_path)
