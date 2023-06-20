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


def arithmetic_coding(string:str,probabilities):
    #Se asume que las probabilidades son un diccionario
    u=0
    v=1
    p=v-u
    for n in range(0,len(string)):
        
        Q_n=0
        R_n=0

        #Calcular probabilidades acomulativas
        for letter,probability in probabilities.items():
            if letter != string[n]:
                Q_n= probability + Q_n
                R_n= probability + R_n
            else:
                R_n= probability + R_n
                break
        
        #Actualizar el intervalo [u,v)
        v = u + (p*R_n)
        u = u + (p*Q_n)
        p = v - u 
    
    return u+(p/2),len(string)


def compress_text(text):
    # Comprimir el texto a una lista de probabilidades y un número decimal
    probabilities = train_probabilistic_model(text)
    encoded_value,length = arithmetic_coding(text, probabilities)
    compressed_data = {
        'probabilities': probabilities,
        'encoded_value': encoded_value,
        'length':length
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
        file.write('\n')
        file.write('Length:\n')
        file.write(str(compressed_data['length']))

def read_input_text(file_path):
    # Leer el texto de entrada desde un archivo
    with open(file_path, 'r') as file:
        input_text = file.read()
    return input_text


def read_compressed_data():
    data = {}
    encoded_value = 0
    length = 0

    with open("compressed_data.txt", "r") as file:
        section = None

        for line in file:
            line = line.strip()

            if line == "Probabilities:":
                section = "Probabilities"
            elif line == "Encoded Value:":
                section = "Encoded Value"
            elif line == "Length:":
                section = "Length"
            else:
                if section == "Probabilities":
                    letter, value = line.split(":")
                    data[letter] = float(value)
                elif section == "Encoded Value":
                    encoded_value = float(line)
                elif section == "Length":
                    length = int(line)

    return data, encoded_value, length

def arithmeticDecoding(t,length,probabilities):
    u = 0
    v = 1
    tag=t

    decodedLength = 0
    decodedString = ""

    #Calcular el rango de probabilidades
    #Diccionario con el símbolo como llave y el valor máximo como valor
    probabilitiesRange = {}
    accomulatedProbability = 0
    for letter,probability in probabilities.items():
        accomulatedProbability = probability + accomulatedProbability
        probabilitiesRange[letter]=accomulatedProbability

    #Calculo de la decodificación
    while length >= decodedLength:  
        #Nuevo tag
        prevProbability = 0
        newTag = (tag-u)/(v-u)

        #Comprobación del rango de probabilidades
        for letter,probability in probabilitiesRange.items():
            if probability > newTag:
                decodedString = decodedString + letter
                decodedLength = decodedLength + 1
                u=prevProbability
                v=probability
                tag=newTag
                break
            else:
                prevProbability = probability
        if decodedLength==length:
            break

    return decodedString

# Obtener el texto de entrada desde un archivo
input_file = 'input.txt'
input_text = read_input_text(input_file)
print(f"Texto de entrada desde {input_file}: {input_text}")

compressed_data = compress_text(input_text)
output_file = 'compressed_data.txt'
save_compressed_data(compressed_data, output_file)
print(f"Datos comprimidos guardados en el archivo: {output_file}")

probabilities,tag,len=read_compressed_data()
print(arithmeticDecoding(tag,len,probabilities))