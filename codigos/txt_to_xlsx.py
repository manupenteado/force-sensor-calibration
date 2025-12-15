import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

"""current_folder = os.path.dirname(__file__)
data_folder = os.path.join(current_folder, "..", "testes/silicone_smf")
data_folder = os.path.abspath(data_folder)

weight_files = [f for f in os.listdir(data_folder) if f.endswith('txt')]

data = {}
lenghts = {}

for file in weight_files:
    file_path = os.path.join(data_folder, file)

    with open(file_path, "r", encoding='utf-8') as f:
        lines = f.readlines()
        values = [float(l.strip()) for l in lines]

    column_name = os.path.splitext(file)[0]
    data[column_name] = values
    lenghts[column_name] = len(values)
    if (lenghts [column_name] != 289):
        print(lenghts)

    

print(lenghts)
df = pd.DataFrame(data)
result_excel = os.path.join(data_folder, "result_52g.xlsx")
df.to_excel(result_excel, index=False)

print (f"Data saved to {result_excel}")"""

# Nova função para calcular médias dos 10 testes por peso
current_folder = os.path.dirname(__file__)
pesos_folder = os.path.join(current_folder, "..", "testes/")
pesos_folder = os.path.abspath(pesos_folder)

# Obter lista de pastas de pesos e ordená-las numericamente
peso_dirs = [d for d in os.listdir(pesos_folder) if os.path.isdir(os.path.join(pesos_folder, d)) and d.endswith('g')]
# Ordena por número (extrai o número do começo do nome)
peso_dirs.sort(key=lambda x: int(x.replace('g', '')))

data = {}

for peso_dir in peso_dirs:
    peso_path = os.path.join(pesos_folder, peso_dir)
    
    # Encontrar todos os arquivos de teste para este peso (XXg-1 até XXg-10)
    test_files = []
    for i in range(1, 11):
        file_name = f"{peso_dir}-{i}"
        file_path = os.path.join(peso_path, file_name)
        if os.path.exists(file_path):
            test_files.append(file_path)
    
    if len(test_files) > 0:
        # Ler todos os arquivos
        all_values = []
        for file_path in test_files:
            with open(file_path, "r", encoding='utf-8') as f:
                lines = f.readlines()
                values = [float(l.strip()) for l in lines]
                # Ignorar a segunda linha (índice 1)
                values = values[:1] + values[2:]
                all_values.append(values)
        
        # Encontrar o tamanho máximo para padding
        max_length = max(len(v) for v in all_values)
        
        # Padding de arrays com NaN para torná-los do mesmo tamanho
        all_values_padded = []
        for values in all_values:
            if len(values) < max_length:
                values = values + [np.nan] * (max_length - len(values))
            all_values_padded.append(values)
        
        # Converter para array numpy para calcular média (ignora NaN)
        all_values_array = np.array(all_values_padded)
        average = np.nanmean(all_values_array, axis=0)
        
        # Adicionar ao dicionário de dados
        data[peso_dir] = average
        print(f"✓ Peso {peso_dir}: {len(test_files)} arquivos, {len(average)} linhas de média calculadas")
    else:
        print(f"✗ Peso {peso_dir}: nenhum arquivo encontrado")

# Criar DataFrame e salvar em Excel
df = pd.DataFrame(data)
result_excel = os.path.join(pesos_folder, "media_pesos_sem_2linha.xlsx")
df.to_excel(result_excel, index=False)

print(f"\n✓ Dados salvos em: {result_excel}")



