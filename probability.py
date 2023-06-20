from collections import defaultdict
import math


def get_symbol_frequencies(text):
    # Obtener las frecuencias de ocurrencia de los símbolos en el texto
    frequencies = defaultdict(int)
    for symbol in text:
        frequencies[symbol] += 1
    return frequencies


def calculate_probabilities(symbol_frequencies):
    # Calcular las probabilidades de ocurrencia de cada símbolo
    total_symbols = sum(symbol_frequencies.values())
    probabilities = {}
    for symbol, frequency in symbol_frequencies.items():
        probabilities[symbol] = frequency / total_symbols
    return probabilities


def train_probabilistic_model(text):
    # Entrenar un modelo de aprendizaje utilizando las probabilidades obtenidas
    symbol_frequencies = get_symbol_frequencies(text)
    probabilities = calculate_probabilities(symbol_frequencies)
    return probabilities


def arithmetic_coding(text, probabilities):
    # Codificar el texto utilizando la codificación aritmética
    lower = 0.0
    upper = 1.0
    for symbol in text:
        symbol_probability = probabilities[symbol]
        range_size = upper - lower
        upper = lower + range_size * symbol_probability
        lower = lower + range_size * sum(probabilities[s] for s in probabilities if s < symbol)
    encoded_value = (lower + upper) / 2.0
    return encoded_value


def compress_text(text):
    # Comprimir el texto a una lista de probabilidades y un número decimal
    probabilities = train_probabilistic_model(text)
    encoded_value = arithmetic_coding(text, probabilities)
    compressed_data = {
        'probabilities': probabilities,
        'encoded_value': encoded_value
    }
    return compressed_data


def save_compressed_data(compressed_data, output_file):
    # Guardar los datos comprimidos en un archivo
    with open(output_file, 'w') as file:
        file.write('Probabilities:\n')
        for symbol, probability in compressed_data['probabilities'].items():
            file.write(f"{symbol}: {probability}\n")
        file.write('Encoded Value:\n')
        file.write(str(compressed_data['encoded_value']))

def read_input_text(file_path):
    # Leer el texto de entrada desde un archivo
    with open(file_path, 'r') as file:
        input_text = file.read()
    return input_text


# Obtener el texto de entrada desde un archivo
input_file = 'input.txt'
input_text = read_input_text(input_file)
print(f"Texto de entrada desde {input_file}: {input_text}")

compressed_data = compress_text(input_text)
output_file = 'compressed_data.txt'
save_compressed_data(compressed_data, output_file)
print(f"Datos comprimidos guardados en el archivo: {output_file}")
