import heapq
import os


class HuffmanNode:
    def __init__(self, symbol=None, frequency=None):
        self.symbol = symbol
        self.frequency = frequency
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.frequency < other.frequency


def get_symbol_frequencies(file_path):
    # Obtener las frecuencias de ocurrencia de los símbolos en el archivo
    frequencies = {}

    with open(file_path, 'rb') as file:
        byte = file.read(1)
        while byte:
            symbol = byte.decode('latin-1')
            if symbol in frequencies:
                frequencies[symbol] += 1
            else:
                frequencies[symbol] = 1
            byte = file.read(1)

    return frequencies


def build_huffman_tree(symbol_frequencies):
    # Construir el árbol de Huffman basado en las frecuencias de ocurrencia de los símbolos
    heap = []

    for symbol, frequency in symbol_frequencies.items():
        node = HuffmanNode(symbol, frequency)
        heapq.heappush(heap, node)

    while len(heap) > 1:
        node1 = heapq.heappop(heap)
        node2 = heapq.heappop(heap)
        merged_frequency = node1.frequency + node2.frequency
        merged_node = HuffmanNode(frequency=merged_frequency)
        merged_node.left = node1
        merged_node.right = node2
        heapq.heappush(heap, merged_node)

    return heap[0]


def build_huffman_code_table(huffman_tree):
    # Construir la tabla de códigos Huffman utilizando el árbol de Huffman
    code_table = {}

    def traverse_tree(node, code):
        if node.symbol:
            code_table[node.symbol] = code
        else:
            traverse_tree(node.left, code + '0')
            traverse_tree(node.right, code + '1')

    traverse_tree(huffman_tree, '')

    return code_table


def compress_file(file_path, code_table):
    # Comprimir el archivo utilizando la tabla de códigos Huffman
    compressed_data = ''

    with open(file_path, 'rb') as file:
        byte = file.read(1)
        while byte:
            symbol = byte.decode('latin-1')
            compressed_data += code_table[symbol]
            byte = file.read(1)

    return compressed_data


def write_compressed_file(file_path, compressed_data, code_table):
    # Escribir los datos comprimidos y la tabla de códigos en un archivo
    output_file_path = file_path + '.compressed'
    with open(output_file_path, 'w') as file:
        # Escribir la tabla de códigos en el archivo
        for symbol, code in code_table.items():
            file.write(f'{symbol}:{code}\n')

        file.write('\n')  # Separador entre la tabla de códigos y los datos comprimidos

        # Escribir los datos comprimidos en el archivo
        file.write(compressed_data)

    return output_file_path


def read_code_table(compressed_file_path):
    # Leer la tabla de códigos Huffman desde un archivo comprimido
    code_table = {}

    with open(compressed_file_path, 'r') as file:
        # Saltar las líneas de la tabla de códigos hasta llegar al separador
        line = file.readline().strip()
        while line:
            line = file.readline().strip()
            if line == '':
                                break

            symbol, code = line.split(':')
            code_table[symbol] = code
            line = file.readline().strip()

    return code_table


def decompress_file(compressed_file_path, code_table):
    # Descomprimir el archivo utilizando la tabla de códigos Huffman
    decompressed_data = ''

    with open(compressed_file_path, 'r') as file:
        # Saltar las líneas de la tabla de códigos hasta llegar al separador
        line = file.readline().strip()
        while line:
            if line == '':
                break
            line = file.readline().strip()

        # Leer los datos comprimidos desde el archivo
        compressed_data = file.read()

    # Recorrer los datos comprimidos y buscar los códigos en la tabla para obtener los símbolos originales
    current_code = ''
    for bit in compressed_data:
        current_code += bit
        if current_code in code_table:
            symbol = code_table[current_code]
            decompressed_data += symbol
            current_code = ''

    return decompressed_data


# Ejemplo de uso
input_file = 'input.txt'
output_file = 'output.txt'
print(f"Archivo de entrada: {input_file}")
symbol_frequencies = get_symbol_frequencies(input_file)
print("Frecuencias de símbolos:")
for symbol, frequency in symbol_frequencies.items():
    print(f"{symbol}: {frequency}")
huffman_tree = build_huffman_tree(symbol_frequencies)
code_table = build_huffman_code_table(huffman_tree)
print("Tabla de códigos Huffman:")
for symbol, code in code_table.items():
    print(f"{symbol}: {code}")
compressed_data = compress_file(input_file, code_table)
compressed_file = write_compressed_file(input_file, compressed_data, code_table)
print(f"Archivo comprimido: {compressed_file}")
decompressed_data = decompress_file(compressed_file, code_table)
#print("Datos descomprimidos:")
print(decompressed_data)

# Escribir los resultados en el archivo de salida
with open(output_file, 'w') as file:
    file.write(f"Archivo de entrada: {input_file}\n")
    file.write("Frecuencias de símbolos:\n")
    for symbol, frequency in symbol_frequencies.items():
        file.write(f"{symbol}: {frequency}\n")

    file.write("Tabla de códigos Huffman:\n")
    for symbol, code in code_table.items():
        file.write(f"{symbol}: {code}\n")

    file.write(f"Archivo comprimido: {compressed_file}\n")
    #file.write("Datos descomprimidos:\n")
    file.write(decompressed_data)
