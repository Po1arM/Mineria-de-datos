#Determina los articulos y la cantidad de cada uno
lines = []
dictionary = {}
text = open('C:/Users/FGuzm/Desktop/prueba.txt')
lines = text.readlines()

#Determina cada producto unico y la cantidad de veces que aparece en el dataset
for line in lines:
    x = line.split(", ")
    for producto in x:
        producto = producto.lower()
        #Elimina el caracter de salto de linea para hacer la comparacion
        producto = producto.replace("\n","")
        if producto in dictionary:
            #Si existe una entrada entonces se agrega uno a la cantidad de veces que aparece
           dictionary[producto] += 1
        else:
            #Si no, se crea la entrada
           dictionary[producto] = 1
#Arreglo unicamente con los nombres de los productos           
llaves = list(dictionary.keys())

#Asigna una letra a cada producto
cont = 0
arr = []
for i in range(65,65 + 35):
    if i <= 90:
        #Letras mayusculas
        arr.append(chr(i))
    else:
        #Letras minusculas
        arr.append(chr(i+6))

text.close
for i in dictionary.items():
    print(i)
#Crea el archivo arff
nuevoFile = input("Nombre del arff: ")
text = open(nuevoFile,"a")

text.write("@relation comprasPucmm\n")
#Define las lineas de attribute
for producto in llaves:
    text.write("@attribute '"+producto+"' { t}\n")

#Define la seccion de datos en formato binario
text.write("\n@data")
for line in lines:
    compra = [0 for i in range(len(llaves))]
    x = line.split(", ")
    for producto in x:
        producto = producto.lower()
        producto = producto.replace("\n","")
        
        compra[llaves.index(producto)] = 1

    #Eliminando caracteres inecesarios
    compraStr = str(compra).replace("[","")
    compraStr = compraStr.replace("]","")
    compraStr = compraStr.replace("0","?")
    compraStr = compraStr.replace("1","t")
    compraStr = compraStr.replace(" ","")
    text.write("\n"+compraStr)



