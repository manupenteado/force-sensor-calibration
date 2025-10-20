import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#refazer 175g

current_folder = os.path.dirname(__file__)
data_folder = os.path.join(current_folder, "..", "testes_pesos_manu")
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
    print(lenghts)

    

print(lenghts)
df = pd.DataFrame(data)
result_excel = os.path.join(current_folder, "result.xlsx")
df.to_excel(result_excel, index=False)

print (f"Data saved to {result_excel}")

