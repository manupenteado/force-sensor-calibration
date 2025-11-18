import os

pesos_folder = "/workspaces/force-sensor-calibration/testes/fixa_eva_10pontos/pesos"

peso_dirs = sorted([d for d in os.listdir(pesos_folder) if os.path.isdir(os.path.join(pesos_folder, d))], 
                   key=lambda x: int(x.replace('g', '')))

for peso_dir in peso_dirs:
    peso_path = os.path.join(pesos_folder, peso_dir)
    
    sizes = {}
    for i in range(1, 11):
        file_name = f"{peso_dir}-{i}"
        file_path = os.path.join(peso_path, file_name)
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                lines = len(f.readlines())
            sizes[file_name] = lines
    
    # Verificar se todos têm o mesmo tamanho
    unique_sizes = set(sizes.values())
    if len(unique_sizes) > 1:
        print(f"\n⚠ {peso_dir}: TAMANHOS DIFERENTES")
        for file, size in sorted(sizes.items()):
            print(f"  {file}: {size} linhas")
    else:
        print(f"✓ {peso_dir}: todos os {len(sizes)} arquivos têm {list(unique_sizes)[0]} linhas")
