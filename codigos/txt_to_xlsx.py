import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#modulo de expressões regulares que ajuda a encontrar padrões em strings
import re

#Global variables
expected_length = 27
desired_folder = "testes/silicone_smf_5pontos"
excel_filename = "media_dos_5pontos.xlsx"
num_tests = 5
ignore_2line = False



"""


                                    FUNÇÕES


"""




"""                                                            



                        FUNCIONALIDADE 1 PARA UMA MEDIÇÃO



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

    #cria um DataFrame do pandas com os dados
    df = pd.DataFrame(data)

    #caminho completo do arquivo excel
    result_excel = os.path.join(data_folder, filename)

    #salva o DataFrame em um arquivo excel, sem o índice
    df.to_excel(result_excel, index=False)

    print(f"✓ Dados salvos em: {result_excel}")

    return result_excel



def for_one_measurement(data_folder):
    """Processa medições únicas: carrega, valida e salva em Excel."""

    #chama as funções definidas acima
    weight_files = get_sorted_weight_files(data_folder)
    data, lengths = load_measurement_data(data_folder, weight_files)
    validate_measurement_lengths(lengths)
    save_data_to_excel(data, data_folder)


"""



             FUNCIONALIDADE 2 PARA MAIS MEDIÇÕES E APENAS 1 EXCEL COM A MÉDIA





"""



def get_sorted_weight_directories(data_folder):
    """Obtém e ordena numericamente as pastas de peso (terminadas em 'g')."""
    
    #d é cada item dentro da data_folder, ele percorre todas as pastas dentro de data_folder
    peso_dirs = [d for d in os.listdir(data_folder)
                #apenas se d for diretório e terminar com 'g'
                if os.path.isdir(os.path.join(data_folder, d))
                and d.endswith('g')]

    #ordena as pastas numericamente, removendo o 'g' e convertendo para int
    peso_dirs.sort(key=lambda x: int(x.replace('g', '')))
    
    return peso_dirs



def get_test_files_for_weight(peso_path, peso_dir):
    """Obtém lista de arquivos de teste para um peso específico.
    
    Espera arquivos nomeados como '1-100g.txt', '2-100g.txt', etc.
    """
    
    #lista vazia para armazenar os arquivos de teste encontrados
    test_files = []

    #percorre de 1 até num_tests (inclusive)
    for i in range(1, num_tests + 1):

        #nome do arquivo esperado
        file_name = f"{i}-{peso_dir}.txt"
        #caminho completo do arquivo
        file_path = os.path.join(peso_path, file_name)

        #se o arquivo existir, adiciona à lista
        if os.path.exists(file_path):
            test_files.append(file_path)
    
    return test_files



def read_and_prepare_test_values(test_files):
    """Lê múltiplos arquivos de teste e prepara valores para cálculo de média.
    
    Remove a segunda linha (índice 1) de cada arquivo se existir e retorna
    lista com valores de cada arquivo. Reutiliza read_measurement_file().
    """
    
    #lista para armazenar todos os valores lidos
    all_values = []
    for file_path in test_files:
        values = read_measurement_file(file_path)
        
        # Ignorar a segunda linha (índice 1) se existir e se a flag estiver ativada
        if len(values) > 1 and ignore_2line == True:
            values = values[:1] + values[2:]
            print(f"  - Ignorando segunda linha em {os.path.basename(file_path)}")
        
        #adiciona os valores lidos à lista principal
        all_values.append(values)

    return all_values



def calculate_padded_average(all_values):
    """Calcula média de valores com comprimentos diferentes usando padding com NaN.
    
    Encontra o tamanho máximo, faz padding com NaN e calcula média ignorando NaN.
    """
    
    #v percorre cada lista de valores e encontra o comprimento máximo
    max_length = max(len(v) for v in all_values)
    
    #lista vazia para armazenar valores com padding (NaN)
    all_values_padded = []

    #percorre a lista de todos os valores
    for values in all_values:
        #se alguma lista tiver o comprimento menor que o máximo
        if len(values) < max_length:
            #adiciona NaN até atingir o comprimento máximo
            values = values + [np.nan] * (max_length - len(values))
        #adiciona a lista (com padding) à nova lista
        all_values_padded.append(values)
    
    # Converter para array numpy para calcular média (ignora NaN)
    all_values_array = np.array(all_values_padded)

    #ignora NaN ao calcular a média e calcula-a coluna por coluna (axis=0)
    average = np.nanmean(all_values_array, axis=0)
    
    return average



def process_weight_data(peso_dir, peso_path, data):
    """Processa dados de um peso específico e adiciona ao dicionário data.
    
    Reutiliza as funções: get_test_files_for_weight(), read_and_prepare_test_values()
    e calculate_padded_average().
    """
    
    #lista de arquivos para um peso específico
    test_files = get_test_files_for_weight(peso_path, peso_dir)
    
    #se tiver algo na lista de arquivos
    if len(test_files) > 0:
        #lê e prepara os valores de todos os arquivos de teste
        all_values = read_and_prepare_test_values(test_files)
        #calcula a média com padding
        average = calculate_padded_average(all_values)
        
        #o dicionario data na posição peso_dir recebe a média calculada
        data[peso_dir] = average
        print(f"✓ Peso {peso_dir}: {len(test_files)} arquivos, {len(average)} linhas de média calculadas")
        return True
    else:
        print(f"✗ Peso {peso_dir}: nenhum arquivo encontrado")
        return False



def for_more_measurements(data_folder):
    """Processa múltiplas medições: ordena pastas, processa cada peso e salva em Excel.
    
    Reutiliza as funções: get_sorted_weight_directories(), process_weight_data()
    e save_data_to_excel() para criar um Excel com as médias de cada peso.
    """
    
    #se nao houver diretório, lança erro
    if not os.path.isdir(data_folder):
        raise FileNotFoundError(f"Pasta de pesos não encontrada: {data_folder}")
    
    #obtém e ordena as pastas de peso
    peso_dirs = get_sorted_weight_directories(data_folder)
    #dicionário vazio para armazenar os dados processados
    data = {}
    
    #processa cada pasta de peso
    for peso_dir in peso_dirs:
        #caminho completo da pasta de peso
        peso_path = os.path.join(data_folder, peso_dir)
        #chama a função para processar os dados daquele peso
        process_weight_data(peso_dir, peso_path, data)
    
    # Usar save_data_to_excel com filename customizado
    df = pd.DataFrame(data)
    result_excel = os.path.join(data_folder, excel_filename)
    #salva o DataFrame em um arquivo excel, sem o índice
    df.to_excel(result_excel, index=False)
    
    print(f"\n✓ Dados salvos em: {result_excel}")




"""



        FUNCIONALIDADE 3 PARA VÁRIAS MEDIÇÕES COM UMA PLANILHA PARA CADA PESO




"""


def read_test_files_into_dict(test_files):
    """Lê múltiplos arquivos de teste e retorna um dicionário com os dados.
    
    Responsabilidade: Ler os arquivos e organizar os dados em um dicionário.
    
    Args:
        test_files: Lista de caminhos completos dos arquivos a ler.
    
    Returns:
        Dicionário com os dados, onde a chave é o nome do arquivo sem extensão
        e o valor é a lista de valores lidos.
    """
    
    # Dicionário para armazenar os dados lidos de cada arquivo
    data = {}
    
    # Lê cada arquivo de teste e adiciona como coluna ao dicionário
    for file_path in test_files:
        # Lê os valores do arquivo
        values = read_measurement_file(file_path)
        
        # Nome da coluna: nome do arquivo sem extensão
        column_name = os.path.splitext(os.path.basename(file_path))[0]
        
        # Adiciona os valores como coluna
        data[column_name] = values
    
    return data



def save_weight_excel(peso_dir, peso_path, data):
    """Salva os dados de um peso específico em arquivo Excel.
    
    Responsabilidade: Converter dados em DataFrame e salvar em Excel.
    
    Args:
        peso_dir: Nome do peso (ex: "50g").
        peso_path: Caminho completo da pasta do peso.
        data: Dicionário com os dados a salvar.
    
    Returns:
        O caminho completo do arquivo Excel criado.
    """
    
    # Cria um DataFrame com os dados
    df = pd.DataFrame(data)
    
    # Nome do arquivo Excel (ex: "50g.xlsx")
    excel_filename = f"{peso_dir}.xlsx"
    result_excel = os.path.join(peso_path, excel_filename)
    
    # Salva o DataFrame em arquivo Excel
    df.to_excel(result_excel, index=False)
    
    print(f"✓ Peso {peso_dir}: {len(data)} colunas salvos em {excel_filename}")
    
    return result_excel



def process_weight_for_individual_file(peso_dir, peso_path):
    """Processa um peso específico: obtém, lê e salva seus dados em Excel.
    
    Responsabilidade: Orquestrar o processamento de um único peso.
    
    Reutiliza: get_test_files_for_weight(), read_test_files_into_dict() e save_weight_excel().
    
    Args:
        peso_dir: Nome do peso (ex: "50g").
        peso_path: Caminho completo da pasta do peso.
    
    Returns:
        True se processado com sucesso, False caso contrário.
    """
    
    # Obtém os arquivos de teste para este peso
    test_files = get_test_files_for_weight(peso_path, peso_dir)
    
    if len(test_files) > 0:
        # Lê os dados dos arquivos
        data = read_test_files_into_dict(test_files)
        
        # Salva em Excel
        save_weight_excel(peso_dir, peso_path, data)
        return True
    else:
        print(f"✗ Peso {peso_dir}: nenhum arquivo encontrado")
        return False



def for_each_weight_separate_file(data_folder):
    """Processa cada peso e cria uma planilha individual com os 5 arquivos de teste como colunas.
    
    Responsabilidade: Coordenar o processamento de todos os pesos.
    
    Para cada pasta de peso (ex: 50g, 75g), lê os 5 arquivos de teste e cria uma planilha
    individual contendo cada arquivo como uma coluna. A planilha é salva dentro da pasta do peso.
    
    Reutiliza: get_sorted_weight_directories() e process_weight_for_individual_file().
    """
    
    # Validação: se não houver diretório, lança erro
    if not os.path.isdir(data_folder):
        raise FileNotFoundError(f"Pasta de pesos não encontrada: {data_folder}")
    
    # Obtém e ordena as pastas de peso
    peso_dirs = get_sorted_weight_directories(data_folder)
    
    # Processa cada pasta de peso
    for peso_dir in peso_dirs:
        # Caminho completo da pasta de peso
        peso_path = os.path.join(data_folder, peso_dir)
        
        # Processa o peso
        process_weight_for_individual_file(peso_dir, peso_path)












"""


                                    MAIN



"""


if __name__ == "__main__":
    #pega o diretório atual do script
    current_folder = os.path.dirname(__file__)
    #sai do diretório atual e entra na pasta desejada
    data_folder = os.path.join(current_folder, "..", desired_folder)
    #pega o caminho absoluto da pasta de dados
    data_folder = os.path.abspath(data_folder)

    #chama função desejada para tratar os dados do momento

    """ 



          Escolha entre as funções disponíveis.




    """

    #for_one_measurement(data_folder)
    #for_more_measurements(data_folder)
    for_each_weight_separate_file(data_folder)