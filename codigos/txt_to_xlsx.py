import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#modulo de expressões regulares que ajuda a encontrar padrões em strings
import re

expected_length = 27



"""


                                    FUNÇÕES


"""



def get_sorted_weight_files(data_folder):
    """Obtém lista de arquivos .txt e os ordena peso"""
    
    #função sorted ordena uma lista
    weight_files = sorted( 
        #for f in f percorre todos os arquivos na pasta data_folder 
        #endswith filtra apenas arquivos que terminam com .txt
        [f for f in os.listdir(data_folder) if f.endswith('.txt')],
        #ordena os arquivos pelo número presente no nome do arquivo
        #x é o nome do arquivo, int(re.search procura o numero
        #\d significa um único dígito, só que "\" em python pode ter varios significados
        #então é necessário usar o 'r' antes que significa raw string, ou seja, a string é interpretada literalmente como \d, sem significados da linguagem
        #o + significa que pode ser um ou mais digitos, e group() retorna o valor encontrado
        key = lambda x: int(re.search(r'\d+', x).group())
    )
    return weight_files



def read_measurement_file(file_path):
    """Lê um arquivo de medição e retorna os valores como lista de floats."""

    #abre o arquivo, "r" lê, encoding utf-8 para ler caracteres especiais
    #f é o arquivo aberto e quando acabar ele fecha automaticamente
    with open(file_path, "r", encoding='utf-8') as f:

        #lê todas as linhas do arquivo e armazena em uma lista chamada lines
        lines = f.readlines()

        #for l in lines percorre cada linha da lista lines
        #l.strip() remove espaços em branco e \n
        #converte a string pra float e armazena na lista values
        values = [float(l.strip()) for l in lines]

    return values



def load_measurement_data(data_folder, weight_files):
    """Carrega dados de todos os arquivos e retorna dicionário de dados e comprimentos."""

    #dois dicionários vazios
    data = {}
    lengths = {}

    #percorre cada arquivo da lista weight_files
    for file in weight_files:

        #junta o caminho da pasta com o nome do arquivo para pegar o caminho completo
        file_path = os.path.join(data_folder, file)

        #lê os valores do arquivo com a função read_measurement_file e o armazena em uma lista chamada values
        values = read_measurement_file(file_path)
        
        # column name é o nome do arquivo sem a extensão (o 0 significa pegar a primeira parte do split)
        column_name = os.path.splitext(file)[0]

        #data na posição column_name recebe a lista de valores
        data[column_name] = values

        #lengths na posição column_name recebe o comprimento da lista de valores
        lengths[column_name] = len(values)

    return data, lengths



def validate_measurement_lengths(lengths):
    """Valida se todos os comprimentos coincidem com o esperado."""

    #vai pegar a quantidade de valores em cada medição e verificar se é igual ao esperado
    #lenght.items() retorna uma lista de tuplas (chave, valor) do dicionário lengths
    #k é a chave (nome do arquivo) e v é o valor (comprimento da lista)
    #as chaves criam um novo dicionário apenas com os comprimentos inválidos
    invalid_lengths = {k: v for k, v in lengths.items() if v != expected_length}
    
    #se comprimento invalido tiver algo, imprime os avisos
    if invalid_lengths:
        print("⚠ Avisos de comprimento:")
        print(invalid_lengths)
    
    #retorna True se todos os comprimentos forem válidos
    #retorna False se houver comprimentos inválidos
    return len(invalid_lengths) == 0


def save_data_to_excel(data, data_folder, filename="result_silicone_smf.xlsx"):
    """Salva dados em arquivo Excel."""
    df = pd.DataFrame(data)
    result_excel = os.path.join(data_folder, filename)
    df.to_excel(result_excel, index=False)
    print(f"✓ Dados salvos em: {result_excel}")
    return result_excel


def for_one_measurement(data_folder):
    """Processa medições únicas: carrega, valida e salva em Excel."""
    weight_files = get_sorted_weight_files(data_folder)
    data, lengths = load_measurement_data(data_folder, weight_files)
    
    print(f"Comprimentos das medições: {lengths}")
    validate_measurement_lengths(lengths)
    
    save_data_to_excel(data, data_folder)


def for_more_measurement(data_folder):

    if not os.path.isdir(data_folder):
        raise FileNotFoundError(f"Pasta de pesos não encontrada: {data_folder}")

    # Obter lista de pastas de pesos e ordená-las numericamente
    peso_dirs = [d for d in os.listdir(data_folder) if os.path.isdir(os.path.join(data_folder, d)) and d.endswith('g')]
    peso_dirs.sort(key=lambda x: int(x.replace('g', '')))

    data = {}

    for peso_dir in peso_dirs:
        peso_path = os.path.join(data_folder, peso_dir)
        
        # Espera-se arquivos nomeados como '1-100g.txt', '2-100g.txt', ...
        test_files = []
        for i in range(1, 6):
            file_name = f"{i}-{peso_dir}.txt"
            file_path = os.path.join(peso_path, file_name)
            if os.path.exists(file_path):
                test_files.append(file_path)

        if len(test_files) > 0:
            # Ler todos os arquivos
            all_values = []
            for file_path in test_files:
                with open(file_path, "r", encoding='utf-8') as f:
                    lines = [l.strip() for l in f.readlines() if l.strip() != ""]
                    # Ignorar a segunda linha (índice 1) se existir
                    if len(lines) > 1:
                        lines = lines[:1] + lines[2:]
                    values = [float(l) for l in lines]
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
    result_excel = os.path.join(data_folder, "media_pesos_silicone_smf_com5pontos.xlsx")
    df.to_excel(result_excel, index=False)

    print(f"\n✓ Dados salvos em: {result_excel}")




current_folder = os.path.dirname(__file__)
data_folder = os.path.join(current_folder, "..", "testes/silicone_cortado_1medida")
data_folder = os.path.abspath(data_folder)

for_one_measurement(data_folder)