def arithmeticEncoding(string:str,probabilities):
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

x="casa"
P={"c":1/4,"a":2/4,"s":1/4,}

tag,len=arithmeticEncoding(x,P)
print(arithmeticDecoding(tag,len,P))


