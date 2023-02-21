import pandas as pd
#.read:csv -> lee el archivo .csv
suscripciones = pd.read_csv("proyecto1-estructuras\suscripciones.csv")
listEtiquetas=[]
diccionarioEtiquetas={}
#while -> llena una lista con las etiquetas que desea crear el usuario
i='si'
print('Crea tus etiquetas')
while i=='si':
    etiquetas = input('Etiqueta : ')
    listEtiquetas.append(etiquetas)
    print('Si desea agregar otra etiqueta digite si \nSi NO desea agregar otra etiqueta digite no')
    i=input('--> ')
#for(externo) -> llena un diccionario donde cada etiqueta queda con los canales elegidos por el usuario
#for(interno) -> Cambia la lista de strings por una lista de números enteros
for i in listEtiquetas:
    print('Elija los canales que desea etiquetar en la etiqueta ',i)
    print(suscripciones)
    agregar=input('Digite los numeros de los canales separados por coma(,) que desea agregar a la etiqueta : ')
    separarCanales=agregar.split(",")
    for a in range(len(separarCanales)):
        separarCanales[a]=int(separarCanales[a])
    diccionarioEtiquetas.update({i:suscripciones.iloc[separarCanales,1:3]})
#for -> imprime la etiqueta con sus respectivos canales 
for i in diccionarioEtiquetas:
    print(i,'--> ',diccionarioEtiquetas[i])


