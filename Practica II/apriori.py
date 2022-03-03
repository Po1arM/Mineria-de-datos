from itertools import combinations

lines = []
dictionary = {}
allPass = False
soporte, confianza = 0.0,0.0

#Leer el archivo y determinar la cantidad de items iniciales
def getFile():
    global lines, dictionary,soporte,confianza 

    file = input("Ingrese la ubicacion del archivo: ") 
    text = open(file)
    lines = text.readlines()

    soporte = float(input("Ingrese el soporte minimo: "))
    confianza = float(input("Ingrese la confianza minima: "))

    #Determina cada producto unico y la cantidad de veces que aparece en el dataset
    for line in lines:
        x = line.split(" ")
        for producto in x:
            #Elimina el caracter de salto de linea para hacer la comparacion
            producto = producto.replace("\n","")
            if producto in dictionary:
                #Si existe una entrada entonces se agrega uno a la cantidad de veces que aparece
                dictionary[producto] += 1
            else:
                #Si no, se crea la entrada
                dictionary[producto] = 1

#Revisa las veces que aparece un subset dentro de las transacciones totales
def checkSubSet(originalSet,subsetSize):
    if subsetSize == 2:
        #Si es la primera vez, se hace una combinacion de todos los items
        dataset = list(combinations(list(dictionary.keys()),subsetSize))
    else:
        #Si no, se crean los nuevos subsets eliminando valores repetidos
        dataset = generateSubSet(originalSet,subsetSize)

    auxSet = {}
    
    #Se revisa cuantas veces aparece un subset dentro del conjunto de transacciones
    for itemSet in dataset:
        for line in lines:
            if check(itemSet,line):
                if itemSet in auxSet:
                    auxSet[itemSet] += 1
                else:
                    auxSet[itemSet] = 1 
    
    return checkSoporte(auxSet)
    
#Revisa que el soporte para un subset sea mayor al soporte especificado
def checkSoporte(dataSet):
    exitSet = []
    for itemSet in dataSet.keys():
        itemSuport = dataSet[itemSet]/len(lines)
        if itemSuport > soporte:
            exitSet.append(itemSet)
    
    return exitSet

#Revisa que un subset completo se encuentre dentro de una transaccion
def check(tuple, line):
    for i in tuple:
        if i not in line:
            return False
    return True

#Genera los nuevos subsets verificando que no existan ni subsets iguales, ni elementos repetidos dentro de este
def generateSubSet(originalSet,n):
    global allPass
    auxList = []
    for i in range(len(originalSet)-1):
        for k in range(1+i,len(originalSet)):
            for j in originalSet[k]:
                aux = (j,)
                auxList.append(tuple(originalSet[i]) + aux)

    nuevaLista = list(set(map(tuple,map(sorted,auxList))))
    aux = []

    for tup in nuevaLista:
        b = set()
        result=[element for element in tup
            if not (tuple(element) in b
                or  b.add(tuple(element)))]
        if len(result) == n:
            aux.append(tuple(result))
        else:
            allPass = False

    return aux

#Genera el formato de regla a traves de la division de las tuplas
def checkConfianza(dataset):
    reglas = []
    for subSet in dataset:
        auxset = list(powerset(subSet))[1:-1]
        for aux in auxset:
            aux = set(tuple(aux))
            aux1 = set(subSet)
            result = tuple(aux1 - aux)
            
            reglas.append(checkLines(aux,result,tuple(subSet)))
    
    result = {}
    for dict in reglas:
        result.update(dict)
    return result

#Genera los supersets para dividir el antecedente del consecuente
def powerset(s):
    x = len(s)
    masks = [1 << i for i in range(x)]
    for i in range(1 << x):
        yield [ss for mask, ss in zip(masks, s) if i & mask]

#Calcula la confianza de una regla y devuelve las reglas cuya confianza sea mayor a la especificada 
#Por el usuario
def checkLines(ante,cons, set):
    cantAnte = 0
    cantSet = 0

    listByConfianza = {}
    for line in lines:
        if check(ante,line):
            cantAnte += 1
            if check(set,line):
                cantSet +=1
    if cantSet/cantAnte > confianza:
        regla = f'{ante} -> {cons}'
        listByConfianza[regla] = cantSet/cantAnte 

    return listByConfianza

def main():
    global allPass
    getFile()
    dataSet = checkSoporte(dictionary)
    cont = 2
    while not allPass:
        allPass = True
        dataSet = checkSubSet(dataSet,cont)
        cont += 1
        if len(dataSet) == 0:
            print("No hay reglas de asociacion para los valores datos")
            exit()
    
    dataSet = checkConfianza(dataSet)

    print("\nReglas encontradas: ")
    dataSet = dict(sorted(dataSet.items(), key=lambda item: item[1],reverse=True))
    for set in dataSet:
        print(set, dataSet[set])


main()